#!/usr/bin/env python3
# The Jekel AutoGrader
# By: John Jekel
# Copyright (c) 2023 John Jekel
#
# Useful script for autograding your project with the testcases in the repository

# Constants
TESTING_DIR = "~/.jekelautograder"

# Imports

import argparse
import json
import os
import shutil
import subprocess
import sys
import tarfile

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

    extract_tarball_and_compile(tarball_info[0], tarball_info[1], tarball_info[2])

    testcases = read_manifest(tarball_info[2])

    test_results = run_testcases(tarball_info[2], testcases)

    summarize_and_grade(tarball_info[1], tarball_info[2], testcases, test_results)

    print("Whelp, that's all from me. Good luck on your project! - JZJ")

def basic_sanity_checks():
    print("Performing some \x1b[4mbasic sanity checks\x1b[0m before we get started...")

    if not os.path.exists("projects"):
        die("Couldn't locate the projects directory", "Are you running the script from the checked-out repository directory?")

    for i in range(1, 4):
        if not os.path.exists("projects/project" + str(i)):
            die("Couldn't locate the projects/project" + str(i) + " directory", "Are you running the script from the checked-out repository directory?")
        if not os.path.exists("projects/project" + str(i) + "/manifest.json"):
            die("Couldn't locate the projects/project" + str(i) + "/manifest.json file", "Are you running the script from the checked-out repository directory?")
        if not os.path.exists("projects/project" + str(i) + "/input"):
            die("Couldn't locate the projects/project" + str(i) + "/input directory", "Are you running the script from the checked-out repository directory?")
        if not os.path.exists("projects/project" + str(i) + "/output"):
            die("Couldn't locate the projects/project" + str(i) + "/output directory", "Are you running the script from the checked-out repository directory?")

    print("Looking good, I think I'm set to go!\n")

def get_info_about_tarball():
    if len(sys.argv) != 2:
        general_unrecoverable_mistake("You didn't give me the argument(s) I was expecting!", "I only take a single argument, the path to the tarball that you'd like to test :)")

    print("To begin, let's check your \x1b[4mtarball's file name and path\x1b[0m...")

    raw_path = sys.argv[1]

    if not os.path.exists(raw_path):
        general_unrecoverable_mistake("The tarball you specified dosn't exist!", "Double check the path you provided and give it another go")

    normalized_path = os.path.normpath(sys.argv[1])
    tarball_name = os.path.basename(normalized_path)

    split_by_underscore = tarball_name.split("_")

    if len(split_by_underscore) != 2:
        unrecoverable_project_mistake("The format of your tarball's name is incorrect", "Check out the requirements for tarball naming on LEARN and try again")

    uwid = split_by_underscore[0]

    if (len(uwid) == 0) or (len(uwid) > 8) or (not uwid.isalpha()):
        unrecoverable_project_mistake("You're not using your eight-letter-or-less UW ID", "Check out the requirements for tarball naming on LEARN and try again")

    split_last_part_by_dot = split_by_underscore[1].split(".")

    if len(split_last_part_by_dot) != 3:
        unrecoverable_project_mistake("The format of your tarball's name is incorrect", "Check out the requirements for tarball naming on LEARN and try again")

    project_num_str = split_last_part_by_dot[0]

    if (len(project_num_str) != 2) or (project_num_str[:1] != "p"):
        unrecoverable_project_mistake("The format of your tarball's name is incorrect", "Check out the requirements for tarball naming on LEARN and try again")

    try:
        project_num = int(project_num_str[1:2])
    except ValueError:
        unrecoverable_project_mistake("The project number is missing", "Check out the requirements for tarball naming on LEARN and try again")

    if (project_num == 0) or (project_num > 4):
        unrecoverable_project_mistake("The project number is invalid", "Check out the requirements for tarball naming on LEARN and try again")

    if (split_last_part_by_dot[1] != "tar") or (split_last_part_by_dot[2] != "gz"):
        unrecoverable_project_mistake("Bad file extension", "Check out the requirements for tarball naming on LEARN and try again")

    print("Excellent! Based on the name of the tarball, \x1b[96m" + tarball_name + "\x1b[0m, I've deduced the following:")
    print("Your UWID is: \x1b[96m" + uwid + "\x1b[0m")
    print("Your tarball is for: \x1b[96mProject " + str(project_num) + "\x1b[0m")
    if (uwid == "jzjekel"):
        print("You are my creator :)")
    print("")

    return normalized_path, uwid, project_num

