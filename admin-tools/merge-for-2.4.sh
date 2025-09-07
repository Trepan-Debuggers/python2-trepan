#/bin/bash
# Setup for running Python 2.4 .. 2.7, merging python-3.0-to-3.2 into this branch
#!/bin/bash
PYTHON_VERSION=2.4

bs=${BASH_SOURCE[0]}
if [[ $0 == $bs ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi

mydir=$(dirname $bs)
trepan2_owd=$(pwd)/
cd $mydir
. ./checkout_common.sh

(cd $mydir/../../../rocky  && \
     setup_version python-uncompyle6 python-2.4 && \
     setup_version python-xdis python-2.4 && \
     setup_version python-filecache python-2.4 && \
     setup_version shell-term-background python-2.4 && \
     setup_version pytracer python-2.4 && \
     setup_version pycolumnize python-2.4 \
)
checkout_finish master
