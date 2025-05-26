.PHONY: install test clean run

# Variables
PYTHON = python3
VENV = venv
VENV_BIN = $(VENV)/bin
PIP = $(VENV_BIN)/pip
PYTHON_VENV = $(VENV_BIN)/python

# Default target
help:
	@echo "Smart Pager Development Commands:"
	@echo "  make setup    - Create virtual environment and install dependencies"
	@echo "  make test     - Run all tests"
	@echo "  make run      - Run with example file"
	@echo "  make install  - Install package in development mode"
	@echo "  make clean    - Clean up generated files"

# Setup development environment
setup:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Install package in development mode
install: setup
	$(PIP) install -e .

# Run tests
test:
	$(PYTHON_VENV) test_basic.py
	$(PYTHON_VENV) test_render.py

# Run with example file
run:
	$(PYTHON_VENV) smart_pager.py examples/sample_logs.txt

# Clean up
clean:
	rm -rf $(VENV)
	rm -rf *.pyc
	rm -rf __pycache__
	rm -rf smart_pager/__pycache__
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/

# Format code (if black is installed)
format:
	$(PIP) install black
	$(VENV_BIN)/black smart_pager/ *.py
