.PHONY: install test clean run demo

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
	@echo "  make demo     - Run with example files"
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

# Run all tests
test:
	@echo "Running basic tests..."
	$(PYTHON_VENV) test_basic.py
	@echo "\nRunning render tests..."
	$(PYTHON_VENV) test_render.py
	@echo "\nRunning complex file tests..."
	$(PYTHON_VENV) test_complex.py
	@echo "\nRunning comprehensive feature tests..."
	$(PYTHON_VENV) test_features.py
	@echo "\n✅ All tests passed!"

# Demo with example files
demo:
	@echo "Demo 1: Simple logs"
	@echo "Run: $(PYTHON_VENV) smart_pager.py examples/sample_logs.txt"
	@echo "\nDemo 2: Complex logs"  
	@echo "Run: $(PYTHON_VENV) smart_pager.py examples/complex_logs.txt"
	@echo "\nPress 'q' to quit, 'j/k' to navigate, Enter to expand JSON"

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

# Quick run with sample file
run:
	$(PYTHON_VENV) smart_pager.py examples/sample_logs.txt
