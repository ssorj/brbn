.PHONY: default help clean build install devel

DESTDIR := ""
PREFIX := /usr/local

default: devel

help:
	@echo "clean          Clean up the source tree"
	@echo "build          Build the code"
	@echo "install        Install the code"
	@echo "test           Run tests"
	@echo "devel          Clean, build, install, test"

clean:
	find python -type f -name \*.pyc -delete
	rm -rf python/__pycache__
	rm -rf build
	rm -rf install

build:
	mkdir -p build/bin
	scripts/configure-file bin/brbn.in build/bin/brbn brbn_home ${PREFIX}/share/brbn
	chmod 755 build/bin/brbn

install: home = ${DESTDIR}${PREFIX}/share/brbn
install: build
	scripts/install-files python ${home}/python \*.py
	scripts/install-files files ${home}/files \*
	scripts/install-files build/bin ${DESTDIR}${PREFIX}/bin \*

test: install

devel: PREFIX := ${PWD}/install
devel: clean test
	PATH=${PREFIX}/bin:${PATH} brbn
