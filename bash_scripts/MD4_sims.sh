#!/bin/bash

cd .. 

lamb_values=(0.4 1.6 3.2 4.8 6.4 7.2 7.6 7.92)
for lamb in "${lamb_values[@]}"
do
    python3 main.py MD4 100000 -c 10000 -l $lamb -m 2 -n 250 --save
done