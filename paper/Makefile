PROJECT_NAME := hw4
REPO_ROOT := $(shell readlink -f ..)
SRC := $(shell find . -name '*.tex') homework.sty

LANDSCAPE_DIR := figures/landscapes
LANDSCAPE_DEPS := $(shell find $(REPO_ROOT)/natural/landscape -name '*.py') $(REPO_ROOT)/scripts/landscapes.py
# Use a trigger file to avoid rebuilding the figures with every build.
LANDSCAPE_TRIGGER := $(LANDSCAPE_DIR)/.landscape-figures.trigger

REACTION_DIR := figures/reactions
REACTION_DEPS := $(REPO_ROOT)/natural/automata/reaction_diffusion.py $(REPO_ROOT)/scripts/reaction.py
REACTION_TRIGGER := $(REACTION_DIR)/.reaction-figures.trigger
# TODO: Increase size and iterations after testing.
REACTION_SIZE := 128
REACTION_ITERS := 5000

HEAT_DIR := figures/heat
HEAT_DEPS := $(REPO_ROOT)/natural/automata/heat.py $(REPO_ROOT)/scripts/heat.py
HEAT_TRIGGER := $(HEAT_DIR)/.heat-figures.trigger

.PHONY: all error view warn-todos clean clean-figures cleanall figures _pre-reaction

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

clean:
	latexmk -C
	rm -rf *.bbl *.tdo

cleanall: clean
cleanall: clean-figures

