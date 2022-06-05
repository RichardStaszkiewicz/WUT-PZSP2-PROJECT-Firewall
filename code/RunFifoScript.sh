#!/bin/bash
FILE=/dataFlow
if [ ! -p dataFlow ]; then
    mkfifo dataFlow
    chmod 777 dataFlow
fi
echo "" > dataFlow