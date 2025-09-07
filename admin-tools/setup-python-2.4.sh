#!/bin/bash
PYTHON_VERSION=2.4

if [[ $0 == $bs ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi

mydir=$(dirname $bs)
trepan2_owd=$(pwd)
cd $mydir/..
(cd $mydir/../../../rocky  && \
     setup_version python-uncompyle6 python-2.4 && \
     setup_version python-xdis python-2.4 && \
     setup_version python-filecache python-2.4 && \
     setup_version shell-term-background python-2.4 && \
     setup_version pytracer python-2.4 && \
     setup_version pycolumnize python-2.4 \
)
checkout_finish python-2.4-to-2.5
