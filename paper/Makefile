PROJECT_NAME := hw4
REPO_ROOT := $(shell readlink -f ..)
SRC := $(shell find . -name '*.tex') homework.sty

LANDSCAPE_DEPS := $(shell find $(REPO_ROOT)/natural/landscape -name '*.py') $(REPO_ROOT)/scripts/landscape_figures.py
# Use a trigger file to avoid rebuilding the figures with every build.
LANDSCAPE_TRIGGER := .landscape-figures.trigger

.PHONY: all error view warn-todos clean clean-figures figures

all: $(PROJECT_NAME).pdf $(SRC)

$(PROJECT_NAME).pdf: figures
$(PROJECT_NAME).pdf: $(PROJECT_NAME).tex
	# latexmk -pdf --synctex=1 -file-line-error -interaction=nonstopmode -shell-escape $<
	latexmk -pdf --synctex=1 -file-line-error -interaction=batchmode -shell-escape $<
	@$(MAKE) warn-todos

# A target to build with better error messages when latexmk craps itself.
error:
	pdflatex -shell-escape -file-line-error $(PROJECT_NAME).tex
	@$(MAKE) warn-todos

view:
	1>/dev/null 2>/dev/null xdg-open $(PROJECT_NAME).pdf &

warn-todos:
	@BOLD=$$(tput bold);                                                                           \
	RED=$$(tput setaf 1);                                                                          \
	RESET=$$(tput sgr0);                                                                           \
	grep -irn --include "*.tex" --include "*.sty" "% TODO:" && echo "$${BOLD}$${RED}Warning:$${RESET}$${RED} TODO comment(s) found.$${RESET}"

clean: clean-figures
	latexmk -C
	rm -rf *.bbl *.tdo

clean-figures:
	rm $(LANDSCAPE_TRIGGER)
	rm -rf ./figures/landscapes/*

figures: $(LANDSCAPE_TRIGGER)
	@mkdir -p ./figures

$(LANDSCAPE_TRIGGER): $(LANDSCAPE_DEPS)
	touch $(LANDSCAPE_TRIGGER)
	BASEDIR=./figures/landscapes;                                                                  \
	mkdir -p "$${BASEDIR}";                                                                        \
	BASEDIR=$$(readlink -f ./figures/landscapes);                                                  \
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscape_figures.py $${BASEDIR}
