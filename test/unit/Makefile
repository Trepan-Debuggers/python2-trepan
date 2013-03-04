PYTHON ?= python

PHONY=all check check-short test-unit test-unit-short

#: Same as test-unit
all: 
	$(MAKE) test-unit

#: Same as test-unit
check: 
	$(MAKE) test-unit

#: Same as test-unit-short
check-short:
	$(MAKE) test-unit-short

#: Run unit tests reduced verbosity
test-unit-short: 
	$(PYTHON) ../../setup.py nosetests | \
	$(PYTHON) ../../make-check-filter.py

#: Remove derived files
clean: 
	-rm -fr *.egg-info || true

# Whatever else it is you want to do, it should be forwarded to the 
# to top-level directories
%: 
	$(MAKE) -C ../.. $@
