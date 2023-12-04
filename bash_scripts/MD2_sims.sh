#!/bin/bash

cd ..

lamb_values=(0.2 0.8 1.6 2.4 3.2 3.6 3.8 3.96)
for lamb in "${lamb_values[@]}"
do
    python3 main.py MD2 100000 -c 10000 -l $lamb -m 2 -n 250 --save
done