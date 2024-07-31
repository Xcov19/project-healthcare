#!/bin/bash

ruff check domain/
ruff check app/
PYRIGHT_PYTHON_FORCE_VERSION=latest poetry run pyright **/*.py