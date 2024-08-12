check:
	@bash check.sh

run:
	@bash run.sh

install:
	@bash install.sh

pip-install:
	pip install --prefer-binary --use-pep517  --check-build-dependencies .[dev]

test:
	pytest -s xcov19/tests/
