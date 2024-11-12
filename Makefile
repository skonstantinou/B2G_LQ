###############################################################
### Author .........: Alexandros X. Attikis 
### Institute ......: University Of Cyprus (UCY)
### Note ...........: pdflatex used for generating pdf-files
### Description: ...: Makefile for LaTeX document
###############################################################

### Definitions 
TARGET := talk

TEXSOURCES := $(wildcard tex/*.tex)
TEXTABLES := $(wildcard tables/*.tex)
TEXTABLES += $(wildcard tables/*/*.tex)
BIBSOURCES := $(wildcard *.bib)
EPSFIGURES := $(wildcard figures/*.eps) $(wildcard figures_style/*.eps)

PNGFIGURES := $(wildcard figures/*.png)
PNGFIGURES += $(wildcard figures/*/*.png)
PNGFIGURES += $(wildcard figures/*/*/*.png)
PNGFIGURES += $(wildcard figures/*/*/*/*.png)
PNGFIGURES += $(wildcard figures/*/*/*/*/*.png)
PNGFIGURES += $(wildcard figures/*/*/*/*/*/*.png)
PNGFIGURES += $(wildcard figures/*/*/*/*/*/*/*.png)
PNGFIGURES += $(wildcard figures/*/*/*/*/*/*/*/*.png)

EPSFIGURES += $(wildcard figures/*/*.eps)
EPSFIGURES += $(wildcard figures/*/*/*.eps)
EPSFIGURES += $(wildcard figures/*/*/*/*.eps)
EPSFIGURES += $(wildcard figures/*/*/*/*/*.eps)
EPSFIGURES += $(wildcard figures/*/*/*/*/*/*.eps)
EPSFIGURES += $(wildcard figures/*/*/*/*/*/*/*.eps)
EPSFIGURES += $(wildcard figures/*/*/*/*/*/*/*/*.eps)

PDFFIGURES += $(wildcard figures/*/*.pdf)
PDFFIGURES += $(wildcard figures/*/*/*.pdf)
PDFFIGURES += $(wildcard figures/*/*/*/*.pdf)
PDFFIGURES += $(wildcard figures/*/*/*/*/*.pdf)
PDFFIGURES += $(wildcard figures/*/*/*/*/*/*.pdf)
PDFFIGURES += $(wildcard figures/*/*/*/*/*/*/*.pdf)
PDFFIGURES += $(wildcard figures/*/*/*/*/*/*/*/*.pdf)

PDFGENFIGURES := $(patsubst %.eps,%.pdf,$(EPSFIGURES))
PDFFIGURES := $(filter-out $(PDFGENFIGURES),$(wildcard figures/*.pdf))

PDFSOURCES := $(TEXSOURCES) $(TEXTABLES) $(BIBSOURCES) $(PDFFIGURES) $(PDFGENFIGURES) $(PNGFIGURES)

.SUFFIXES: .pdf .eps
.PHONY: spell clean realclean

default: $(TARGET)

all: pdf

### Produce pdf
$(TARGET): $(TARGET).pdf

pdf: $(TARGET).pdf
$(TARGET).pdf: $(TARGET).tex $(PDFSOURCES)
	@rm -f output.txt warnings.txt
	@pdflatex $(TARGET).tex
	#@bibtex $(TARGET)
	@pdflatex $(TARGET).tex | tee -a output.txt
	@echo "\n****************************************************************************"
	@grep -i 'warning' output.txt | tee -a warnings.txt
	@echo "\n*** Number of \"LaTeX Warning\" occurrences in warnings.txt:" 
	@grep -i 'warning' warnings.txt | wc -l
	@echo "\n*** Generated pdf document:"
	@ls -la $(TARGET).pdf
	@echo "****************************************************************************"
	@echo

### Rules for conversions
%.pdf: %.eps
	@echo "Converting figure '$*.eps' to pdf format"
	@epstopdf $*.eps

spell:
	@for f in $(TEXSOURCES); do \
	echo "Spell checking $$f"; \
	aspell check --master=british $$f; \
	done

clean:
	@rm -f $(TARGET).out $(TARGET).aux $(TARGET).log $(TARGET).toc $(TARGET).blg $(TARGET).bbl $(TARGET).ps $(TARGET).pdf $(PDFGENFIGURES)
	@echo "Temporary files removed"

realclean: clean
	@rm -f *~ tex/*~ tables/*~ tables/*/*~ figures/*~ figures/*/*~ \
	  *.backup tex/*.backup tables/*.backup tables/*/*.backup figures/*.backup figures/*/*.backup
	@echo "Backup files removed"

open: pdf
	@open -a Preview $(TARGET).pdf
