XCOV19_SETUP_IMAGE := xcov19-setup
XCOV19_TEST_INTEGRATION_SETUP_IMAGE := xcov19-integration-test

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
	APP_ENV=test PYTHON_CONFIGURE_OPTS="--enable-loadable-sqlite-extensions" APP_DB_ENGINE_URL="sqlite+aiosqlite://" pytest -s xcov19/tests/ -m "integration"

todos:
	@grep -rn "TODO:" xcov19/ --exclude-dir=node_modules --include="*.py"

set-docker:
	@bash set_docker.sh

docker-build:
	docker build --load -f Dockerfile.build -t $(XCOV19_SETUP_IMAGE) .

docker-integration:
	docker build --load -f Dockerfile.test-integration -t $(XCOV19_TEST_INTEGRATION_SETUP_IMAGE) .

docker-run-server:
	docker compose -f docker-compose.yml up --build --remove-orphans

docker-test-integration:
	make docker-integration && docker run -it -f Dockerfile.test-integration
