#!/bin/bash
PYTHON_VERSION=2.4

if [[ $0 == $bs ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi

function checkout_version {
    local repo=$1
    version=${2:-python-2.4-to-2.7}
    echo Checking out $version on $repo ...
    (cd ../$repo && git checkout $version && pyenv local $PYTHON_VERSION) && \
	git pull
    return $?
}

export PATH=$HOME/.pyenv/bin/pyenv:$PATH
set_python24_owd=$(pwd)
bs=${BASH_SOURCE[0]}
mydir=$(dirname $bs)
cd $mydir/..
checkout_version python-spark python-2.4-to-2.7 && \
checkout_version python-filecache python-2.4-to-2.7 && \
checkout_version python-xdis python-2.4-to-2.7 && \
checkout_version shell-term-background python-2.4-to-2.7 && \
checkout_version python-uncompyle6 python-2.4-to-2.7 && \
git checkout python-2.4-to-2.5 && pyenv local $PYTHON_VERSION && git pull
remake -c clean_pyc
cd $set_python24_owd
