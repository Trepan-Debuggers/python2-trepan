.. _set_highlight:

Set Highlight
-------------
**set highlight** [ **reset** ] {**plain** | **light** | **dark** | **off**}

Set whether we use terminal highlighting. Permissable values are:

       plain:  no terminal highlighting
       off:    same as plain
       light:  terminal background is light (the default)
       dark:   terminal background is dark

If the first argument is *reset*, we clear any existing color formatting
and recolor all source code output.

See also:
+++++++++

:ref:`show highlight <show_highlight>`
