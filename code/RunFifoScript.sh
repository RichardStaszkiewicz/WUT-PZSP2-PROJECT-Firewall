#!/bin/bash
FILE=/dataFlow
if [ ! -p dataFlow ]; then
    mkfifo dataFlow
    chmod 777 dataFlow
fi

echo "\n echo \n"

echo "" > dataFlow