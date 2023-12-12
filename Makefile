.PHONY: pre-commit
pre-commit: venv
	venv/bin/pre-commit install

venv: venv/touchfile

venv/touchfile: requirements.txt
	test -d venv || python3.10 -m venv venv
	venv/bin/pip install -r requirements.txt

.PHONY: clean
clean:
	rm -rf venv
	find . -iname "*.pyc" -delete
	find . -type d -name __pycache__ -delete
