# Makefile for Sphinx documentation

# Next four are the source of truth - what is in pyproject.toml
# should agree with first two and one of the last two.
PROJECT_NAME = Gadgets
PYPI_NAME = gadgets
CURR_ROLLING_RELEASE_VERSION = 4.6.0
DEVEL_VERSION = 6.0.0
PREV_ROLLING_RELEASE_VERSION = 4.6.0

SPHINXOPTS ?=
SPHINXBUILD ?= sphinx-build
SOURCEDIR = source
BUILDDIR = build

# Put help first so that "make" without argument is like "make help"
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

clean_source:
	@rm -f "$(SOURCEDIR)"/conf.py

clean_prev_release:
	@rm -rf "$(BUILDDIR)"/prev_release

clean_curr_release:
	@rm -rf "$(BUILDDIR)"/curr_release

clean_devel:
	@rm -rf "$(BUILDDIR)"/devel

clean_index_html:
	@rm -f "$(BUILDDIR)"/index.html

clean: clean_prev_release clean_curr_release clean_devel clean_source clean_index_html
	@echo Removed all doc build artifacts.

setup_curr_release: clean_curr_release clean_index_html
	@./gen_conf.py curr_release "$(CURR_ROLLING_RELEASE_VERSION)" "$(PROJECT_NAME)" "$(PYPI_NAME)" > "$(SOURCEDIR)"/conf.py
	@echo Generating source/conf.py for current rolling release

setup_devel: clean_devel clean_index_html
	@./gen_conf.py devel "$(DEVEL_VERSION)" "$(PROJECT_NAME)" "$(PYPI_NAME)" > "$(SOURCEDIR)"/conf.py
	@echo Generating source/conf.py for devel

setup_prev_release: clean_prev_release clean_index_html
	@./gen_conf.py prev_release "$(PREV_ROLLING_RELEASE_VERSION)" "$(PROJECT_NAME)" "$(PYPI_NAME)" > "$(SOURCEDIR)"/conf.py
	@echo Generating source/conf.py for previous rolling release

$(BUILDDIR)/index.html: index.html.in Makefile
	@sed -e 's/@CURR_RELEASE@/$(CURR_ROLLING_RELEASE_VERSION)/g' \
	     -e 's/@DEVEL@/$(DEVEL_VERSION)/g' \
         -e 's/@PREV_RELEASE@/$(PREV_ROLLING_RELEASE_VERSION)/g' \
	     -e 's/@PROJECTNAME@/$(PROJECT_NAME)/g' \
	     -e 's/@PYPINAME@/$(PYPI_NAME)/g' \
	     $< > $@

# Build current rolling release labeled docs
curr_release: setup_curr_release $(BUILDDIR)/index.html
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)"/curr_release $(SPHINXOPTS)

# Build development labeled docs
devel: setup_devel $(BUILDDIR)/index.html
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)"/devel $(SPHINXOPTS)

# Build previous rolling release labeled docs
prev_release: setup_prev_release $(BUILDDIR)/index.html
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)"/prev_release $(SPHINXOPTS)

# Expose Makefile variables to scripts: make print-DEVEL_VERSION
print-%:
	@echo $($*)

.PHONY: help setup_prev_release setup_curr_release setup_devel devel release
.PHONY: prev_release curr_release devel
.PHONY: clean_source clean_release clean_release clean_devel clean_index_html clean

# Due to both builds needing to share the generated source/conf.py
.NOTPARALLEL:
