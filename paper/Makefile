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
REACTION_SIZE := 256
REACTION_ITERS := 10000

HEAT_DIR := figures/heat
HEAT_DEPS := $(REPO_ROOT)/natural/automata/heat.py $(REPO_ROOT)/scripts/heat.py
HEAT_TRIGGER := $(HEAT_DIR)/.heat-figures.trigger

.PHONY: all error view warn-todos clean clean-figures cleanall figures _pre-reaction

all: $(PROJECT_NAME).pdf $(SRC)

$(PROJECT_NAME).pdf: figures
$(PROJECT_NAME).pdf: $(PROJECT_NAME).tex
	# latexmk -pdf --synctex=1 -file-line-error -interaction=batchmode -shell-escape $<
	latexmk -pdf --synctex=1 -file-line-error -interaction=nonstopmode -shell-escape $<
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
	grep -irn --include "*.tex" --include "*.sty" "% TODO:" && echo "$${BOLD}$${RED}Warning:$${RESET}$${RED} TODO comment(s) found.$${RESET}" || true

clean:
	latexmk -C
	rm -rf *.bbl *.tdo
	rm -rf _minted-$(PROJECT_NAME)

cleanall: clean
cleanall: clean-figures

clean-figures:
	rm -f $(LANDSCAPE_TRIGGER) $(REACTION_TRIGGER) $(HEAT_TRIGGER)
	rm -f $(LANDSCAPE_DIR)/*
	rm -f $(REACTION_DIR)/*.eps
	rm -f $(REACTION_DIR)/*.pdf
	rm -f $(HEAT_DIR)/*

figures: heat
figures: landscapes
figures: reactions

heat: $(HEAT_TRIGGER)
landscapes: $(LANDSCAPE_TRIGGER)
reactions: $(REACTION_TRIGGER)

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

$(LANDSCAPE_TRIGGER): landscape-1d
$(LANDSCAPE_TRIGGER): landscape-2d-hurst
$(LANDSCAPE_TRIGGER): landscape-2d-sealevel
	touch $(LANDSCAPE_TRIGGER)

_pre-landscape:
	mkdir -p $(LANDSCAPE_DIR)
	$(eval LANDSCAPE_DIR := $(shell readlink -f $(LANDSCAPE_DIR)))

landscape-1d: _pre-landscape
landscape-1d: $(LANDSCAPE_DIR)/1d.eps
landscape-1d: $(LANDSCAPE_DIR)/1d-num-recursions.eps
landscape-1d: $(LANDSCAPE_DIR)/1d-scale.eps
landscape-1d: $(LANDSCAPE_DIR)/1d-hurst-exponent.eps
landscape-2d-hurst: _pre-landscape
landscape-2d-hurst: $(LANDSCAPE_DIR)/2d-hurst-1.eps
landscape-2d-hurst: $(LANDSCAPE_DIR)/2d-hurst-6.eps
landscape-2d-hurst: $(LANDSCAPE_DIR)/2d-hurst-7.eps
landscape-2d-hurst: $(LANDSCAPE_DIR)/2d-hurst-8.eps
landscape-2d-hurst: $(LANDSCAPE_DIR)/2d-hurst-9.eps
landscape-2d-sealevel: _pre-landscape
landscape-2d-sealevel: $(LANDSCAPE_DIR)/2d-sealevel-1.eps
landscape-2d-sealevel: $(LANDSCAPE_DIR)/2d-sealevel-2.eps

$(LANDSCAPE_DIR)/1d.eps: $(LANDSCAPE_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscapes.py                             \
		--one                                                                                      \
		--recursions 10                                                                            \
		--scale 2                                                                                  \
		--hurst 0.5                                                                                \
		--seed 37                                                                                  \
		--output $(LANDSCAPE_DIR)/1d.eps

$(LANDSCAPE_DIR)/1d-num-recursions.eps: $(LANDSCAPE_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscapes.py                             \
		--one                                                                                      \
		--recursions 4 6 8 10                                                                      \
		--scale 2                                                                                  \
		--hurst 0.5                                                                                \
		--seed 420                                                                                 \
		--output $(LANDSCAPE_DIR)/1d-num-recursions.eps

$(LANDSCAPE_DIR)/1d-scale.eps: $(LANDSCAPE_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscapes.py                             \
		--one                                                                                      \
		--recursions 5                                                                             \
		--scale 0.5 1 2 4                                                                          \
		--hurst 0.5                                                                                \
		--seed 420                                                                                 \
		--output $(LANDSCAPE_DIR)/1d-scale.eps

$(LANDSCAPE_DIR)/1d-hurst-exponent.eps: $(LANDSCAPE_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscapes.py                             \
		--one                                                                                      \
		--recursions 5                                                                             \
		--scale 2                                                                                  \
		--hurst 0.1 0.3 0.5 0.7 0.9                                                                \
		--seed 420                                                                                 \
		--output $(LANDSCAPE_DIR)/1d-hurst-exponent.eps

$(LANDSCAPE_DIR)/2d-hurst-1.eps: $(LANDSCAPE_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscapes.py                             \
		--recursions 6                                                                             \
		--scale 1                                                                                  \
		--hurst 1                                                                                  \
		--seed 3188393957                                                                          \
		--output $(LANDSCAPE_DIR)/2d-hurst-1.eps

$(LANDSCAPE_DIR)/2d-hurst-6.eps: $(LANDSCAPE_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscapes.py                             \
		--recursions 6                                                                             \
		--scale 1                                                                                  \
		--hurst 0.6                                                                                \
		--seed 3188393957                                                                          \
		--output $(LANDSCAPE_DIR)/2d-hurst-6.eps

$(LANDSCAPE_DIR)/2d-hurst-7.eps: $(LANDSCAPE_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscapes.py                             \
		--recursions 6                                                                             \
		--scale 1                                                                                  \
		--hurst 0.7                                                                                \
		--seed 3188393957                                                                          \
		--output $(LANDSCAPE_DIR)/2d-hurst-7.eps

$(LANDSCAPE_DIR)/2d-hurst-8.eps: $(LANDSCAPE_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscapes.py                             \
		--recursions 6                                                                             \
		--scale 1                                                                                  \
		--hurst 0.8                                                                                \
		--seed 3188393957                                                                          \
		--output $(LANDSCAPE_DIR)/2d-hurst-8.eps

$(LANDSCAPE_DIR)/2d-hurst-9.eps: $(LANDSCAPE_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscapes.py                             \
		--recursions 6                                                                             \
		--scale 1                                                                                  \
		--hurst 0.9                                                                                \
		--seed 3188393957                                                                          \
		--output $(LANDSCAPE_DIR)/2d-hurst-9.eps

# 4212677775 is similar
$(LANDSCAPE_DIR)/2d-sealevel-1.eps: $(LANDSCAPE_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscapes.py                             \
		--recursions 6                                                                             \
		--scale 1                                                                                  \
		--hurst 0.9                                                                                \
		--seed 68230869                                                                            \
		--sealevel -1                                                                              \
		--output $(LANDSCAPE_DIR)/2d-sealevel-1.eps

$(LANDSCAPE_DIR)/2d-sealevel-2.eps: $(LANDSCAPE_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/landscapes.py                             \
		--recursions 6                                                                             \
		--scale 1                                                                                  \
		--hurst 0.9                                                                                \
		--seed 4175779808                                                                          \
		--sealevel -0.7                                                                            \
		--output $(LANDSCAPE_DIR)/2d-sealevel-2.eps

_pre-reaction:
	mkdir -p $(REACTION_DIR)
	$(eval REACTION_DIR := $(shell readlink -f $(REACTION_DIR)))

$(REACTION_TRIGGER): alpha
$(REACTION_TRIGGER): beta
$(REACTION_TRIGGER): gamma
$(REACTION_TRIGGER): delta
$(REACTION_TRIGGER): epsilon
$(REACTION_TRIGGER): zeta
$(REACTION_TRIGGER): eta
$(REACTION_TRIGGER): theta
$(REACTION_TRIGGER): iota
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
zeta: _pre-reaction
zeta: $(REACTION_DIR)/zeta.eps
eta: _pre-reaction
eta: $(REACTION_DIR)/eta.eps
theta: _pre-reaction
theta: $(REACTION_DIR)/theta.eps
iota: _pre-reaction
iota: $(REACTION_DIR)/iota.eps
kappa: _pre-reaction
kappa: $(REACTION_DIR)/kappa.eps
lambda: _pre-reaction
lambda: $(REACTION_DIR)/lambda.eps
mu: _pre-reaction
mu: $(REACTION_DIR)/mu.eps

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
		--iterations $(shell expr $(REACTION_ITERS) \* 2 )                                         \
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

$(REACTION_DIR)/zeta.eps: $(REACTION_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/reaction.py                               \
		--iterations $(REACTION_ITERS)                                                             \
		--kill 0.06                                                                                \
		--feed 0.023                                                                               \
		--radius 2                                                                                 \
		--scale 0.1                                                                                \
		--size $(REACTION_SIZE)                                                                    \
		--title "Pattern $$\\zeta$$"                                                               \
		--output $(REACTION_DIR)/zeta.eps

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

$(REACTION_DIR)/theta.eps: $(REACTION_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/reaction.py                               \
		--iterations $(REACTION_ITERS)                                                             \
		--kill 0.06                                                                                \
		--feed 0.04                                                                                \
		--radius 2                                                                                 \
		--scale 0.1                                                                                \
		--size $(REACTION_SIZE)                                                                    \
		--title "Pattern $$\\theta$$"                                                              \
		--output $(REACTION_DIR)/theta.eps

$(REACTION_DIR)/iota.eps: $(REACTION_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/reaction.py                               \
		--iterations $(REACTION_ITERS)                                                             \
		--kill 0.06                                                                                \
		--feed 0.054                                                                               \
		--radius 2                                                                                 \
		--scale 0.2                                                                                \
		--size $(REACTION_SIZE)                                                                    \
		--title "Pattern $$\\iota$$"                                                               \
		--output $(REACTION_DIR)/iota.eps

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

$(REACTION_DIR)/lambda.eps: $(REACTION_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/reaction.py                               \
		--iterations $(shell expr $(REACTION_ITERS) \* 2 )                                         \
		--kill 0.066                                                                               \
		--feed 0.04                                                                                \
		--radius 5                                                                                 \
		--size $(REACTION_SIZE)                                                                    \
		--title "Pattern $$\\lambda$$"                                                             \
		--output $(REACTION_DIR)/lambda.eps

$(REACTION_DIR)/mu.eps: $(REACTION_DEPS)
	PYTHONPATH=$(REPO_ROOT) python3 $(REPO_ROOT)/scripts/reaction.py                               \
		--iterations $(shell expr $(REACTION_ITERS) \* 3 )                                         \
		--kill 0.0665                                                                              \
		--feed 0.055                                                                               \
		--radius 32                                                                                \
		--scale 0.1                                                                                \
		--size $(REACTION_SIZE)                                                                    \
		--title "Pattern $$\\mu$$"                                                                 \
		--output $(REACTION_DIR)/mu.eps
