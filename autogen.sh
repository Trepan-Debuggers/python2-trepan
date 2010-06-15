#!/bin/sh
# Things to do after doing a clean SVN update to add the proper files.
ln -vfs README.txt README
[ ! -f version.m4 ] && touch version.m4
autoreconf -i -s
