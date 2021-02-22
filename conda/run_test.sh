#! /bin/bash
$PYTHON -m pytest tests/metaclass
$PYTHON -m pytest tests/preprocess
$PYTHON -m pytest tests/runtime
$PYTHON -m pytest tests/tsc
$PYTHON -m pytest tests/utils