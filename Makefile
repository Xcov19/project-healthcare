check:
	@bash check.sh

run:
	@bash run.sh

install:
	@bash install.sh

pip-install:
	pip install --prefer-binary --use-pep517  --check-build-dependencies .[dev]

test:
	APP_ENV=test APP_DB_ENGINE_URL="sqlite+aiosqlite://" pytest -s xcov19/tests/ -m "not slow and not integration and not api"

test-integration:
	APP_ENV=test APP_DB_ENGINE_URL="sqlite+aiosqlite://" pytest -s xcov19/tests/ -m "integration"

todos:
	@grep -rn "TODO:" xcov19/ --exclude-dir=node_modules --include="*.py"