# Makefile for Sphinx documentation
PROJECT_NAME = Gadgets
PYPI_NAME = gadgets

# last PyPI release - needs to agree with last release on PyPI
RELEASE_VERSION = 4.6.0
# future PyPI release - needs to agree with what is in pyproject.toml
DEVEL_VERSION = 6.0.0

SPHINXOPTS ?=
SPHINXBUILD ?= sphinx-build
SOURCEDIR = source
BUILDDIR = build

# Put help first so that "make" without argument is like "make help"
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

clean_source:
	@rm -f "$(SOURCEDIR)"/conf.py

clean_devel:
	@rm -rf "$(BUILDDIR)"/development

clean_release:
	@rm -rf "$(BUILDDIR)"/release

clean_index_html:
	@rm -f "$(BUILDDIR)"/index.html

clean: clean_devel clean_release clean_source clean_index_html
	@echo Removed all doc build artifacts.

setup_devel: clean_devel clean_index_html
	@./gen_conf.py devel "$(DEVEL_VERSION)" "$(PROJECT_NAME)" "$(PYPI_NAME)" > "$(SOURCEDIR)"/conf.py
	@echo Generating source/conf.py for devel

setup_release: clean_release clean_index_html
	@./gen_conf.py release "$(RELEASE_VERSION)" "$(PROJECT_NAME)" "$(PYPI_NAME)" > "$(SOURCEDIR)"/conf.py
	@echo Generating source/conf.py for release

$(BUILDDIR)/index.html: index.html.in Makefile
	@sed -e 's/@RELEASE@/$(RELEASE_VERSION)/g' \
	     -e 's/@DEVEL@/$(DEVEL_VERSION)/g' \
	     $< > $@

# Build development labeled docs
devel: setup_devel $(BUILDDIR)/index.html
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)"/development $(SPHINXOPTS)

# Build release labeled docs
release: setup_release $(BUILDDIR)/index.html
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)"/release $(SPHINXOPTS)


# Expose Makefile variables to scripts: make print-RELEASE_VERSION
print-%:
	@echo $($*)

.PHONY: help setup_devel setup_release devel release
.PHONY: clean_source clean_devel clean_release clean_index_html clean

# Due to both builds needing to share the generated source/conf.py
.NOTPARALLEL:
