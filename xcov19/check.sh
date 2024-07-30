#!/bin/bash

ruff check xcov19/domain/*.py
poetry run pyright xcov19/domain