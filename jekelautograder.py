#!/usr/bin/env python3
# The Jekel AutoGrader
# By: John Jekel
# Copyright (c) 2023 John Jekel
#
# Useful script for autograding your project with the testcases in the repository

#TODO take two options, project number and path to tar.gz

# Imports

import os.path

#Functions
def main():
    print("Jekel AutoGrader")

    ensure_testcases_are_locatable_or_die()

    die("The autograder isn't quite finished yet", "John is working on it")

def ensure_testcases_are_locatable_or_die():
    if not os.path.exists("project"):
        die("Couldn't locate any testcases", "Are you running the script from the checked-out repository directory?")

def die(error_string, tip):
    print("Shoot, an error occured: " + error_string)
    print("Maybe this tip will help: " + tip)
    print("From the ashes of disaster grow the roses of success!")

#On script entry, call main()

if __name__ == "__main__":
    main()
