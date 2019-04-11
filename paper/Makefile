PROJECT_NAME := hw4
REPO_ROOT := $(shell readlink -f ..)
SRC := $(shell find . -name '*.tex') homework.sty

LANDSCAPE_DIR := figures/landscapes
LANDSCAPE_DEPS := $(shell find $(REPO_ROOT)/natural/landscape -name '*.py') $(REPO_ROOT)/scripts/landscapes.py
# Use a trigger file to avoid rebuilding the figures with every build.
LANDSCAPE_TRIGGER := $(LANDSCAPE_DIR)/.landscape-figures.trigger

.PHONY: all error view warn-todos clean clean-figures figures

all: $(PROJECT_NAME).pdf $(SRC)

$(PROJECT_NAME).pdf: figures
$(PROJECT_NAME).pdf: $(PROJECT_NAME).tex
	# latexmk -pdf --synctex=1 -file-line-error -interaction=nonstopmode -shell-escape $<
	latexmk -pdf --synctex=1 -file-line-error -interaction=batchmode -shell-escape $<
	@$(MAKE) --no-print-directory warn-todos

# A target to build with better error messages when latexmk craps itself.
error:
	pdflatex -shell-escape -file-line-error $(PROJECT_NAME).tex
	@$(MAKE) --no-print-directory warn-todos

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
	mkdir -p $(LANDSCAPE_DIR)
	touch $(LANDSCAPE_TRIGGER)
	$(eval LANDSCAPE_DIR := $(shell readlink -f $(LANDSCAPE_DIR)))
	@# Start all the jobs in parallel the poor man's way, fully aware there's a better way (tm).
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscapes.py                             \
		--one                                                                                      \
		--recursions 4                                                                             \
		--scale 2                                                                                  \
		--hurst 0.5                                                                                \
		--seed 3                                                                                   \
		--output $(LANDSCAPE_DIR)/1d-4-2-0_5-3.eps                                               & \
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscapes.py                             \
		--one                                                                                      \
		--recursions 10                                                                            \
		--scale 2                                                                                  \
		--hurst 0.5                                                                                \
		--seed 37                                                                                  \
		--output $(LANDSCAPE_DIR)/1d-10-2-0_5-37.eps                                             & \
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscapes.py                             \
		--one                                                                                      \
		--recursions 4 6 8 10                                                                      \
		--scale 2                                                                                  \
		--hurst 0.5                                                                                \
		--seed 420                                                                                 \
		--output $(LANDSCAPE_DIR)/1d-nrc-2-0_5-420.eps                                           & \
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscapes.py                             \
		--one                                                                                      \
		--recursions 5                                                                             \
		--scale 0.5 1 2 4                                                                          \
		--hurst 0.5                                                                                \
		--seed 420                                                                                 \
		--output $(LANDSCAPE_DIR)/1d-5-scale-0_5-420.eps                                         & \
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscapes.py                             \
		--one                                                                                      \
		--recursions 5                                                                             \
		--scale 2                                                                                  \
		--hurst 0.1 0.3 0.5 0.7 0.9                                                                \
		--seed 420                                                                                 \
		--output $(LANDSCAPE_DIR)/1d-5-2-hurst-420.eps                                           & \
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscapes.py                             \
		--recursions 4                                                                             \
		--scale 1                                                                                  \
		--hurst 0.5                                                                                \
		--seed 3                                                                                   \
		--output $(LANDSCAPE_DIR)/2d-4-1-0_5-3.eps                                               & \
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscapes.py                             \
		--recursions 4                                                                             \
		--scale 1                                                                                  \
		--hurst 0.7                                                                                \
		--seed 9                                                                                   \
		--output $(LANDSCAPE_DIR)/2d-4-1-0_7-9.eps                                               & \
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscapes.py                             \
		--recursions 4                                                                             \
		--scale 1                                                                                  \
		--hurst 0.7                                                                                \
		--seed 9                                                                                   \
		--sealevel -0.8                                                                            \
		--output $(LANDSCAPE_DIR)/2d-4-1-0_7-9-sealevel.eps                                      & \
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscapes.py                             \
		--recursions 6                                                                             \
		--scale 1                                                                                  \
		--hurst 0.7                                                                                \
		--seed 5                                                                                   \
		--output $(LANDSCAPE_DIR)/2d-6-1-0_7-5.eps                                               & \
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscapes.py                             \
		--recursions 6                                                                             \
		--scale 1                                                                                  \
		--hurst 0.7                                                                                \
		--seed 5                                                                                   \
		--sealevel 0                                                                               \
		--output $(LANDSCAPE_DIR)/2d-6-1-0_7-5-sealevel.eps                                      & \
	wait
