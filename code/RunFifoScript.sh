#!/bin/bash
gcc makeFifo.c -o makeFifo
./makeFifo
chmod 777 dataFlow
echo "" > dataFlow