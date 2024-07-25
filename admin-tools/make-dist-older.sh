#!/bin/bash
PACKAGE=trepan2

# FIXME put some of the below in a common routine
function finish {
  cd $make_dist_older_owd
}
make_dist_older_owd=$(pwd)
trap finish EXIT

cd $(dirname ${BASH_SOURCE[0]})
if ! source ./pyenv-older-versions ; then
    exit $?
fi
if ! source ./setup-python-2.4.sh ; then
    exit $?
fi

cd ..
source trepan/version.py
echo $__version__

for pyversion in $PYVERSIONS; do
    if ! pyenv local $pyversion ; then
	exit $?
    fi

    rm -fr build
    python setup.py bdist_egg
done

# Pypi can only have one source tarball.
# Tarballs can get created from the above setup, so make sure to remove them since we want
# the tarball from master.

python ./setup.py sdist
tarball=dist/${PACKAGE}-$__version__.tar.gz
if [[ -f $tarball ]]; then
    mv -v $tarball dist/${PACKAGE}_24-$__version__.tar.gz
fi
finish
