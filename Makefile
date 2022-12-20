.phony: install install_dev test check

install:
	python3 -m venv .env
	.env/bin/pip install -r requirements.txt
	.env/bin/pip install -e .

install_dev:
	python3 -m venv .env
	.env/bin/pip install -r requirements.txt
	.env/bin/pip install -r requirements.check.txt
	.env/bin/pip install -e .	

test:
	.env/bin/pytest tests

check:
	.env/bin/flake8 drunk tests
	.env/bin/mypy drunk tests
	.env/bin/pylint drunk tests

format:
	.env/bin/isort drunk tests
	.env/bin/black drunk tests