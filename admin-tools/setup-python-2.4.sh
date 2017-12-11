#!/bin/bash
PYTHON_VERSION=2.4.6

function checkout_version {
    local repo=$1
    version=${2:-python-2.4}
    echo Checking out $version.4 on $repo ...
    (cd ../$repo && git checkout $version && pyenv local $PYTHON_VERSION) && \
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
cd $fulldir/..
(cd ../python-spark && git checkout python-2.4 && pyenv local $PYTHON_VERSION) && git pull && \
    (cd ../python-filecache && git checkout python-2.4) && \
    (cd ../python-xdis && git checkout python-2.4 && pyenv local $PYTHON_VERSION) && git pull && \
    (cd ../python-uncompyle6 && git checkout python-2.4 && pyenv local $PYTHON_VERSION) && git pull && \
    git checkout python-2.4 &&  pyenv local $PYTHON_VERSION && git pull
cd $owd
git checkout python-2.4 &&  pyenv local $PYTHON_VERSION && git pull
