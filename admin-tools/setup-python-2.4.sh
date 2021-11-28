#!/bin/bash
PYTHON_VERSION=2.4.6

function checkout_version {
    local repo=$1
    echo Checking out python-2.4 on $repo ...
    (cd ../$repo && git checkout python-2.4 && pyenv local $PYTHON_VERSION) && \
	git pull
    return $?
}

export PATH=$HOME/.pyenv/bin/pyenv:$PATH
owd=$(pwd)
bs=${BASH_SOURCE[0]}
if [[ $0 == $bs ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi
mydir=$(dirname $bs)
fulldir=$(readlink -f $mydir)
(cd $fulldir/.. &&  checkout_version python-spark &&  checkout_version python-filecache &&
 checkout_version python-xdis && checkout_version python-uncompyle6)
cd $owd
git checkout python-2.4 &&  pyenv local $PYTHON_VERSION && git pull
