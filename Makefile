PYTHON ?= python3
PIP ?= pip3
NAME ?=

.PHONY: help setup new-lecture new-exercise install-lecture-reqs test-all clean

help:
	@echo "Targets:"
	@echo "  setup                                Install base project in editable mode"
	@echo "  new-lecture NAME=...                 Scaffold a new lecture under lectures/"
	@echo "  new-exercise LECTURE=... NAME=...    Scaffold a new exercise under a lecture"
	@echo "  install-lecture-reqs NAME=...        Install requirements.txt if present"
	@echo "  test-all                             Run repository-wide tests (placeholder)"
	@echo "  clean                                Remove temporary artifacts"

setup:
	$(PIP) install -e .

new-lecture:
	@if [ -z "$(NAME)" ]; then echo "Usage: make new-lecture NAME=xx-lecture-name"; exit 1; fi
	$(PYTHON) scripts/new_lecture.py $(NAME)

new-exercise:
	@if [ -z "$(LECTURE)" ] || [ -z "$(NAME)" ]; then echo "Usage: make new-exercise LECTURE=xx-lecture-name NAME=uebungNN"; exit 1; fi
	$(PYTHON) scripts/new_exercise.py $(LECTURE) $(NAME)

install-lecture-reqs:
	@if [ -z "$(NAME)" ]; then echo "Usage: make install-lecture-reqs NAME=xx-lecture-name"; exit 1; fi
	@if [ -f lectures/$(NAME)/requirements.txt ]; then \
		$(PIP) install -r lectures/$(NAME)/requirements.txt; \
		else echo "No requirements.txt found for lectures/$(NAME)"; fi

test-all:
	@echo "No tests yet. Add pytest suites per lecture and common."

clean:
	rm -rf **/__pycache__ .pytest_cache .ruff_cache build dist *.egg-info
