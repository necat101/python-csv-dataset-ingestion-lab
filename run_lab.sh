#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
python3 run_lab.py
echo
python3 -m unittest test_lab -v
