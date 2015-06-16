.. _set_highlight:

Set Highlight
-------------

**set highlight** [ **reset** ] {**plain** | **light** | **dark** | **off**}

Set whether we use terminal highlighting. Permissable values are:

:plain:
   no terminal highlighting
:off:
   same as plain
:light:
   terminal background is light (the default)
:dark:
   terminal background is dark

If the first argument is *reset*, we clear any existing color formatting
and recolor all source code output.

Examples:
+++++++++

    set highlight off   # no highlight
    set highlight plain # same as above
    set highlight       # same as above
    set highlight dark  # terminal has dark background
    set highlight light # terminal has light background
    set highlight reset light # clear source-code cache and
                              # set for light background
    set highlight reset # clear source-code cache

.. seealso::

   :ref:`show highlight <show_highlight>`
