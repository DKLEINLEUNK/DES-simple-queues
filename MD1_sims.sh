#!/bin/bash

lamb_values=(0.1 0.4 0.8 1.2 1.6 1.8 1.9 1.98)
for lamb in "${lamb_values[@]}"
do
    python3 main.py MD1 100000 -c 10000 -l $lamb -m 2 -n 250 --save
done