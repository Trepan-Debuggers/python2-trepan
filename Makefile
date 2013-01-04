# Compatibility for us old-timers.
EXTRA_DIST=ipython/ipy_pydbgr.py pydbgr
PHONY=check clean dist distclean test test-unit test-functional

#: Default target - same as "check"
all: check

#: Same as "check" 
test: check

#: Run all tests: unit, functional and integration
check: test-unit test-functional test-integration

#: Run unit (white-box) tests
test-unit: 
	$(PYTHON) ./setup.py nosetests

#: Run functional tests
test-functional: 
	(cd test/functional && $(PYTHON) ./setup.py nosetests)

#: Run integration (black-box) tests
test-integration: 
	(cd test/integration && $(PYTHON) ./setup.py nosetests)

#: Clean up temporary files
clean: 
	$(PYTHON) ./setup.py $@

dist-python: 
	$(PYTHON) ./setup.py sdist bdist

# It is too much work to figure out how to add a new command to distutils
# to do the following. I'm sure distutils will someday get there.
DISTCLEAN_FILES = build dist *.egg-info *.pyc

#: Remove ALL dervied files 
distclean: clean
	-rm -fr $(DISTCLEAN_FILES) || true
	-find . -name \*.pyc -exec rm -v {} \;

#: Install package locally
install: 
	$(PYTHON) ./setup.py install

#: Create a ChangeLog from git via git log and git2cl
ChangeLog:
	git log --pretty --numstat --summary | $(GIT2CL) >$@

.PHONY: $(PHONY)
