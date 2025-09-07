#/bin/bash
# Setup for running Python 2.4 .. 2.7, merging python-3.0-to-3.2 into this branch
#!/bin/bash
PYTHON_VERSION=2.4

bs=${BASH_SOURCE[0]}
trepan_merge_24_owd=$(pwd)
mydir=$(dirname $bs)
cd $mydir/..
pyenv local $PYTHON_VERSION
cd $(dirname ${BASH_SOURCE[0]})
if . ./setup-python-2.4.sh; then
    git merge python-master
=======
if . ./admin-tools/setup-python-2.4.sh; then
    git merge master
>>>>>>> master
fi
cd $trepan_merge_24_owd
