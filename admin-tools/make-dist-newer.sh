#!/bin/bash
PACKAGE=trepan2

# FIXME put some of the below in a common routine
function make_dist_finish {
  cd $make_dist_trepan2_owd
}

make_dist_trepan2_owd=$(pwd)
trap finish EXIT
cd $(dirname ${BASH_SOURCE[0]})

if ! source ./pyenv-newer-versions ; then
    exit $?
fi
if ! source ./setup-master.sh ; then
    exit $?
fi

cd ..
source trepan/version.py
if [[ ! -n $__version__ ]]; then
    echo "You need to set __version__ first"
    exit 1
fi
echo $__version__

for pyversion in $PYVERSIONS; do
    if ! pyenv local $pyversion ; then
	exit $?
    fi
    # pip bdist_egg create too-general wheels. So
    # we narrow that by moving the generated wheel.

    # Pick out first two number of version, e.g. 3.5.1 -> 35
    first_two=$(echo $pyversion | cut -d'.' -f 1-2 | sed -e 's/\.//')
    rm -fr build
    python setup.py bdist_egg bdist_wheel
    if [[ $first_two =~ py* ]]; then
	if [[ $first_two =~ pypy* ]]; then
	    # For PyPy, remove the what is after the dash, e.g. pypy37-none-any.whl instead of pypy37-7-none-any.whl
	    first_two=${first_two%-*}
	fi
	mv -v dist/${PACKAGE}-$__version__-{py3,$first_two}-none-any.whl
    else
	mv -v dist/${PACKAGE}-$__version__-{py3,py$first_two}-none-any.whl
    fi
done

python ./setup.py sdist
make_dist_finish
