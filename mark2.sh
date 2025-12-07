#!/bin/bash

export PYTHONPATH=./src

# 31 red
# 32 green
# 33 yellow

./src/mark2/main.py "$@" 2> >(while IFS= read -r line; do
    echo -e "\e[33m$line\e[0m" >&2
done)
