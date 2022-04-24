.phony: install install_dev test check

install:
	python3 -m venv .env
	.env/bin/pip install -r requirements.txt

install_dev:
	python3 -m venv .env
	.env/bin/pip install -r requirements.txt
	.env/bin/pip install -r requirements.check.txt

test:
	.env/bin/pytest tests

check:
	.env/bin/mypy drunk tests
	.env/bin/flake8 drunk tests

format:
	.env/bin/isort drunk tests
	.env/bin/black drunk tests