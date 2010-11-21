# Compatibility for us old-timers.
EXTRA_DIST=ipython/ipy_pydbgr.py pydbgr version.m4.in
PHONY=check clean dist distclean test test-unit test-functional
all: check

test: check

# check: test-unit test-functional test-integration
check: test-unit test-functional test-integration

test-unit: 
	python ./setup.py nosetests

test-functional: 
	(cd test/functional && python ./setup.py nosetests)

test-integration: 
	(cd test/integration && python ./setup.py nosetests)

clean: 
	python ./setup.py $@

dist-python: 
	python ./setup.py sdist bdist

# Make sure we never package up '.svn' directories
dist-hook:
	find $(distdir) -name '.svn'  | xargs rm -rf
	find $(distdir) -path '*.pyc' | xargs rm -rf

# It is too much work to figure out how to add a new command to distutils
# to do the following. I'm sure distutils will someday get there.
DISTCLEAN_FILES = build dist *.egg-info *.pyc
distclean: clean
	-rm -fr $(DISTCLEAN_FILES) || true
	-find . -name \*.pyc -exec rm -v {} \;
install: 
	python ./setup.py install

ChangeLog:
	svn2cl --authors=svn2cl_usermap http://pydbgr.googlecode.com/svn/trunk -o $@

.PHONY: $(PHONY)
