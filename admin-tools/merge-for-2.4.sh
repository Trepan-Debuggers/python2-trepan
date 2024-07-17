#/bin/bash
# Setup for running Python 2.4 .. 2.7, merging python-3.0-to-3.2 into this branch
trepan2_24_owd=$(pwd)
cd $(dirname ${BASH_SOURCE[0]})
(cd .. && PYTHON_VERSION=2.4 && pyenv local $PYTHON_VERSION)
if . ./setup-python-2.4.sh; then
    git merge master
fi
cd $trepan2_24_owd
