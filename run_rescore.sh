#!/usr/bin/env bash

for file in ./logs/*; do
    inspect score "$file" --action overwrite --scorer scorers.py@max_cell_match 
done
