#!/bin/bash
autoflake -r --exclude "**/__init__.py" --in-place --remove-all-unused-imports .
isort --skip "migrations/*" -rc .
black --exclude migrations .