def extract_tarball_and_compile(tarball_path, uwid, project_num):
    print("Okay, now I'm going to \x1b[4mextract your tarball\x1b[0m to a temporary location...")

    testing_path = os.path.expanduser(TESTING_DIR)

    #TODO better error checking

    #Delete the testing directory if it already existed before
    if os.path.exists(testing_path):
        shutil.rmtree(testing_path)

    #Create the testing directory
    os.mkdir(testing_path)

    #Copy the tarball to the testing directory
    new_tarball_path = testing_path + "/tarball.tar.gz"
    shutil.copyfile(tarball_path, new_tarball_path)

    #Extract it
    tarball = tarfile.open(new_tarball_path)
    tarball.extractall(testing_path)

    #Check for a design doc
    print("Done! Let me just double check your \x1b[4mdesign doc\x1b[0m...")
    design_doc_name = uwid + "_design_p" + str(project_num) + ".pdf"
    if not design_doc_name in tarball.getnames():
        recoverable_project_mistake("Your design doc is missing or named incorrectly", "It should be named \"" + design_doc_name + "\"")
    else:
        print("The name looks good! ", end="")

    print("Now I'll \x1b[4mtest your Makefile\x1b[0m...")
    if not "Makefile" in tarball.getnames():
        tarball.close()
        unrecoverable_project_mistake("Your Makefile is missing!", "Please ensure your tarball includes a file called Makefile and try again")
    tarball.close()

    make_subprocess = subprocess.Popen(["make"], cwd=testing_path)
    make_subprocess.wait()
    if not os.path.exists(testing_path + "/a.out"):
        unrecoverable_project_mistake("Your makefile didn't produce a.out", "Please ensure there are no errors above, and that you haven't used GCC's -o option")

    print("Sweet, your Makefile sucessfully produced an a.out binary!\n")

def read_manifest(project_num):
    print("Reading the manifest file for Project " + str(project_num) + " and \x1b[4mensuring I can find all of the testcases\x1b[0m...")

    #TODO error checking json parsing

    #We can already assume the manifest exists (it was checked by sanity checks)
    testcases_path = "projects/project" + str(project_num)
    manifest_path = testcases_path + "/manifest.json"
    manifest_file = open(manifest_path)
    manifest = json.load(manifest_file)#TODO handle exceptions here

    if not "testcases" in manifest:
        die("The manifest.json for the current project is missing a testcases array", "Fix the manifest, or contact jzjekel@uwaterloo.ca")

    for testcase in manifest["testcases"]:
        if not "name" in testcase:
            die("A testcase in the manifest.json is missing a name.", "Fix the manifest, or contact jzjekel@uwaterloo.ca")
        if not "author" in testcase:
            die("The \"" + testcase["name"] + "\" testcase in the manifest.json is missing an author.", "Fix the manifest, or contact jzjekel@uwaterloo.ca")
        if not os.path.exists(testcases_path + "/input/" + testcase["name"] + ".in"):
            die("The input file for the \"" + testcase["name"] + "\" testcase in the manifest.json is missing", "Add the file or remove the entry from the manifest, or contact jzjekel@uwaterloo.ca")
        if not os.path.exists(testcases_path + "/output/" + testcase["name"] + ".out"):
            die("The output file for the \"" + testcase["name"] + "\" testcase in the manifest.json is missing", "Add the file or remove the entry from the manifest, or contact jzjekel@uwaterloo.ca")

    print("Awesome, all " + str(len(manifest["testcases"])) + " testcase(s) in the manifest exist!\n")
    return manifest["testcases"]

