#!/bin/bash

ruff check xcov19/
PYRIGHT_PYTHON_FORCE_VERSION=latest poetry run pyright **/*.py