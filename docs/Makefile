# Makefile for Sphinx documentation

# Next four are the source of truth - what is in pyproject.toml
# should agree with first two and one of the last two.
PROJECT_NAME = Gadgets
PYPI_NAME = gadgets
CURR_RELEASE_VERSION = 6.0.0
DEVEL_VERSION = 6.0.0
PREV_RELEASE_VERSION = 4.6.0

SPHINXOPTS ?=
SPHINXBUILD ?= sphinx-build

# Give build info if "make" without arguments is given
help:
	@echo To build docs: uv run make {devel | curr_release | prev_release}

clean_source:
	@rm -f source/conf.py

clean_prev_release:
	@rm -rf build/prev_release

clean_curr_release:
	@rm -rf build/curr_release

clean_devel:
	@rm -rf devel

clean_index_html:
	@rm -f build/index.html

clean: clean_prev_release clean_curr_release clean_devel clean_source clean_index_html
	@echo Removed all doc build artifacts.

setup_devel: clean_devel clean_index_html
	@mkdir -p devel
	@python3 gen_conf.py devel "$(DEVEL_VERSION)" "$(PROJECT_NAME)" "$(PYPI_NAME)" > source/conf.py
	@echo Generating source/conf.py for devel

setup_curr_release: clean_curr_release clean_index_html
	@mkdir -p build/curr_release
	@python3 gen_conf.py curr_release "$(CURR_RELEASE_VERSION)" "$(PROJECT_NAME)" "$(PYPI_NAME)" > source/conf.py
	@echo Generating source/conf.py for current release

setup_prev_release: clean_prev_release clean_index_html
	@mkdir -p build/prev_release
	@python3 gen_conf.py prev_release "$(PREV_ROLLING_RELEASE_VERSION)" "$(PROJECT_NAME)" "$(PYPI_NAME)" > source/conf.py
	@sed -e 's/@CURR_RELEASE@/$(CURR_RELEASE_VERSION)/g'
	@echo Generating source/conf.py for previous release

build/index.html: index.html.in Makefile
	@mkdir -p build
	@sed
		-e 's/@DEVEL@/$(DEVEL_VERSION)/g' \
		-e 's/@CURR_RELEASE@/$(CURR_RELEASE_VERSION)/g' \
		-e 's/@DEVEL@/$(DEVEL_VERSION)/g' \
		-e 's/@PREV_RELEASE@/$(PREV_RELEASE_VERSION)/g' \
		-e 's/@PROJECTNAME@/$(PROJECT_NAME)/g' \
		-e 's/@PYPINAME@/$(PYPI_NAME)/g' \
		$< > $@

# Build current release labeled docs
curr_release: setup_curr_release build/index.html
	@$(SPHINXBUILD) -b html source build/curr_release $(SPHINXOPTS)

# Build previous release labeled docs
prev_release: setup_prev_release build/index.html
	@$(SPHINXBUILD) -b html source build/prev_release $(SPHINXOPTS)

# Build development labeled docs
devel: setup_devel
	@$(SPHINXBUILD) -b html source devel $(SPHINXOPTS)

# Expose Makefile variables to scripts: make print-DEVEL_VERSION
print-%:
	@echo $($*)

.PHONY: help clean clean_source clean_index_html
.PHONY: clean_prev_release clean_curr_release clean_devel
.PHONY: setup_prev_release setup_curr_release setup_devel
.PHONY: curr_release prev_release devel

# Due to both builds needing to share the generated source/conf.py
.NOTPARALLEL:
