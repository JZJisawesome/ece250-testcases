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
        echo -e "\033[91;1mShoot, an error occured: \033[0m\033[91;4mCouldn't find jekelautograder.py\033[0m"
        echo -e "Maybe this tip will help: \033[92mAre you running the autograder from the repository root?\033[0m"
        echo -e "\033[95mFrom the ashes of disaster grow the roses of success!\033[0m"
    fi
else
        echo -e "\033[91;1mShoot, an error occured: \033[0m\033[91;4mCouldn't find a Python version 3 interpreter\033[0m"
        echo -e "Maybe this tip will help: \033[92mAre you on eceubuntu? If not, do you have python installed?\033[0m"
        echo -e "\033[95mFrom the ashes of disaster grow the roses of success!\033[0m"
fi


