#!/bin/bash
PYTHON_VERSION=2.7.18

# FIXME put some of the below in a common routine
function finish {
  cd $owd
}

function checkout_version {
    local repo=$1
    local branch=${2:-python-2.4}
    echo Checking out $branch on $repo ...
    (cd ../$repo && git checkout $branch && pyenv local $PYTHON_VERSION) && \
	git pull
    return $?
}

export PATH=$HOME/.pyenv/bin/pyenv:$PATH
owd=$(pwd)
bs=${BASH_SOURCE[0]}
mydir=$(dirname $bs)
fulldir=$(readlink -f $mydir)
cd $fulldir/..
checkout_version python-spark  && \
checkout_version python-filecache python-2.4-to-2.7 && \
checkout_version python-xdis python-2.4-to-2.7 && \
checkout_version python-uncompyle6 && \
git checkout master && pyenv local $PYTHON_VERSION && git pull
cd $owd
