.PHONY: help
.DEFAULT_GOAL := help

help:
	echo "There was, not help, no help from you!"

install: ## Install requirements
	pip install -r requirements.txt

format: ## Run code formatters
	isort app
	black app

lint: ## Run code linters
	isort --check app
	black --check app
	flake8 app
	mypy app

test:  ## Run tests with coverage
	pytest --cov