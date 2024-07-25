#!/bin/bash
PYTHON_VERSION=2.4.6

if [[ $0 == $bs ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi

# FIXME put some of the below in a common routine
function finish {
  cd $setup_python24_owd
}

function checkout_version {
    local repo=$1
    version=${2:-python-2.4-to-2.7}
    echo Checking out $version on $repo ...
    (cd ../$repo && git checkout $version && pyenv local $PYTHON_VERSION) && \
	git pull
    return $?
}

trap finish EXIT
export PATH=$HOME/.pyenv/bin/pyenv:$PATH
set_python24_owd=$(pwd)
bs=${BASH_SOURCE[0]}
mydir=$(dirname $bs)
fulldir=$(readlink -f $mydir)
cd $fulldir/..
checkout_version python-spark python-2.4 && \
checkout_version python-filecache python-2.4-to-2.7 && \
checkout_version python-xdis python-2.4-to-2.7 && \
checkout_version python-uncompyle6 python-2.4-to-2.7 && \
git checkout python-2.4-to-2.5 && pyenv local $PYTHON_VERSION && git pull
remake -c clean_pyc
finish
