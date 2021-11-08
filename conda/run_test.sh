#! /bin/bash
$PYTHON -m pytest tests/abstractions
$PYTHON -m pytest tests/parser
$PYTHON -m pytest tests/runtime
$PYTHON -m pytest tests/tsc
$PYTHON -m pytest tests/utils