def run_testcases(project_num, testcases):#TODO parameters
    print("Alright, we're finally getting to the good part. Let's run some testcases!")

    testcases_path = "projects/project" + str(project_num)
    testing_path = os.path.expanduser(TESTING_DIR)

    failed_testcases = []

    #TODO make this multithreaded otherwise this will be quite slow

    testcase_num = 1
    for testcase in testcases:
        print("Running testcase " + str(testcase_num) + " of " + str(len(testcases)) + ": \"\x1b[96m" + testcase["name"] + "\x1b[0m\", by \x1b[95m" + testcase["author"] + "\x1b[0m... ", end="")

        testcase_input_file = open(testcases_path + "/input/" + testcase["name"] + ".in")

        test_subprocess = subprocess.Popen(["valgrind", "./a.out"], stdin=testcase_input_file, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=testing_path)
        test_subprocess.wait()
        testcase_input_file.close()

        test_subprocess_stdout, test_subprocess_stderr = test_subprocess.communicate()

        if "All heap blocks were freed -- no leaks are possible" in test_subprocess_stderr.decode():
            memory_safe = True
        else:
            memory_safe = False

        stdout_as_lines = test_subprocess_stdout.decode().splitlines()
        testcase_output_file = open(testcases_path + "/output/" + testcase["name"] + ".out")
        expected_output_as_lines = testcase_output_file.read().splitlines()
        testcase_output_file.close()

        mismatched_line = -1
        correct_output = True
        for i in range(len(expected_output_as_lines)):
            if (i >= len(stdout_as_lines)) or (stdout_as_lines[i] != expected_output_as_lines[i]):
                correct_output = False
                mismatched_line = i
                break

        if not correct_output:
           print("\x1b[91mLine " + str(mismatched_line) + " mismatched the expected output :(\x1b[0m")
        elif not memory_safe:
           print("\x1b[93mMemory unsafety detected :(\x1b[0m")
        else:
           print("\x1b[92mSuccessful! :)\x1b[0m")

        if (not correct_output) or (not memory_safe):
            failed_testcases.append((testcase["name"], correct_output, mismatched_line, memory_safe))

        testcase_num = testcase_num + 1

    if len(failed_testcases) != 0:
        recoverable_project_mistake("At least one of the testcases was unsuccessful", "Try to run the problematic testcases manually to narrow down the issue in your code")

    print("")

    return failed_testcases

def summarize_and_grade(uwid, project_num, testcases, failed_testcases):
    if len(failed_testcases) == 0:
        print("\x1b[92;5;1mCongratulations " + uwid + "!\x1b[0m\x1b[92m You passed every testcase I have for Project " + str(project_num) + " with flying colors!\x1b[0m")

    print("Here is a breakdown of your grade: ")
    print("Testcases passed: \x1b[96m" + str(len(testcases) - len(failed_testcases))+ " out of " + str(len(testcases)) + "\x1b[0m")
    print("Testcases failed: \x1b[96m" + str(len(failed_testcases))+ " out of " + str(len(testcases)) + "\x1b[0m")

    failed_with_output_mismatches = 0
    failed_with_memory_unsafety = 0
    for testcase in failed_testcases:
        if not testcase[1]:
            failed_with_output_mismatches = failed_with_output_mismatches + 1
        if not testcase[3]:
            failed_with_memory_unsafety = failed_with_memory_unsafety + 1

    print("Testcases with output mismatches: \x1b[96m" + str(failed_with_output_mismatches)+ " out of " + str(len(testcases)) + "\x1b[0m")
    print("Testcases with memory unsafety: \x1b[96m" + str(failed_with_memory_unsafety)+ " out of " + str(len(testcases)) + "\x1b[0m")

    print("\x1b[95mYour JekelScore(TM) is %", str((float(len(testcases) - len(failed_testcases)) / float(len(testcases))) * 100) + "\x1b[0m\n")

def recoverable_project_mistake(mistake_string, tip):
    print("\x1b[90m\n---------- snip snip ----------\x1b[0m")
    print("\x1b[93;1mShoot, I might have found a mistake in your project: \x1b[0m\x1b[93;4m" + mistake_string + "\x1b[0m")
    print("Maybe this tip will help: \x1b[92m" + tip + "\x1b[0m")
    print("\x1b[95mEvery shiny dream that fades and dies, generates the steam for two more tries!\x1b[0m")
    print("\x1b[90m---------- snip snip ----------\x1b[0m")

def unrecoverable_project_mistake(mistake_string, tip):
    print("\x1b[90m\n---------- snip snip ----------\x1b[0m")
    print("\x1b[91;1mShoot, there's potentially a mistake in your project we can't ignore: \x1b[0m\x1b[91;4m" + mistake_string + "\x1b[0m")
    print("Maybe this tip will help: \x1b[92m" + tip + "\x1b[0m")
    print("\x1b[95mHappiness can be found even in the darkest of times, if one only remembers to turn on the the light.\x1b[0m")
    sys.exit(1)

def general_unrecoverable_mistake(mistake_string, tip):
    print("\x1b[90m\n---------- snip snip ----------\x1b[0m")
    print("\x1b[91;1mShoot, I might have found a mistake: \x1b[0m\x1b[91;4m" + mistake_string + "\x1b[0m")
    print("Maybe this tip will help: \x1b[92m" + tip + "\x1b[0m")
    print("\x1b[95mFrom the ashes of disaster grow the roses of success!\x1b[0m")
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
