lint:
	flake8 --verbose # --docstring-convention

py_test:
	pytest

black_format:
	black .


test_all:
	make black_format
	make lint
	make py_test