DESTDIR := ""
PREFIX := ${HOME}/.local
BRBN_HOME = ${PREFIX}/share/brbn

.PHONY: default
default: devel

.PHONY: help
help:
	@echo "clean          Clean up the source tree"
	@echo "build          Build the code"
	@echo "install        Install the code"
	@echo "test           Run tests"
	@echo "devel          Clean, build, install, test"

.PHONY: clean
clean:
	find python -type f -name \*.pyc -delete
	find python -type d -name __pycache__ -delete
	rm -rf build
	rm -rf install

.PHONY: build
build:
	mkdir -p build/bin
	scripts/configure-file -a brbn_home=${BRBN_HOME} bin/brbn.in build/bin/brbn

.PHONY: install
install: build
	scripts/install-files -n \*.py python ${DESTDIR}${BRBN_HOME}/python
	scripts/install-files files ${DESTDIR}${BRBN_HOME}/files
	scripts/install-files build/bin ${DESTDIR}${PREFIX}/bin

.PHONY: test
test: PREFIX := ${PWD}/install
test: clean install
	${PREFIX}/bin/brbn --init-only

.PHONY: devel
devel: PREFIX := ${PWD}/install
devel: clean install
	${PREFIX}/bin/brbn

.PHONY: update-spindle
update-spindle:
	curl "https://raw.githubusercontent.com/ssorj/spindle/master/spindle.py" -o python/spindle.py
