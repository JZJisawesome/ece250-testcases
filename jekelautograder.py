#!/usr/bin/env python3
# The Jekel AutoGrader
# By: John Jekel
# Copyright (c) 2023 John Jekel
#
# Useful script for autograding your project with the testcases in the repository

#TODO take two options, project number and path to tar.gz

# Imports

import argparse
import os.path
import sys

#Functions
def main():
    print("\x1b[95m     _      _        _      _         _         ____               _\x1b[0m")
    print("\x1b[95m    | | ___| | _____| |    / \\  _   _| |_ ___  / ___|_ __ __ _  __| | ___ _ __\x1b[0m")
    print("\x1b[95m _  | |/ _ \\ |/ / _ \\ |   / _ \\| | | | __/ _ \\| |  _| '__/ _` |/ _` |/ _ \\ '__|\x1b[0m")
    print("\x1b[95m| |_| |  __/   <  __/ |  / ___ \\ |_| | || (_) | |_| | | | (_| | (_| |  __/ |\x1b[0m")
    print("\x1b[95m \\___/ \\___|_|\\_\\___|_| /_/   \\_\\__,_|\\__\\___/ \\____|_|  \\__,_|\\__,_|\\___|_|\x1b[0m")

    print("\x1b[90mCopyright (c) 2023 John Jekel\x1b[0m\n")

    basic_sanity_checks()

    tarball_info = get_info_about_tarball()

    die("The autograder isn't quite finished yet", "John is working on it :)")

    print("\x1b[95mWhelp, that's all from me. Thanks for using the Jekel AutoGrader :)\x1b[0m")

def basic_sanity_checks():
    print("Performing some \x1b[4mbasic sanity checks\x1b[0m before we get started...")

    if not os.path.exists("projects"):
        die("Couldn't locate any testcases", "Are you running the script from the checked-out repository directory?")

    #TODO other checks

    print("Looking good, I think I'm set to go!\n")

def get_info_about_tarball():
    if len(sys.argv) != 2:
        print("\x1b[90m\n---------- snip snip ----------\x1b[0m")
        print("\x1b[93;1mShoot, you didn't give me the argument(s) I was expecting!\x1b[0m")
        print("Maybe this tip will help: \x1b[92mI only take a single argument, the path to the tarball that you'd like to test :)\x1b[0m")
        print("\x1b[95mFrom the ashes of disaster grow the roses of success!\x1b[0m")
        sys.exit(1)

    print("To begin, let's check your \x1b[4mtarball file itself\x1b[0m")

    normalized_path = os.path.normpath(sys.argv[1])
    tarball_name = os.path.basename(normalized_path)

    #TODO check it is okay and parse useful info from the filename

    print("Looks good! Based on the name of the tarball, \x1b[96m" + tarball_name + "\x1b[0m, I've deduced the following:")

    die("The autograder isn't quite finished yet", "John is working on it :)")


#TODO function to get path to all testcases (input and output)

#TODO function to run testcases and collect results

#TODO function to summarize and grade

def recoverable_mistake(mistake_string, tip):
    print("\x1b[90m\n---------- snip snip ----------\x1b[0m")
    print("\x1b[93;1mShoot, I might have found a mistake in your project: \x1b[0m\x1b[93;4m" + mistake_string + "\x1b[0m")
    print("Maybe this tip will help: \x1b[92m" + tip + "\x1b[0m")
    print("\x1b[95mFrom the ashes of disaster grow the roses of success!\x1b[0m")
    print("\x1b[90m---------- snip snip ----------\x1b[0m")

def unrecoverable_mistake(mistake_string, tip):
    print("\x1b[90m\n---------- snip snip ----------\x1b[0m")
    print("\x1b[91;1mShoot, there's potentially a mistake in your project we can't ignore: \x1b[0m\x1b[91;4m" + mistake_string + "\x1b[0m")
    print("Maybe this tip will help: \x1b[92m" + tip + "\x1b[0m")
    print("\x1b[95mHappiness can be found even in the darkest of times, if one only remembers to turn on the the light.\x1b[0m")
    sys.exit(1)

def die(error_string, tip):
    print("\x1b[90m\n---------- snip snip ----------\x1b[0m")
    print("\x1b[91;1mShoot, an error occured: \x1b[0m\x1b[91;4m" + error_string + "\x1b[0m")
    print("Maybe this tip will help: \x1b[92m" + tip + "\x1b[0m")
    print("\x1b[95mOh a spoonful of sugar helps the medicine go down, in the most delightful way!\x1b[0m")
    sys.exit(1)

#On script entry, call main()

if __name__ == "__main__":
    main()
