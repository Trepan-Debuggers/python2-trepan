; -*- emacs-lisp -*-
(load-file "./elk-test.el")
(load-file "./pydbgr.el")

(make-variable-buffer-local 'gud-pydbgr-marker-acc)

(deftest "pydbgr-marker-filter-test"
  (assert-equal "Testing 1 2 3" (gud-pydbgr-marker-filter "Testing 1 2 3"))
  (assert-equal "ABC" (gud-pydbgr-marker-filter 
"breakpoints
No breakpoints

ABC")))

(defun regexp-stack-test (location-str)
  "Test to see that location-str matches pydbgr--stack-frame-regexp"
  (assert-equal 0 (string-match pydbgr--stack-frame-regexp location-str))
)
(defun regexp-breakpoint-test (location-str)
  "Test to see that location-str matches pydbgr--breakpoint-regexp"
  (assert-equal 0 (string-match pydbgr--breakpoint-regexp location-str))
)
(defun regexp-file-test (location-str file-str)
  "Test to see that location-str matches gud-pydbgr-marker-regexp"
  (assert-equal 0 (string-match gud-pydbgr-marker-regexp location-str))
  (assert-equal file-str
		(substring location-str
			   (match-beginning gud-pydbgr-marker-regexp-file-group) 
			   (match-end gud-pydbgr-marker-regexp-file-group)))
)
(deftest "pydbgr-marker-regexp-test"

  (regexp-breakpoint-test
   "1   breakpoint    keep y   at /src/external-cvs/pydbgr/test/gcd.py:24")
  (regexp-stack-test
   "-> 0 <module>() called from file '/src/external-cvs/pydbgr/test/gcd.py' at line 10")
  (regexp-stack-test 
   "   1 <module>() called from file '<string>' at line 1")
  (regexp-stack-test 
   "   2 run(self=<__main__.Pdb instance at 0xb7d2cc6c>, cmd='execfile( \"../test/gcd.py\")\n', globals={'__builti...) called from file '/usr/local/lib/python2.5/site-packages/pydbgr/pydbgrbdb.py' at line 313")

  (regexp-file-test 
   "(e:\\sources\\capfilterscanner\\capanalyzer.py:3):  <module>"
   "e:\\sources\\capfilterscanner\\capanalyzer.py"
   )
  (regexp-file-test 
   "(e:\\Documents and Settings\\jsmith\\My Documents\\cpanalyzer test.py:3):  <module>"
   "e:\\Documents and Settings\\jsmith\\My Documents\\cpanalyzer test.py"
   )  
  (regexp-file-test 
   "(/tmp/gcd.py:29):  gcd"
   "/tmp/gcd.py"
   )
  (regexp-file-test 
   "(/tmp/gcd.py:29)"
   "/tmp/gcd.py"
   )
)

(defun position-regexp-test (location-str file-str line-str)
  "Test to see that location-str matches position-regexp-test with the correct
file and line submatches."
  (assert-equal 0 (string-match pydbgr-position-re location-str))
  (assert-equal file-str (match-string pydbgr-marker-regexp-file-group
                                       location-str))
  (assert-equal line-str (match-string pydbgr-marker-regexp-line-group
                                       location-str))
  )
(deftest "pydbgr-position-re-test"

  (position-regexp-test 
   "(e:\\sources\\capfilterscanner\\capanalyzer.py:3):  <module>\n"
   "e:\\sources\\capfilterscanner\\capanalyzer.py" "3"
   )
  (position-regexp-test 
   "(e:\\Documents and Settings\\jsmith\\My Documents\\cpanalyzer test.py:3):  <module>\n"
   "e:\\Documents and Settings\\jsmith\\My Documents\\cpanalyzer test.py" "3"
   )  
  (position-regexp-test 
   "(/tmp/gcd.py:29):  gcd\n"
   "/tmp/gcd.py" "29"
   )
  (position-regexp-test 
   "(/tmp/gcd.py:29)\n"
   "/tmp/gcd.py" "29"
   )
)  
   
(deftest "pydbgr-get-script-name-test"
  (assert-equal '("foo" nil) (pydbgr-get-script-name '("foo")))
  (assert-equal '("foo" nil) (pydbgr-get-script-name '("-o" "myfile" "foo")))
  (assert-equal '("foo" t) (pydbgr-get-script-name '("--annotate=1" "foo")))
  (assert-equal '("foo" nil) 
		(pydbgr-get-script-name 
		 '("pydbgr" "--target" "tcp:127.0.0.1" "--nx" "foo")))
  (assert-equal '("foo" nil) (pydbgr-get-script-name 
			      '("pydbgr" "--threading" "--sigcheck" "--error"
				"errfile.out" "foo" "-1")))
)

(build-suite "pydbgr-suite" 
	     "pydbgr-marker-regexp-test" 
	     "pydbgr-position-re-test"
	     "pydbgr-marker-filter-test")
(run-elk-test "pydbgr-suite"
              "test regular expression used in tracking lines")

