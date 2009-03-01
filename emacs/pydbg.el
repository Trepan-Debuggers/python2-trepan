;; Copyright (C) 2006, 2007 Free Software Foundation, Inc.
;; Copyright (C) 2007, 2009 Rocky Bernstein (rocky@gnu.org) 
;; This file is (not yet) part of GNU Emacs.

;; GNU Emacs is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation; either version 2, or (at your option)
;; any later version.

;; GNU Emacs is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with GNU Emacs; see the file COPYING.  If not, write to the
;; Free Software Foundation, Inc., 59 Temple Place - Suite 330,
;; Boston, MA 02111-1307, USA.
;; ======================================================================
;; pydbg (Python extended debugger) functions

(if (< emacs-major-version 22)
  (error
   "This version of pydbg.el needs at least Emacs 22 or greater - you have version %d."
   emacs-major-version))

(require 'gud)


;; User-definable variables
;; vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

(defcustom gud-pydbg-command-name "pydbg --annotate=3"
  "File name for executing the Python debugger.
This should be an executable on your path, or an absolute file name."
  :type 'string
  :group 'gud)

(defcustom pydbg-temp-directory
  (let ((ok '(lambda (x)
	       (and x
		    (setq x (expand-file-name x)) ; always true
		    (file-directory-p x)
		    (file-writable-p x)
		    x))))
    (or (funcall ok (getenv "TMPDIR"))
	(funcall ok "/usr/tmp")
	(funcall ok "/tmp")
	(funcall ok "/var/tmp")
	(funcall ok  ".")
	(error
	 "Couldn't find a usable temp directory -- set `pydbg-temp-directory'")))
  "*Directory used for temporary files created by a *Python* process.
By default, the first directory from this list that exists and that you
can write into: the value (if any) of the environment variable TMPDIR,
/usr/tmp, /tmp, /var/tmp, or the current directory."
  :type 'string
  :group 'pydbg)

(defgroup pydbgtrack nil
  "Pydbg file tracking by watching the prompt."
  :prefix "pydbg-pydbgtrack-"
  :group 'shell)

(defcustom pydbg-pydbgtrack-do-tracking-p nil
  "*Controls whether the pydbgtrack feature is enabled or not.
When non-nil, pydbgtrack is enabled in all comint-based buffers,
e.g. shell buffers and the *Python* buffer.  When using pydbg to debug a
Python program, pydbgtrack notices the pydbg prompt and displays the
source file and line that the program is stopped at, much the same way
as gud-mode does for debugging C programs with gdb."
  :type 'boolean
  :group 'pydbg)
(make-variable-buffer-local 'pydbg-pydbgtrack-do-tracking-p)

(defcustom pydbg-many-windows nil
  "*If non-nil, display secondary pydbg windows, in a layout similar to `gdba'.
However only set to the multi-window display if the pydbg
command invocation has an annotate options (\"--annotate 1\"."
  :type 'boolean
  :group 'pydbg)

(defcustom pydbg-pydbgtrack-minor-mode-string " PYDBG"
  "*String to use in the minor mode list when pydbgtrack is enabled."
  :type 'string
  :group 'pydbg)


;; ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
;; NO USER DEFINABLE VARIABLES BEYOND THIS POINT

(defvar gud-pydbg-history nil
  "History of argument lists passed to pydbg.")

(defconst gud-pydbg-marker-regexp
  "^(\\(\\(?:[a-zA-Z]:\\)?[-a-zA-Z0-9_/.\\\\ ]+\\):\\([0-9]+\\))"
  "Regular expression used to find a file location given by pydbg.

Program-location lines look like this:
   (/usr/bin/zonetab2pot.py:15): <module>
or MS Windows:
   (c:\\mydirectory\\gcd.py:10): <module>
and in tracebacks like this:
   (/usr/bin/zonetab2pot.py:15)
")

(defconst gud-pydbg-marker-regexp-file-group 1
  "Group position in gud-pydbg-marker-regexp that matches the file name.")

(defconst gud-pydbg-marker-regexp-line-group 2
  "Group position in gud-pydbg-marker-regexp that matches the line number.")

;;-----------------------------------------------------------------------------
;; ALB - annotations support
;;-----------------------------------------------------------------------------

(defconst pydbg-annotation-start-regexp
  "\\([a-z]+\\)\n")
(defconst pydbg-annotation-end-regexp
  "^\n")

(defun gud-pydbg-massage-args (file args)
  args)

;; There's no guarantee that Emacs will hand the filter the entire
;; marker at once; it could be broken up across several strings.  We
;; might even receive a big chunk with several markers in it.  If we
;; receive a chunk of text which looks like it might contain the
;; beginning of a marker, we save it here between calls to the
;; filter.
(defun gud-pydbg-marker-filter (string)
  ;;(message "GOT: %s" string)
  (setq gud-marker-acc (concat gud-marker-acc string))
  ;;(message "ACC: %s" gud-marker-acc)
  (let ((output "") s s2 (tmp ""))

    ;; ALB first we process the annotations (if any)
    (while (setq s (string-match pydbg-annotation-start-regexp
                                 gud-marker-acc))
      (let ((name (substring gud-marker-acc (match-beginning 1) (match-end 1)))
            (end (match-end 0)))
        (if (setq s2 (string-match pydbg-annotation-end-regexp
                                   gud-marker-acc end))
            ;; ok, annotation complete, process it and remove it
            (let ((contents (substring gud-marker-acc end s2))
                  (end2 (match-end 0)))
              (pydbg-process-annotation name contents)
              (setq gud-marker-acc
                    (concat (substring gud-marker-acc 0 s)
                            (substring gud-marker-acc end2))))
          ;; otherwise, save the partial annotation to a temporary, and re-add
          ;; it to gud-marker-acc after normal output has been processed
          (setq tmp (substring gud-marker-acc s))
          (setq gud-marker-acc (substring gud-marker-acc 0 s)))))
    
    (when (setq s (string-match pydbg-annotation-end-regexp gud-marker-acc))
      ;; save the beginning of gud-marker-acc to tmp, remove it and restore it
      ;; after normal output has been processed
      (setq tmp (substring gud-marker-acc 0 s))
      (setq gud-marker-acc (substring gud-marker-acc s)))
           
    ;; Process all the complete markers in this chunk.
    ;; Format of line looks like this:
    ;;   (/etc/init.d/ntp.init:16):
    ;; but we also allow DOS drive letters
    ;;   (d:/etc/init.d/ntp.init:16):
    (while (string-match gud-pydbg-marker-regexp gud-marker-acc)
      (setq

       ;; Extract the frame position from the marker.
       gud-last-frame
       (cons (substring gud-marker-acc 
			(match-beginning gud-pydbg-marker-regexp-file-group) 
			(match-end gud-pydbg-marker-regexp-file-group))
	     (string-to-number
	      (substring gud-marker-acc
			 (match-beginning gud-pydbg-marker-regexp-line-group)
			 (match-end gud-pydbg-marker-regexp-line-group))))

       ;; Append any text before the marker to the output we're going
       ;; to return - include the marker in this text.
       output (concat output
		      (substring gud-marker-acc 0 (match-end 0)))

       ;; Set the accumulator to the remaining text.
       gud-marker-acc (substring gud-marker-acc (match-end 0))))

    ;; Does the remaining text look like it might end with the
    ;; beginning of another marker?  If it does, then keep it in
    ;; gud-marker-acc until we receive the rest of it.  Since we
    ;; know the full marker regexp above failed, it's pretty simple to
    ;; test for marker starts.
    (if (string-match "\032.*\\'" gud-marker-acc)
	(progn
	  ;; Everything before the potential marker start can be output.
	  (setq output (concat output (substring gud-marker-acc
						 0 (match-beginning 0))))

	  ;; Everything after, we save, to combine with later input.
	  (setq gud-marker-acc
		(concat tmp (substring gud-marker-acc (match-beginning 0)))))

      (setq output (concat output gud-marker-acc)
	    gud-marker-acc tmp))

    output))

(defun gud-pydbg-find-file (f)
  (find-file-noselect f 'nowarn))

; From Emacs 23
(unless (fboundp 'split-string-and-unquote)
  (defun split-string-and-unquote (string &optional separator)
  "Split the STRING into a list of strings.
It understands Emacs Lisp quoting within STRING, such that
  (split-string-and-unquote (combine-and-quote-strings strs)) == strs
The SEPARATOR regexp defaults to \"\\s-+\"."
  (let ((sep (or separator "\\s-+"))
	(i (string-match "[\"]" string)))
    (if (null i)
	(split-string string sep t)	; no quoting:  easy
      (append (unless (eq i 0) (split-string (substring string 0 i) sep t))
	      (let ((rfs (read-from-string string i)))
		(cons (car rfs)
		      (split-string-and-unquote (substring string (cdr rfs))
						sep)))))))
)

(defun pydbg-get-script-name (args &optional annotate-p)
  "Pick out the script name from the command line and return a
list of that and whether the annotate option was set. Initially
annotate should be set to nil."
  (let ((arg (pop args)))
     (cond 
      ((not arg) (list nil annotate-p))
      ((string-match "^--annotate=[1-9]" arg)
       (pydbg-get-script-name args t))
      ((member arg '("-t" "--target" "-o" "--output"
		    "--execute" "-e" "--error" "--cd" "-x" "--command"))
       (if args 
	   (pydbg-get-script-name (cdr args) annotate-p)
       ;else
	 (list nil annotate-p)))
      ((string-match "^-[a-zA-z]" arg) (pydbg-get-script-name args annotate-p))
      ((string-match "^--[a-zA-z]+" arg) (pydbg-get-script-name args annotate-p))
      ((string-match "^pydbg" arg) (pydbg-get-script-name args annotate-p))
     ; found script name (or nil
      (t (list arg annotate-p)))))

;;;###autoload
(defun pydbg (command-line)
  "Run pydbg on program FILE in buffer *gud-cmd-FILE*.
The directory containing FILE becomes the initial working directory
and source-file directory for your debugger.

The custom variable `gud-pydbg-command-name' sets the pattern used
to invoke pydbg.

If `pydbg-many-windows' is nil (the default value) then pydbg just
starts with two windows: one displaying the GUD buffer and the
other with the source file with the main routine of the inferior.

If `pydbg-many-windows' is t, regardless of the value of the layout
below will appear.

+----------------------------------------------------------------------+
|                               GDB Toolbar                            |
+-----------------------------------+----------------------------------+
| GUD buffer (I/O of pydbg)          | Locals buffer                    |
|                                   |                                  |
|                                   |                                  |
|                                   |                                  |
+-----------------------------------+----------------------------------+
| Source buffer                                                        |
|                                                                      |
+-----------------------------------+----------------------------------+
| Stack buffer                      | Breakpoints buffer               |
| RET  pydbg-goto-stack-frame        | SPC    pydbg-toggle-breakpoint    |
|                                   | RET    pydbg-goto-breakpoint      |
|                                   | D      pydbg-delete-breakpoint    |
+-----------------------------------+----------------------------------+
"
  (interactive
   (list (gud-query-cmdline 'pydbg)))

  ; Parse the command line and pick out the script name and whether --annotate
  ; has been set.
  (let* ((words (split-string-and-unquote command-line))
	(script-name-annotate-p (pydbg-get-script-name 
			       (gud-pydbg-massage-args "1" words) nil))
	(target-name (file-name-nondirectory (car script-name-annotate-p)))
	(annotate-p (cadr script-name-annotate-p))
	(pydbg-buffer-name (format "*pydbg-cmd-%s*" target-name))
	(pydbg-buffer (get-buffer pydbg-buffer-name))
	)

    ;; `gud-pydbg-massage-args' needs whole `command-line'.
    ;; command-line is refered through dyanmic scope.
    (gud-common-init command-line 'gud-pydbg-massage-args
		     'gud-pydbg-marker-filter 'gud-pydbg-find-file)
    
    ; gud-common-init sets the pydbg process buffer name incorrectly, because
    ; it can't parse the command line properly to pick out the script name.
    ; So we'll do it here and rename that buffer. The buffer we want to rename
    ; happens to be the current buffer.
    (setq gud-target-name target-name)
    (when pydbg-buffer (kill-buffer pydbg-buffer))
    (rename-buffer pydbg-buffer-name)

    (set (make-local-variable 'gud-minor-mode) 'pydbg)

    (gud-def gud-args   "info args" "a"
	     "Show arguments of current stack.")
    (gud-def gud-break  "break %d%f:%l""\C-b"
	     "Set breakpoint at current line.")
    (gud-def gud-cont   "continue"   "\C-r" 
	     "Continue with display.")
    (gud-def gud-down   "down %p"     ">"
	     "Down N stack frames (numeric arg).")
    (gud-def gud-finish "finish"      "f\C-f"
	     "Finish executing current function.")
    (gud-def gud-next   "next %p"     "\C-n"
	     "Step one line (skip functions).")
    (gud-def gud-print  "p %e"        "\C-p"
	     "Evaluate python expression at point.")
    (gud-def gud-remove "clear %d%f:%l" "\C-d"
	     "Remove breakpoint at current line")
    (gud-def gud-run    "run"       "R"
	     "Restart the Python script.")
    (gud-def gud-statement "eval %e" "\C-e"
	     "Execute Python statement at point.")
    (gud-def gud-step   "step %p"       "\C-s"
	     "Step one source line with display.")
    (gud-def gud-tbreak "tbreak %d%f:%l"  "\C-t"
	     "Set temporary breakpoint at current line.")
    (gud-def gud-up     "up %p"
	     "<" "Up N stack frames (numeric arg).")
    (gud-def gud-where   "where"
	     "T" "Show stack trace.")
    (local-set-key "\C-i" 'gud-gdb-complete-command)
    (setq comint-prompt-regexp "^(+Pydbg[*]?)+ +")
    (setq paragraph-start comint-prompt-regexp)
    
    ;; Update GUD menu bar
    (define-key gud-menu-map [args]      '("Show arguments of current stack" . 
					 gud-args))
    (define-key gud-menu-map [down]      '("Down Stack" . gud-down))
    (define-key gud-menu-map [eval]      '("Execute Python statement at point" 
					   . gud-statement))
    (define-key gud-menu-map [finish]    '("Finish Function" . gud-finish))
    (define-key gud-menu-map [run]       '("Restart the Python Script" . 
					   gud-run))
    (define-key gud-menu-map [stepi]     'undefined)
    (define-key gud-menu-map [tbreak]    '("Temporary break" . gud-tbreak))
    (define-key gud-menu-map [up]        '("Up Stack" . gud-up))
    (define-key gud-menu-map [where]     '("Show stack trace" . gud-where))
    
    (local-set-key [menu-bar debug finish] '("Finish Function" . gud-finish))
    (local-set-key [menu-bar debug up] '("Up Stack" . gud-up))
    (local-set-key [menu-bar debug down] '("Down Stack" . gud-down))
    
    (setq comint-prompt-regexp "^(+Pydbg[*]?)+ +")
    (setq paragraph-start comint-prompt-regexp)
    
					; remove other py-pdbtrack if which gets in the way
    (remove-hook 'comint-output-filter-functions 'py-pdbtrack-track-stack-file)
    
    (setq paragraph-start comint-prompt-regexp)
    (when (and annotate-p pydbg-many-windows) (pydbg-setup-windows))
    
    (run-hooks 'pydbg-mode-hook)))
  
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; pydbgtrack --- tracking pydbg debugger in an Emacs shell window
;;; Modified from  python-mode in particular the part:
;; pdbtrack support contributed by Ken Manheimer, April 2001.

;;; Code:

(require 'comint)
(require 'custom)
(require 'cl)
(require 'compile)
(require 'shell)

;; have to bind pydbg-file-queue before installing the kill-emacs-hook
(defvar pydbg-file-queue nil
  "Queue of Makefile temp files awaiting execution.
Currently-active file is at the head of the list.")

(defvar pydbg-pydbgtrack-is-tracking-p t)


;; Constants

(defconst pydbg-position-re 
  "\\(^\\|\n\\)(\\(\\(?:[A-Za-z]:\\)?[^:]+\\):\\([0-9]*\\)).*\n"
  "Regular expression for a pydbg position")

(defconst pydbg-marker-regexp-file-group 2
  "Group position in pydbg-postiion-re that matches the file name.")

(defconst pydbg-marker-regexp-line-group 3
  "Group position in pydbg-position-re that matches the line number.")

(defconst pydbg-traceback-line-re
  "^[ \t]+File \"\\([^\"]+\\)\", line \\([0-9]*\\),"
  "Regular expression that describes Python tracebacks.")

(defconst pydbg-pydbgtrack-input-prompt "\n(+Pydbg[*]?)+ +"
  "Regular expression pydbgtrack uses to recognize a pydbg prompt.")

(defconst pydbg-pydbgtrack-track-range 10000
  "Max number of characters from end of buffer to search for stack entry.")


(defun pydbg-pydbgtrack-overlay-arrow (activation)
  "Activate or de arrow at beginning-of-line in current buffer."
  ;; This was derived/simplified from edebug-overlay-arrow
  (cond (activation
	 (setq overlay-arrow-position (make-marker))
	 (setq overlay-arrow-string "=>")
	 (set-marker overlay-arrow-position (point) (current-buffer))
	 (setq pydbg-pydbgtrack-is-tracking-p t))
	(pydbg-pydbgtrack-is-tracking-p
	 (setq overlay-arrow-position nil)
	 (setq pydbg-pydbgtrack-is-tracking-p nil))
	))

(defun pydbg-pydbgtrack-track-stack-file (text)
  "Show the file indicated by the pydbg stack entry line, in a separate window.
Activity is disabled if the buffer-local variable
`pydbg-pydbgtrack-do-tracking-p' is nil.

We depend on the pydbg input prompt matching `pydbg-pydbgtrack-input-prompt'
at the beginning of the line.
" 
  ;; Instead of trying to piece things together from partial text
  ;; (which can be almost useless depending on Emacs version), we
  ;; monitor to the point where we have the next pydbg prompt, and then
  ;; check all text from comint-last-input-end to process-mark.
  ;;
  ;; Also, we're very conservative about clearing the overlay arrow,
  ;; to minimize residue.  This means, for instance, that executing
  ;; other pydbg commands wipe out the highlight.  You can always do a
  ;; 'where' (aka 'w') command to reveal the overlay arrow.
  (let* ((origbuf (current-buffer))
	 (currproc (get-buffer-process origbuf)))

    (if (not (and currproc pydbg-pydbgtrack-do-tracking-p))
        (pydbg-pydbgtrack-overlay-arrow nil)
      ;else 
      (let* ((procmark (process-mark currproc))
	     (block-start (max comint-last-input-end
			       (- procmark pydbg-pydbgtrack-track-range)))
             (block-str (buffer-substring block-start procmark))
             target target_fname target_lineno target_buffer)

        (if (not (string-match (concat pydbg-pydbgtrack-input-prompt "$") block-str))
            (pydbg-pydbgtrack-overlay-arrow nil)

          (setq target (pydbg-pydbgtrack-get-source-buffer block-str))

          (if (stringp target)
              (message "pydbgtrack: %s" target)
	    ;else
	    (gud-pydbg-marker-filter block-str)
            (setq target_lineno (car target))
            (setq target_buffer (cadr target))
            (setq target_fname (buffer-file-name target_buffer))
            (switch-to-buffer-other-window target_buffer)
            (goto-line target_lineno)
            (message "pydbgtrack: line %s, file %s" target_lineno target_fname)
            (pydbg-pydbgtrack-overlay-arrow t)
            (pop-to-buffer origbuf t)
	    )

	  ; Delete processed annotations from buffer.
	  (save-excursion
	    (let ((annotate-start)
		  (annotate-end (point-max)))
	      (goto-char block-start)
	      (while (re-search-forward
		      pydbg-annotation-start-regexp annotate-end t)
		(setq annotate-start (match-beginning 0))
		(if (re-search-forward 
		     pydbg-annotation-end-regexp annotate-end t)
		    (delete-region annotate-start (point))
		;else
		  (forward-line)))
	      )))
	)))
  )

(defun pydbg-pydbgtrack-get-source-buffer (block-str)
  "Return line number and buffer of code indicated by block-str's traceback 
text.

We look first to visit the file indicated in the trace.

Failing that, we look for the most recently visited python-mode buffer
with the same name or having 
having the named function.

If we're unable find the source code we return a string describing the
problem as best as we can determine."

  (if (not (string-match pydbg-position-re block-str))

      "line number cue not found"

    (let* ((filename (match-string pydbg-marker-regexp-file-group block-str))
           (lineno (string-to-number
		    (match-string pydbg-marker-regexp-line-group block-str)))
           funcbuffer)

      (cond ((file-exists-p filename)
             (list lineno (find-file-noselect filename)))

            ((= (elt filename 0) ?\<)
             (format "(Non-file source: '%s')" filename))

            (t (format "Not found: %s" filename)))
      )
    )
  )


;;; Subprocess commands



;; pydbgtrack functions
(defun pydbg-pydbgtrack-toggle-stack-tracking (arg)
  (interactive "P")
  (if (not (get-buffer-process (current-buffer)))
      (error "No process associated with buffer '%s'" (current-buffer)))
  ;; missing or 0 is toggle, >0 turn on, <0 turn off
  (if (or (not arg)
	  (zerop (setq arg (prefix-numeric-value arg))))
      (setq pydbg-pydbgtrack-do-tracking-p (not pydbg-pydbgtrack-do-tracking-p))
    (setq pydbg-pydbgtrack-do-tracking-p (> arg 0)))
  (message "%sabled pydbg's pydbgtrack"
           (if pydbg-pydbgtrack-do-tracking-p "En" "Dis")))

(defun turn-on-pydbgtrack ()
  (interactive)
  (pydbg-pydbgtrack-toggle-stack-tracking 1)
  (setq pydbg-pydbgtrack-is-tracking-p t)
  (local-set-key "\C-cg" 'pydbg-goto-traceback-line)
  (add-hook 'comint-output-filter-functions 'pydbg-pydbgtrack-track-stack-file)
  ; remove other py-pdbtrack if which gets in the way
  (remove-hook 'comint-output-filter-functions 'py-pdbtrack-track-stack-file))
  (remove-hook 'comint-output-filter-functions 
	       'py-rdebugtrack-track-stack-file)


(defun turn-off-pydbgtrack ()
  (interactive)
  (pydbg-pydbgtrack-toggle-stack-tracking 0)
  (setq pydbg-pydbgtrack-is-tracking-p nil)
  (remove-hook 'comint-output-filter-functions 
	       'pydbg-pydbgtrack-track-stack-file) )

;; Add a designator to the minor mode strings if we are tracking
(or (assq 'pydbg-pydbgtrack-minor-mode-string minor-mode-alist)
    (push '(pydbg-pydbgtrack-is-tracking-p
	    pydbg-pydbgtrack-minor-mode-string)
	  minor-mode-alist)) 
;; pydbgtrack


;;-----------------------------------------------------------------------------
;; ALB - annotations support
;;-----------------------------------------------------------------------------

(defvar pydbg--annotation-setup-map
  (progn
    (define-hash-table-test 'str-hash 'string= 'sxhash)
    (let ((map (make-hash-table :test 'str-hash)))
      (puthash "breakpoints" 'pydbg--setup-breakpoints-buffer map)
      (puthash "stack" 'pydbg--setup-stack-buffer map)
      (puthash "locals" 'pydbg--setup-locals-buffer map)
      map)))

(defun pydbg-process-annotation (name contents)
  (let ((buf (get-buffer-create (format "*pydbg-%s-%s*" name gud-target-name))))
    (with-current-buffer buf
      (setq buffer-read-only t)
      (let ((inhibit-read-only t)
            (setup-func (gethash name pydbg--annotation-setup-map)))
        (erase-buffer)
        (insert contents)
        (when setup-func (funcall setup-func buf))))))

(defun pydbg-setup-windows ()
  "Layout the window pattern for `pydbg-many-windows'. This was mostly copied
from `gdb-setup-windows', but simplified."
  (pop-to-buffer gud-comint-buffer)
  (let ((script-name gud-target-name))
    (delete-other-windows)
    (split-window nil ( / ( * (window-height) 3) 4))
    (split-window nil ( / (window-height) 3))
    (split-window-horizontally)
    (other-window 1)
    (set-window-buffer 
     (selected-window) 
     (get-buffer-create (format "*pydbg-locals-%s*" script-name)))
    (other-window 1)
    (switch-to-buffer
     (if gud-last-last-frame
	   (gud-find-file (car gud-last-last-frame))
       ;; Put buffer list in window if we
       ;; can't find a source file.
       (list-buffers-noselect)))
    (other-window 1)
    (set-window-buffer 
     (selected-window)
     (get-buffer-create (format "*pydbg-stack-%s*" script-name)))
    (split-window-horizontally)
    (other-window 1)
    (set-window-buffer 
      (selected-window) 
      (get-buffer-create (format "*pydbg-breakpoints-%s*" script-name)))
     (other-window 1)
     (goto-char (point-max))))
    
(defun pydbg-restore-windows ()
  "Equivalent of `gdb-restore-windows' for pydbg."
  (interactive)
  (when pydbg-many-windows
    (pydbg-setup-windows)))

(defun pydbg-set-windows (&optional name)
  "Sets window used in multi-window frame and issues
pydbg-restore-windows if pydbg-many-windows is set"
  (interactive "sProgram name: ")
  (when name (setq gud-target-name name)
	(setq gud-comint-buffer (current-buffer)))
  (when gud-last-frame (setq gud-last-last-frame gud-last-frame))
  (when pydbg-many-windows
    (pydbg-setup-windows)))

;; ALB fontification and keymaps for secondary buffers (breakpoints, stack)

;; -- breakpoints

(defvar pydbg-breakpoints-mode-map
  (let ((map (make-sparse-keymap))
	(menu (make-sparse-keymap "Breakpoints")))
    (define-key menu [quit] '("Quit"   . pydbg-delete-frame-or-window))
    (define-key menu [goto] '("Goto"   . pydbg-goto-breakpoint))
    (define-key menu [delete] '("Delete" . pydbg-delete-breakpoint))
    (define-key map [mouse-2] 'pydbg-goto-breakpoint-mouse)
    (define-key map [? ] 'pydbg-toggle-breakpoint)
    (define-key map [(control m)] 'pydbg-goto-breakpoint)
    (define-key map [?d] 'pydbg-delete-breakpoint)
    map)
  "Keymap to navigate/set/enable pydbg breakpoints.")

(defun pydbg-delete-frame-or-window ()
  "Delete frame if there is only one window.  Otherwise delete the window."
  (interactive)
  (if (one-window-p) (delete-frame)
    (delete-window)))

(defun pydbg-breakpoints-mode ()
  "Major mode for rdebug breakpoints.

\\{pydbg-breakpoints-mode-map}"
  (kill-all-local-variables)
  (setq major-mode 'pydbg-breakpoints-mode)
  (setq mode-name "PYDBG Breakpoints")
  (use-local-map pydbg-breakpoints-mode-map)
  (setq buffer-read-only t)
  (run-mode-hooks 'pydbg-breakpoints-mode-hook)
 ;(if (eq (buffer-local-value 'gud-minor-mode gud-comint-buffer) 'gdba)
  ;    'gdb-invalidate-breakpoints
  ;  'gdbmi-invalidate-breakpoints)
)

(defconst pydbg--breakpoint-regexp
  "^\\([0-9]+\\) +breakpoint +\\([a-z]+\\) +\\([a-z]+\\) +at +\\(.+\\):\\([0-9]+\\)$"
  "Regexp to recognize breakpoint lines in pydbg breakpoints buffers.")

(defun pydbg--setup-breakpoints-buffer (buf)
  "Detects breakpoint lines and sets up keymap and mouse navigation."
  (with-current-buffer buf
    (let ((inhibit-read-only t))
      (pydbg-breakpoints-mode)
      (goto-char (point-min))
      (while (not (eobp))
        (let ((b (point-at-bol)) 
	      (e (point-at-eol)))
          (when (string-match pydbg--breakpoint-regexp
                              (buffer-substring b e))
            (add-text-properties b e
                                 (list 'mouse-face 'highlight
                                       'keymap pydbg-breakpoints-mode-map))
            (add-text-properties
             (+ b (match-beginning 1)) (+ b (match-end 1))
             (list 'face font-lock-constant-face
                   'font-lock-face font-lock-constant-face))
            ;; fontify "keep/del"
            (let ((face (if (string= "keep" (buffer-substring
                                             (+ b (match-beginning 2))
                                             (+ b (match-end 2))))
                            compilation-info-face
                          compilation-warning-face)))
              (add-text-properties
               (+ b (match-beginning 2)) (+ b (match-end 2))
               (list 'face face 'font-lock-face face)))
            ;; fontify "enabled"
            (when (string= "y" (buffer-substring (+ b (match-beginning 3))
                                                 (+ b (match-end 3))))
              (add-text-properties
               (+ b (match-beginning 3)) (+ b (match-end 3))
               (list 'face compilation-error-face
                     'font-lock-face compilation-error-face)))
            (add-text-properties
             (+ b (match-beginning 4)) (+ b (match-end 4))
             (list 'face font-lock-comment-face
                   'font-lock-face font-lock-comment-face))
            (add-text-properties
             (+ b (match-beginning 5)) (+ b (match-end 5))
             (list 'face font-lock-constant-face
                   'font-lock-face font-lock-constant-face)))
        (forward-line)
        (beginning-of-line))))))

(defun pydbg-goto-breakpoint-mouse (event)
  "Displays the location in a source file of the selected breakpoint."
  (interactive "e")
  (with-current-buffer (window-buffer (posn-window (event-end event)))
    (pydbg-goto-breakpoint (posn-point (event-end event)))))

(defun pydbg-goto-breakpoint (pt)
  "Displays the location in a source file of the selected breakpoint."
  (interactive "d")
  (save-excursion
    (goto-char pt)
    (let ((s (buffer-substring (point-at-bol) (point-at-eol))))
      (when (string-match pydbg--breakpoint-regexp s)
        (pydbg-display-line
         (substring s (match-beginning 4) (match-end 4))
         (string-to-number (substring s (match-beginning 5) (match-end 5))))
        ))))

(defun pydbg-goto-traceback-line (pt)
  "Displays the location in a source file of the Python traceback line."
  (interactive "d")
  (save-excursion
    (goto-char pt)
    (let ((s (buffer-substring (point-at-bol) (point-at-eol)))
	  (gud-comint-buffer (current-buffer)))
      (when (string-match pydbg-traceback-line-re s)
        (pydbg-display-line
         (substring s (match-beginning 1) (match-end 1))
         (string-to-number (substring s (match-beginning 2) (match-end 2))))
        ))))

(defun pydbg-toggle-breakpoint (pt)
  "Toggles the breakpoint at PT in the breakpoints buffer."
  (interactive "d")
  (save-excursion
    (goto-char pt)
    (let ((s (buffer-substring (point-at-bol) (point-at-eol))))
      (when (string-match pydbg--breakpoint-regexp s)
        (let* ((enabled
                (string= (substring s (match-beginning 3) (match-end 3)) "y"))
               (cmd (if enabled "disable" "enable"))
               (bpnum (substring s (match-beginning 1) (match-end 1))))
          (gud-call (format "%s %s" cmd bpnum)))))))

(defun pydbg-delete-breakpoint (pt)
  "Deletes the breakpoint at PT in the breakpoints buffer."
  (interactive "d")
  (save-excursion
    (goto-char pt)
    (let ((s (buffer-substring (point-at-bol) (point-at-eol))))
      (when (string-match pydbg--breakpoint-regexp s)
        (let ((bpnum (substring s (match-beginning 1) (match-end 1))))
          (gud-call (format "delete %s" bpnum)))))))

(defun pydbg-display-line (file line &optional move-arrow)
  (let ((oldpos (and gud-overlay-arrow-position
                     (marker-position gud-overlay-arrow-position)))
        (oldbuf (and gud-overlay-arrow-position
                     (marker-buffer gud-overlay-arrow-position))))
    (gud-display-line file line)
    (unless move-arrow
      (when gud-overlay-arrow-position
        (set-marker gud-overlay-arrow-position oldpos oldbuf)))))


;; -- stack

(defvar pydbg-frames-mode-map
  (let ((map (make-sparse-keymap)))
    (define-key map [mouse-1] 'pydbg-goto-stack-frame-mouse)
    (define-key map [mouse-2] 'pydbg-goto-stack-frame-mouse)
    (define-key map [(control m)] 'pydbg-goto-stack-frame)
    map)
  "Keymap to navigate pydbg stack frames.")

(defun pydbg-frames-mode ()
  "Major mode for pydbg frames.

\\{pydbg-frames-mode-map}"
  ; (kill-all-local-variables)
  (interactive "")
  (setq major-mode 'pydbg-frames-mode)
  (setq mode-name "PYDBG Stack Frames")
  (use-local-map pydbg-frames-mode-map)
  ; (set (make-local-variable 'font-lock-defaults)
  ;     '(gdb-locals-font-lock-keywords))
  (run-mode-hooks 'pydbg-frames-mode-hook))

(defconst pydbg--stack-frame-regexp
  "^\\(->\\|##\\|  \\) +\\([0-9]+\\) +\\([^ (]+\\).+$"
  "Regexp to recognize stack frame lines in pydbg stack buffers.")

(defun pydbg--setup-stack-buffer (buf)
  "Detects stack frame lines and sets up mouse navigation."
  (with-current-buffer buf
    (let ((inhibit-read-only t)
	  (current-frame-point nil) ; position in stack buffer of selected frame
	  )
      (pydbg-frames-mode)
      (goto-char (point-min))
      (while (not (eobp))
        (let* ((b (point-at-bol)) 
	       (e (point-at-eol))
               (s (buffer-substring b e)))
          (when (string-match pydbg--stack-frame-regexp s)
            (add-text-properties
             (+ b (match-beginning 3)) (+ b (match-end 3))
             (list 'face font-lock-function-name-face
                   'font-lock-face font-lock-function-name-face))
            (when (string= (substring s (match-beginning 1) (match-end 1)) "->")
                ;; highlight the currently selected frame
                (add-text-properties b e
                                     (list 'face 'bold
                                           'font-lock-face 'bold))
		(setq overlay-arrow-position (make-marker))
		(set-marker overlay-arrow-position (point))
		(setq current-frame-point (point)))
            (add-text-properties b e
                                 (list 'mouse-face 'highlight
                                       'keymap pydbg-frames-mode-map))))
	;; remove initial ##  or ->
	(beginning-of-line)
	(delete-char 2)
        (forward-line)
        (beginning-of-line))
      ; Go back to the selected frame if any
      (when current-frame-point (goto-char current-frame-point))
      )))

(defun pydbg-goto-stack-frame (pt)
  "Show the pydbg stack frame correspoding at PT in the pydbg stack buffer."
  (interactive "d")
  (save-excursion
    (goto-char pt)
    (let ((s (concat "##" (buffer-substring (point-at-bol) (point-at-eol)))))
      (when (string-match pydbg--stack-frame-regexp s)
        (let ((frame (substring s (match-beginning 2) (match-end 2))))
          (gud-call (concat "frame " frame)))))))

(defun pydbg-goto-stack-frame-mouse (event)
  "Show the pydbg stack frame under the mouse in the pydbg stack buffer."
  (interactive "e")
  (with-current-buffer (window-buffer (posn-window (event-end event)))
    (pydbg-goto-stack-frame (posn-point (event-end event)))))

;; -- locals

(defvar pydbg-locals-mode-map
  (let ((map (make-sparse-keymap)))
    (suppress-keymap map)
    (define-key map "\r" 'pydbg-edit-locals-value)
    (define-key map "e" 'pydbg-edit-locals-value)
    (define-key map [mouse-1] 'pydbg-edit-locals-value)
    (define-key map [mouse-2] 'pydbg-edit-locals-value)
    (define-key map "q" 'kill-this-buffer)
     map))

(defun pydbg-locals-mode ()
  "Major mode for pydbg locals.

\\{pydbg-locals-mode-map}"
  ; (kill-all-local-variables)
  (setq major-mode 'pydbg-locals-mode)
  (setq mode-name "PYDBG Locals")
  (setq buffer-read-only t)
  (use-local-map pydbg-locals-mode-map)
  ; (set (make-local-variable 'font-lock-defaults)
  ;     '(gdb-locals-font-lock-keywords))
  (run-mode-hooks 'pydbg-locals-mode-hook))

(defun pydbg--setup-locals-buffer (buf)
  (with-current-buffer buf (pydbg-locals-mode)))

(defun pydbg-edit-locals-value (&optional event)
  "Assign a value to a variable displayed in the locals buffer."
  (interactive (list last-input-event))
  (save-excursion
    (if event (posn-set-point (event-end event)))
    (beginning-of-line)
    (let* ((var (current-word))
	   (value (read-string (format "New value (%s): " var))))
      (gud-call (format "! %s=%s" var value)))))

(defadvice gud-reset (before pydbg-reset)
  "pydbg cleanup - remove debugger's internal buffers (frame, breakpoints, 
etc.)."
  (dolist (buffer (buffer-list))
    (when (string-match "\\*pydbg-[a-z]+\\*" (buffer-name buffer))
      (let ((w (get-buffer-window buffer)))
        (when w (delete-window w)))
      (kill-buffer buffer))))

(ad-activate 'gud-reset)
(provide 'pydbg)

