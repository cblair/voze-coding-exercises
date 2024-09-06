#!/usr/bin/env bash

echo "Run to install coverage tool: python3 -m pip install coverage"
echo "Then add to PATH. i.e.:"
echo 'export PATH=$PATH:/Library/Frameworks/Python.framework/Versions/3.7/bin'

coverage run --omit=test_*,perf.py -m unittest test_*.py
coverage report -m
