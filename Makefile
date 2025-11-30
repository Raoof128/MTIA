.PHONY: install run test lint format clean help

PYTHON = python3
PIP = pip

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make run        - Run the application"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linters (flake8, mypy)"
	@echo "  make format     - Format code (black, isort)"
	@echo "  make clean      - Remove build artifacts"

install:
	$(PIP) install -r requirements.txt
	$(PIP) install -e .[dev]

run:
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

test:
	PYTHONPATH=. pytest

lint:
	flake8 backend tests
	mypy backend

format:
	black backend tests
	isort backend tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -rf {} +
