#!/bin/bash
# The Jekel AutoGrader
# By: John Jekel
# Copyright (c) 2023 John Jekel
#
# Small bash script for setting up python and launching the actual autograder (written in Python)
#
#

if [ $(type -P "python3") ]
then
    if [ -f "jekelautograder.py" ]; then
        python3 jekelautograder.py
    else
        echo "Couldn't find jekelautograder.py, refusing to continue"
    fi
else
    echo "Couldn't find a Python version 3 interpreter, refusing to continue"
fi