clean-figures:
	rm $(LANDSCAPE_TRIGGER) $(REACTION_TRIGGER)
	rm $(LANDSCAPE_DIR)/*
	rm $(REACTION_DIR)/*.eps

figures: $(HEAT_TRIGGER)
figures: $(LANDSCAPE_TRIGGER)
figures: $(REACTION_TRIGGER)

$(HEAT_TRIGGER): diffusion-simple
$(HEAT_TRIGGER): diffusion-time
	touch $(HEAT_TRIGGER)

_pre-heat:
	mkdir -p $(HEAT_DIR)
	$(eval HEAT_DIR := $(shell readlink -f $(HEAT_DIR)))

diffusion-simple: _pre-heat
diffusion-simple: $(HEAT_DIR)/diffusion-simple.eps
diffusion-time: _pre-heat
diffusion-time: $(HEAT_DIR)/diffusion-time.eps

$(HEAT_DIR)/diffusion-simple.eps: $(HEAT_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/heat.py                                   \
		--prows 1                                                                                  \
		--pcols 1                                                                                  \
		--rows 100                                                                                 \
		--cols 100                                                                                 \
		--timestep 2000                                                                            \
		--output $(HEAT_DIR)/diffusion-simple.eps

$(HEAT_DIR)/diffusion-time.eps: $(HEAT_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/heat.py                                   \
		--prows 3                                                                                  \
		--pcols 3                                                                                  \
		--rows 100                                                                                 \
		--cols 100                                                                                 \
		--timestep 200                                                                             \
		--output $(HEAT_DIR)/diffusion-time.eps

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

_pre-reaction:
	mkdir -p $(REACTION_DIR)
	$(eval REACTION_DIR := $(shell readlink -f $(REACTION_DIR)))

$(REACTION_TRIGGER): alpha
$(REACTION_TRIGGER): beta
$(REACTION_TRIGGER): gamma
$(REACTION_TRIGGER): delta
$(REACTION_TRIGGER): epsilon
$(REACTION_TRIGGER): theta
$(REACTION_TRIGGER): kappa
$(REACTION_TRIGGER): lambda
$(REACTION_TRIGGER): mu
	touch $(REACTION_TRIGGER)

alpha: _pre-reaction
alpha: $(REACTION_DIR)/alpha.eps
beta: _pre-reaction
beta: $(REACTION_DIR)/beta.eps
gamma: _pre-reaction
gamma: $(REACTION_DIR)/gamma.eps
delta: _pre-reaction
delta: $(REACTION_DIR)/delta.eps
epsilon: _pre-reaction
epsilon: $(REACTION_DIR)/epsilon.eps
theta: _pre-reaction
theta: $(REACTION_DIR)/theta.eps
kappa: _pre-reaction
kappa: $(REACTION_DIR)/kappa.eps
lambda: _pre-reaction
lambda: $(REACTION_DIR)/lambda.eps
mu: _pre-reaction
mu: $(REACTION_DIR)/mu.eps
eta: _pre-reaction
eta: $(REACTION_DIR)/eta.eps

$(REACTION_DIR)/alpha.eps: $(REACTION_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/reaction.py                               \
		--iterations $(REACTION_ITERS)                                                             \
		--kill 0.05                                                                                \
		--feed 0.017                                                                               \
		--radius 5                                                                                 \
		--size $(REACTION_SIZE)                                                                    \
		--title "Pattern $$\\alpha$$"                                                              \
		--output $(REACTION_DIR)/alpha.eps

$(REACTION_DIR)/beta.eps: $(REACTION_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/reaction.py                               \
		--iterations $(REACTION_ITERS)                                                             \
		--kill 0.045                                                                               \
		--feed 0.019                                                                               \
		--radius 2                                                                                 \
		--size $(REACTION_SIZE)                                                                    \
		--title "Pattern $$\\beta$$"                                                               \
		--output $(REACTION_DIR)/beta.eps

$(REACTION_DIR)/gamma.eps: $(REACTION_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/reaction.py                               \
		--iterations $(REACTION_ITERS)                                                             \
		--kill 0.052                                                                               \
		--feed 0.021                                                                               \
		--radius 5                                                                                 \
		--size $(REACTION_SIZE)                                                                    \
		--title "Pattern $$\\gamma$$"                                                              \
		--output $(REACTION_DIR)/gamma.eps

$(REACTION_DIR)/delta.eps: $(REACTION_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/reaction.py                               \
		--iterations $(REACTION_ITERS)                                                             \
		--kill 0.052                                                                               \
		--feed 0.026                                                                               \
		--radius 5                                                                                 \
		--size $(REACTION_SIZE)                                                                    \
		--title "Pattern $$\\delta$$"                                                              \
		--output $(REACTION_DIR)/delta.eps

$(REACTION_DIR)/epsilon.eps: $(REACTION_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/reaction.py                               \
		--iterations $(REACTION_ITERS)                                                             \
		--kill 0.052                                                                               \
		--feed 0.017                                                                               \
		--radius 2                                                                                 \
		--size $(REACTION_SIZE)                                                                    \
		--title "Pattern $$\\epsilon$$"                                                            \
		--output $(REACTION_DIR)/epsilon.eps

$(REACTION_DIR)/theta.eps: $(REACTION_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/reaction.py                               \
		--iterations $(REACTION_ITERS)                                                             \
		--kill 0.06                                                                                \
		--feed 0.04                                                                                \
		--radius 2                                                                                 \
		--scale 0.2                                                                                \
		--size $(REACTION_SIZE)                                                                    \
		--title "Pattern $$\\theta$$"                                                              \
		--output $(REACTION_DIR)/theta.eps

$(REACTION_DIR)/kappa.eps: $(REACTION_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/reaction.py                               \
		--iterations $(REACTION_ITERS)                                                             \
		--kill 0.064                                                                               \
		--feed 0.05                                                                                \
		--radius 5                                                                                 \
		--scale 0.2                                                                                \
		--size $(REACTION_SIZE)                                                                    \
		--title "Pattern $$\\kappa$$"                                                              \
		--output $(REACTION_DIR)/kappa.eps

# TODO: Fix lambda
$(REACTION_DIR)/lambda.eps: $(REACTION_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/reaction.py                               \
		--iterations $(REACTION_ITERS)                                                             \
		--kill 0.066                                                                               \
		--feed 0.04                                                                                \
		--radius 5                                                                                 \
		--size $(REACTION_SIZE)                                                                    \
		--title "Pattern $$\\lambda$$"                                                             \
		--output $(REACTION_DIR)/lambda.eps

# TODO: Fix mu
$(REACTION_DIR)/mu.eps: $(REACTION_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/reaction.py                               \
		--iterations $(REACTION_ITERS)                                                             \
		--kill 0.0655                                                                              \
		--feed 0.0565                                                                              \
		--radius 2                                                                                 \
		--scale 0.2                                                                                \
		--size $(REACTION_SIZE)                                                                    \
		--title "Pattern $$\\mu$$"                                                                 \
		--output $(REACTION_DIR)/mu.eps

# TODO: Add zeta, and iota
$(REACTION_DIR)/eta.eps: $(REACTION_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/reaction.py                               \
		--iterations $(REACTION_ITERS)                                                             \
		--kill 0.06                                                                                \
		--feed 0.028                                                                               \
		--radius 2                                                                                 \
		--scale 0.1                                                                                \
		--size $(REACTION_SIZE)                                                                    \
		--title "Pattern $$\\eta$$"                                                                \
		--output $(REACTION_DIR)/eta.eps
