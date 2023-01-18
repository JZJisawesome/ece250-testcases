#!/usr/bin/env python3
# The Jekel AutoGrader
# By: John Jekel
# Copyright (c) 2023 John Jekel
#
# Useful script for autograding your project with the testcases in the repository

#TODO take two options, project number and path to tar.gz

# Imports

import sys
import os.path

#Functions
def main():
    print("\x1b[95mJekel AutoGrader\x1b[0m")
    print("\x1b[90mCopyright (c) 2023 John Jekel\x1b[0m\n")

    ensure_testcases_are_locatable_or_die()

    die("The autograder isn't quite finished yet", "John is working on it :)")

def ensure_testcases_are_locatable_or_die():
    if not os.path.exists("projects"):
        die("Couldn't locate any testcases", "Are you running the script from the checked-out repository directory?")

#TODO function to get path to all testcases (input and output)

#TODO function to run testcases and collect results

#TODO function to summarize and grade

def die(error_string, tip):
    print("\x1b[90m\n---------- snip snip ----------\x1b[0m")
    print("\x1b[91;1mShoot, an error occured: \x1b[0m\x1b[91;4m" + error_string + "\x1b[0m")
    print("Maybe this tip will help: \x1b[92m" + tip + "\x1b[0m")
    print("\x1b[95mFrom the ashes of disaster grow the roses of success!\x1b[0m")
    sys.exit(1)

#On script entry, call main()

if __name__ == "__main__":
    main()
