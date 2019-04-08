PROJECT_NAME := hw4
SRC := $(shell find . -name '*.tex') homework.sty

.PHONY: $(PROJECT_NAME).pdf all clean view

all: $(PROJECT_NAME).pdf $(SRC)

$(PROJECT_NAME).pdf: $(PROJECT_NAME).tex
	# latexmk -pdf --synctex=1 -file-line-error -interaction=nonstopmode -shell-escape $<
	latexmk -pdf --synctex=1 -file-line-error -interaction=batchmode -shell-escape $<

# A target to build with better error messages when latexmk craps itself.
error:
	pdflatex -shell-escape -file-line-error $(PROJECT_NAME).tex

clean:
	latexmk -C
	rm -rf *.bbl *.tdo

view:
	1>/dev/null 2>/dev/null xdg-open $(PROJECT_NAME).pdf &
