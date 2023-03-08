#!/usr/bin/env python3
#The Jekel AutoGrader
#Copyright (c) 2023 John Jekel and Aiden Fox Ivey
#
#Useful script for autograding your project with the testcases in the repository

#Constants
DEFAULT_TIMEOUT_SECS = 30
TESTING_DIR = "~/.jekelautograder"
TARBALL_REQUIREMENTS_TIP = "Check out the requirements for tarball naming on LEARN and try again"
RUNNING_FROM_CHECKOUT_REPO_TIP = "Are you running the script from the checked-out repository directory?"
FMT_INCORRECT_ERROR = "The format of your tarball's name is incorrect"
COULD_NOT_LOCATE_ERROR_PREFIX = "Couldn't locate the projects/project"
FIX_MANIFEST_TIP = "Fix the manifest, or leave an issue at https://github.com/JZJisawesome/ece250-testcases/issues"
PROJECT3_CORPUS_URL = "http://textfiles.com/games/REVIEWS/careurp.rev"
PROJECT3_CORPUS_NAME = "corpus.txt"

#A UWID is expected to be in the following format.
#Up to 8 alphanumeric characters. Some number (1, inf) of
#alphabetic characters, (0,4) numbers, and another
#(1,inf) of alphabetic characters
UWID_REGEX = r"^(?=.{3,8}$)(?=[a-z]+\d{0,4}[a-z]+$).+$"

#Imports
import json
import multiprocessing
import os
import shutil
import subprocess
import sys
import tarfile
import time
import platform
import requests
import re

#Functions
def main():
    print("\x1b[36m ____              _   _              __  __                                     _");
    print("\x1b[36m| __ )  ___   ___ | |_| | ___  __ _  |  \\/  | __ _ _ __ _ __ ___   ___  ___  ___| |_");
    print("\x1b[36m|  _ \\ / _ \\ / _ \\| __| |/ _ \\/ _` | | |\\/| |/ _` | '__| '_ ` _ \\ / _ \\/ __|/ _ \\ __|");
    print("\x1b[36m| |_) | (_) | (_) | |_| |  __/ (_| | | |  | | (_| | |  | | | | | | (_) \\__ \\  __/ |_");
    print("\x1b[36m|____/ \\___/ \\___/ \\__|_|\\___|\\__, | |_|  |_|\\__,_|_|  |_| |_| |_|\\___/|___/\\___|\\__|");
    print("\x1b[36m                              |___/\x1b[0m");
    print("\x1b[90m---------- snip snip ----------\x1b[0m")
    print("\x1b[1mOops, wrong title, just a sec...\x1b[0m")
    print("\x1b[90m---------- snip snip ----------\x1b[0m")

    print("\x1b]0;Jekel AutoGrader\x07", end="")
    print("\x1b[95m     _      _        _      _         _         ____               _\x1b[0m")
    print("\x1b[95m    | | ___| | _____| |    / \\  _   _| |_ ___  / ___|_ __ __ _  __| | ___ _ __\x1b[0m")
    print("\x1b[95m _  | |/ _ \\ |/ / _ \\ |   / _ \\| | | | __/ _ \\| |  _| '__/ _` |/ _` |/ _ \\ '__|\x1b[0m")
    print("\x1b[95m| |_| |  __/   <  __/ |  / ___ \\ |_| | || (_) | |_| | | | (_| | (_| |  __/ |\x1b[0m")
    print("\x1b[95m \\___/ \\___|_|\\_\\___|_| /_/   \\_\\__,_|\\__\\___/ \\____|_|  \\__,_|\\__,_|\\___|_|    for ECE 250\x1b[0m")

    print("\x1b[90mCopyright (c) 2023 John Jekel and Aiden Fox Ivey\x1b[0m\n")

    print("You saw \x1b[1mnothing!\x1b[0m\n")

    basic_sanity_checks()

    tarball_info = get_info_about_tarball()

    extract_tarball_and_compile(tarball_info[0], tarball_info[1], tarball_info[2])

    if tarball_info[2] == 3:
        project3_corpus_logic()

    testcases = read_manifest(tarball_info[2])

    test_results = run_testcases(tarball_info[2], testcases)

    summarize_and_grade(tarball_info[1], tarball_info[2], testcases, test_results)

    print("Whelp, that's all from me. Good luck on your project! - JZJ")
    print("\x1b[1mP.S. Don't forget to contribute your testcases to https://github.com/JZJisawesome/ece250-testcases!\x1b[0m")

    print("\x1b[?25h\x07", end="")

def basic_sanity_checks():
    print("Performing some \x1b[4mbasic sanity checks\x1b[0m before we get started...")

    if not os.path.exists("projects"):
        die("Couldn't locate the projects directory", RUNNING_FROM_CHECKOUT_REPO_TIP)

    for i in range(1, 4):
        if not os.path.exists("projects/project" + str(i)):
            die(COULD_NOT_LOCATE_ERROR_PREFIX + str(i) + " directory", RUNNING_FROM_CHECKOUT_REPO_TIP)
        if not os.path.exists("projects/project" + str(i) + "/manifest.json"):
            die(COULD_NOT_LOCATE_ERROR_PREFIX + str(i) + "/manifest.json file", RUNNING_FROM_CHECKOUT_REPO_TIP)
        if not os.path.exists("projects/project" + str(i) + "/input"):
            die(COULD_NOT_LOCATE_ERROR_PREFIX + str(i) + "/input directory", RUNNING_FROM_CHECKOUT_REPO_TIP)
        if not os.path.exists("projects/project" + str(i) + "/output"):
            die(COULD_NOT_LOCATE_ERROR_PREFIX + str(i) + "/output directory", RUNNING_FROM_CHECKOUT_REPO_TIP)

    if shutil.which("valgrind") is None:
        die("Couldn't locate the \"valgrind\" executable in the PATH", "Do you have Valgrind installed?")

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
        unrecoverable_project_mistake(FMT_INCORRECT_ERROR, TARBALL_REQUIREMENTS_TIP)

    uwid = split_by_underscore[0]
    pattern = re.compile(UWID_REGEX)

    if not pattern.match(uwid):
        unrecoverable_project_mistake("You're not using your up-to-eight-character UW ID", "Check out the requirements for tarball naming on LEARN and try again")

    split_last_part_by_dot = split_by_underscore[1].split(".")

    if len(split_last_part_by_dot) != 3:
        unrecoverable_project_mistake(FMT_INCORRECT_ERROR, TARBALL_REQUIREMENTS_TIP)

    project_num_str = split_last_part_by_dot[0]

    if (len(project_num_str) != 2) or (project_num_str[:1] != "p"):
        unrecoverable_project_mistake(FMT_INCORRECT_ERROR, TARBALL_REQUIREMENTS_TIP)

    try:
        project_num = int(project_num_str[1:2])
    except ValueError:
        unrecoverable_project_mistake("The project number is missing", TARBALL_REQUIREMENTS_TIP)

    if (project_num == 0) or (project_num > 4):
        unrecoverable_project_mistake("The project number is invalid", TARBALL_REQUIREMENTS_TIP)

    if (split_last_part_by_dot[1] != "tar") or (split_last_part_by_dot[2] != "gz"):
        unrecoverable_project_mistake("Bad file extension", TARBALL_REQUIREMENTS_TIP)

    print("Excellent! Based on the name of the tarball, \x1b[96m" + tarball_name + "\x1b[0m, I've deduced the following:")
    print("Your UWID is: \x1b[96m" + uwid + "\x1b[0m")
    print("Your tarball is for: \x1b[96mProject " + str(project_num) + "\x1b[0m")
    if (uwid == "jzjekel"):
        print("\x1b[1mYou are my creator :)\x1b[0m")
    elif ((uwid == "abfoxive") or (uwid == "fmirshek")):
        print("\x1b[1mYou are an AutoGrader maintainer :)\x1b[0m")
    elif (uwid == "laledes"):
        print("\x1b[1mMacOS support is coming, I promise...\x1b[0m")
    elif (uwid == "example"):
        print("\x1b[1mYou know you don't have to copy and paste everything exactly from the README, right?\x1b[0m")
        print("\x1b[1mUnless of course your UWID is actually example, in which case, hello!\x1b[0m")

    print("")

    return normalized_path, uwid, project_num

def extract_tarball_and_compile(tarball_path, uwid, project_num):
    print("Okay, now I'm going to \x1b[4mextract your tarball\x1b[0m to a temporary location...")

    testing_path = os.path.expanduser(TESTING_DIR)

    #Delete the testing directory if it already existed before
    if os.path.exists(testing_path):
        try:
            shutil.rmtree(testing_path)
        except OSError:
            general_warning("Failed to remove the temporary directory " + TESTING_DIR, "Likely this is an issue with NFS; you can probably ignore this")

    #Create the testing directory
    try:
        os.mkdir(testing_path)
    except OSError:
        if os.path.exists(testing_path):
            general_warning("Unable to create the temporary directory, since it already exists", "Likely this is an issue with NFS; you can probably ignore this")
        else:
            die("Unable to create the temporary directory " + TESTING_DIR, "Is there a permissions issue in your home directory?")

    #Copy the tarball to the testing directory (we can assume both exist)
    new_tarball_path = testing_path + "/tarball.tar.gz"
    try:
        shutil.copyfile(tarball_path, new_tarball_path)
    except IsADirectoryError:
        unrecoverable_project_mistake("Tarball is actually a directory", "Nice try breaking the autograder. Better luck next time :)")

    #Extract it
    try:
        tarball = tarfile.open(new_tarball_path)
    except tarfile.HeaderError:
        unrecoverable_project_mistake("Corrupted tarball", "Recreate the tarball and try again")
    except tarfile.ReadError:
        unrecoverable_project_mistake("Couldn't open the tarball for reading", "Do you have read permissions?")
    except tarfile.CompressionError:
        unrecoverable_project_mistake("Unsupported tarball compression method", "Your tarball should be gzip-compressed")
    try:
        tarball.extractall(testing_path)
    except tarfile.HeaderError:
        tarball.close()
        unrecoverable_project_mistake("Corrupted tarball", "Recreate the tarball and try again")
    except tarfile.CompressionError:
        tarball.close()
        unrecoverable_project_mistake("Problem when decompressing tarball", "Your tarball should be gzip-compressed; perhaps it is corrupt?")

    #Ensure the tarball dosn't contain any directories
    for member in tarball.getmembers():
        if member.isdir():
            unrecoverable_project_mistake("You have a least one directory in your tarball, which confuses the autograder!", "There should be no directories in the tarball whatsoever as mentioned by the ECE 250 teaching staff")

    #Check for a design doc
    print("Done! Let me just double check your \x1b[4mdesign doc\x1b[0m...")
    design_doc_name = uwid + "_design_p" + str(project_num) + ".pdf"
    if not design_doc_name in tarball.getnames():
        recoverable_project_mistake("Your design doc is missing or named incorrectly", "It should be named \"" + design_doc_name + "\"")
    else:
        print("The name looks good! ", end="")

    #Project 3-specific checks
    if project_num == 3:
        print("Since this is Project 3, I'll now \x1b[4mperform Project 3-specific checks\x1b[0m...")
        if not "trietest.cpp" in tarball.getnames():
            recoverable_project_mistake("Project 3 requires that you have a file named \"trietest.cpp\" containing main()", "Please create this file and move your main() function to it")
        if PROJECT3_CORPUS_NAME in tarball.getnames():
            unrecoverable_project_mistake("Found " + PROJECT3_CORPUS_NAME + " in your tarball!", "The corpus will be provided during autograding, you aren't allowed to include it in your tarball")

    #Test the user's makefile
    print("Now I'll \x1b[4mtest your Makefile\x1b[0m...")
    if not "Makefile" in tarball.getnames():
        tarball.close()
        unrecoverable_project_mistake("Your Makefile is missing!", "Please ensure your tarball includes a file called Makefile in the root and try again")

    #Ensure a.out wasn't bundled with the tarball accidentally
    if "a.out" in tarball.getnames():
        tarball.close()
        unrecoverable_project_mistake("Your tarball already contains an a.out binary", "Please ensure your tarball does not include any pre-compiled code whatsoever!")

    #We no longer need to access the tarball
    tarball.close()

    make_subprocess = subprocess.Popen(["make", "-j"], cwd=testing_path)
    make_subprocess.wait()
    if not os.path.exists(testing_path + "/a.out"):
        unrecoverable_project_mistake("Your Makefile didn't produce a.out", "Please ensure there are no errors above, and that you haven't used GCC's -o option")

    print("Sweet, your Makefile sucessfully \x1b[4mproduced an a.out binary\x1b[0m!\n")

def read_manifest(project_num):
    print("Reading the manifest file for Project " + str(project_num) + " and \x1b[4mensuring I can find all of the testcases\x1b[0m...")

    #We can already assume the manifest exists (it was checked earlier)
    testcases_path = "projects/project" + str(project_num)
    manifest_path = testcases_path + "/manifest.json"
    manifest_file = open(manifest_path)
    try:
        manifest = json.load(manifest_file)
    except json.decoder.JSONDecodeError:
        die("The manifest.json for the current project is formatted incorrectly", FIX_MANIFEST_TIP)

    manifest_file.close()

    #Ensure we found a "testcases" key in the manifest
    if not "testcases" in manifest:
        die("The manifest.json for the current project is missing a testcases array", FIX_MANIFEST_TIP)
    if len(manifest["testcases"]) == 0:
        die("No testcases are avaliable for the current project yet!", "Please contribute testcases, and do a git pull to grab the most recent ones!")

    #Check that all of the testcases in the manifest are sane and actually exist
    for testcase in manifest["testcases"]:
        if not "name" in testcase:
            die("A testcase in the manifest.json is missing a name.", FIX_MANIFEST_TIP)
        if not "author" in testcase:
            die("The \"" + testcase["name"] + "\" testcase in the manifest.json is missing an author.", FIX_MANIFEST_TIP)
        if not os.path.exists(testcases_path + "/input/" + testcase["name"] + ".in"):
            die("The input file for the \"" + testcase["name"] + "\" testcase in the manifest.json is missing", FIX_MANIFEST_TIP)
        if not os.path.exists(testcases_path + "/output/" + testcase["name"] + ".out"):
            die("The output file for the \"" + testcase["name"] + "\" testcase in the manifest.json is missing", FIX_MANIFEST_TIP)

    print("Awesome, all " + str(len(manifest["testcases"])) + " testcase(s) in the manifest exist!\n")
    return manifest["testcases"]

def project3_corpus_logic():
    print("Working around \x1b[4mcorpus licensing issues\x1b[0m for Project 3...")
    print("\x1b[4mDownloading the original corpus\x1b[0m from textfiles.com...")
    og_corpus_request = requests.get(PROJECT3_CORPUS_URL, allow_redirects=True)
    og_corpus = og_corpus_request.content.decode()

    print("Done! Modifying the corpus to \x1b[4mmatch the one on LEARN\x1b[0m...")
    learn_corpus = og_corpus
    learn_corpus = learn_corpus.replace("\n ", '\n')
    learn_corpus = learn_corpus.replace("11", 'ELEVEN')
    learn_corpus = learn_corpus.replace("25", 'TWENTY FIVE')
    learn_corpus = learn_corpus.replace("sex", 'GENDER')
    learn_corpus = learn_corpus.replace("Mac II.", "MAC")
    learn_corpus = learn_corpus.replace("512K Macs", "FIVE HUNDRED AND TWELVE KILOBYTE MACS")
    learn_corpus = learn_corpus.replace("512KE", "FIVE HUNDRED AND TWELVE")
    learn_corpus = learn_corpus.replace("512K ", "FIVE HUNDRED AND TWELVE KILOBYTES ")
    learn_corpus = learn_corpus.replace("SE, ", '')
    learn_corpus = learn_corpus.replace("the Mac IIx, Mac IIcx, and Mac IIci,", " THE OTHER TWO MACS")
    for character in "?'.\"();,!012345678":
        learn_corpus = learn_corpus.replace(character, '')
    for character in "-":
        learn_corpus = learn_corpus.replace(character, ' ')
    learn_corpus = learn_corpus.partition("*****")[0]
    learn_corpus = learn_corpus.upper()
    learn_corpus = learn_corpus[2:]
    learn_corpus = learn_corpus[:-4]

    print("Modifications successful! \x1b[4mSaving the corpus to disk\x1b[0m so your code can use it...")
    open(os.path.expanduser(TESTING_DIR) + "/" + PROJECT3_CORPUS_NAME, "w").write(learn_corpus)

    print("")

def run_testcases(project_num, testcases):
    print("Alright, we're finally getting to the good part. Let's run some testcases!")

    #Various paths we will be using later
    testcases_path = "projects/project" + str(project_num)
    testing_path = os.path.expanduser(TESTING_DIR)

    #List of failed testcases
    failed_testcases = []

    #Multiprocessing pool-related structures (limits max process to # of detected CPUs instead of launching every testcase at once)
    test_pool = multiprocessing.Pool()
    test_results_async = []

    #Launch all testcases using the pool
    testcase_num = 0
    print("Using up to " + str(multiprocessing.cpu_count()) + " thread(s) to run testcases in parallel...")
    for testcase in testcases:
        print("[Running... ]: Testcase " + str(testcase_num + 1) + " of " + str(len(testcases)) + ": \"\x1b[96m" + testcase["name"] + "\x1b[0m\", by \x1b[95m" + testcase["author"] + "\x1b[0m")
        test_results_async.append(test_pool.apply_async(run_testcase, args=(project_num, testcase)))
        testcase_num = testcase_num + 1

    #Wait for all testcases to finish, printing info about them as we go, and recording info about the ones that fail
    testcase_nums_left = []
    for testcase_num in range(len(testcases)):
        testcase_nums_left.append(testcase_num)

    while len(testcase_nums_left) != 0:
        for testcase_num in testcase_nums_left:
            if not test_results_async[testcase_num].ready():
                continue

            correct_output, mismatched_line, memory_safe, on_time, run_time = test_results_async[testcase_num].get()

            #Print the status based on that
            print("\x1b[" + str(len(testcases) - testcase_num) + "A\x1b[1C", end="")
            if not on_time:
                print("\x1b[91mTimeout  :(\x1b[0m", end="")
            elif not correct_output:
                print("\x1b[91mMismatch :(\x1b[0m", end="")
            elif not memory_safe:
                print("\x1b[93mMemory   :(\x1b[0m", end="")
            else:
                print("\x1b[92mSuccess! :)\x1b[0m", end="")
            print("\x1b[" + str(len(testcases) - testcase_num) + "B\x1b[G", end="", flush=True)

            #Add the testcase to the failed_testcases list if it failed
            if (not correct_output) or (not memory_safe) or (not on_time):
                failed_testcases.append((testcases[testcase_num]["name"], correct_output, mismatched_line, memory_safe, on_time, run_time))

            testcase_nums_left.remove(testcase_num)

        time.sleep(0.01)#Don't completely burn CPU while we are polling

    print("\x1b[90mNote: If some testcases still show as \"Running...\" at this point, this is just a display issue\x1b[0m")
    print("\x1b[90mThis usually happens if your terminal is too small or you resize it while running the script\x1b[0m\n")

    try:
        shutil.rmtree(testing_path)#We no longer need the testing directory anymore!
    except OSError:
        general_warning("Failed to remove the temporary directory " + TESTING_DIR, "Likely this is an issue with NFS; you can probably ignore this")

    return failed_testcases

def run_testcase(project_num, testcase):
    #Various paths
    testcases_path = "projects/project" + str(project_num)
    testing_path = os.path.expanduser(TESTING_DIR)

    #Open the testcase and pipe it to the process
    testcase_input_file = open(testcases_path + "/input/" + testcase["name"] + ".in")

    test_subprocess = subprocess.Popen(["valgrind", "./a.out"], stdin=testcase_input_file, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=testing_path)

    #Determine timeout time
    if "timeout_time_secs" in testcase.keys():
        #TODO ensure it is an integer
        timeout_time_secs = testcase["timeout_time_secs"]
    else:
        timeout_time_secs = DEFAULT_TIMEOUT_SECS

    #Get the stdout and stderr of the process
    try:
        test_subprocess_stdout, test_subprocess_stderr = test_subprocess.communicate(timeout=timeout_time_secs)
    except subprocess.TimeoutExpired:
        test_subprocess.kill()
        test_subprocess.wait()
        return True, -1, True, False, timeout_time_secs

    #Loop through the lines to check if stdout matches what was expected
    stdout_as_lines = test_subprocess_stdout.decode().splitlines()
    testcase_output_file = open(testcases_path + "/output/" + testcase["name"] + ".out")
    expected_output_as_lines = testcase_output_file.read().splitlines()
    testcase_output_file.close()

    correct_output = True
    mismatched_line = -1
    for i in range(len(expected_output_as_lines)):
        if (i >= len(stdout_as_lines)) or (stdout_as_lines[i].rstrip() != expected_output_as_lines[i].rstrip()):
            correct_output = False
            mismatched_line = i
            break

    #Check stderr to see if Valgrind reported any errors
    if "All heap blocks were freed -- no leaks are possible" in test_subprocess_stderr.decode() and "ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)" in test_subprocess_stderr.decode() and not "Invalid" in test_subprocess_stderr.decode() and not "uninit" in test_subprocess_stderr.decode() and not "Process terminating" in test_subprocess_stderr.decode() and not "Mismatched" in test_subprocess_stderr.decode() and not "overlap in mem" in test_subprocess_stderr.decode() and not "fishy" in test_subprocess_stderr.decode() and not "not within mapped region" in test_subprocess_stderr.decode():
        memory_safe = True
    else:
        memory_safe = False

    testcase_input_file.close()

    return correct_output, mismatched_line, memory_safe, True, timeout_time_secs#TODO replace last with total running time up to this point

def summarize_and_grade(uwid, project_num, testcases, failed_testcases):
    if (uwid == "jzjekel"):
        uwid = "JZJ"
    elif (uwid == "abfoxive"):
        uwid = "Aiden"
    elif (uwid == "fmirshek"):
        uwid = "Farzan"
    elif (uwid == "laledes"):
        uwid = "Luc"

    if len(failed_testcases) == 0:
        if (uwid == "JZJ"):
            print("\x1b#6\x1b#3\x1b[92;5;1mCongratulations " + uwid + "!\x1b[0m")
            print("\x1b#6\x1b#4\x1b[92;5;1mCongratulations " + uwid + "!\x1b[0m")
            print("\x1b[92mYou passed every testcase I have for Project " + str(project_num) + " with flying colors!\x1b[0m")
        else:
            print("\x1b[92;5;1mCongratulations " + uwid + "!\x1b[0m\x1b[92m You passed every testcase I have for Project " + str(project_num) + " with flying colors!\x1b[0m")
    else:
        recoverable_project_mistake("At least one of the testcases was unsuccessful", "Try to run the problematic testcases manually to narrow down the issue in your code")
        print("\nHere is some additional info about failed testcases:")
        for testcase_info in failed_testcases:
            print("Testcase \x1b[96m" + testcase_info[0] + "\x1b[0m failed due to ", end="")
            if not testcase_info[1]:
                print("\x1b[91man output mismatch on line " + str(testcase_info[2]) + "\x1b[0m", end="")
                if not testcase_info[3]:
                    print(", and \x1b[93mmemory unsafety\x1b[0m")
                else:
                    print("")
            elif not testcase_info[3]:
                print("\x1b[93mmemory unsafety\x1b[0m")
            elif not testcase_info[4]:
                print("\x1b[91mtiming out after " + str(testcase_info[5]) + " second(s)\x1b[0m")
        print("")

    print("Here is a breakdown of your grade: ")
    print("Testcases passed: \x1b[96m" + str(len(testcases) - len(failed_testcases))+ " out of " + str(len(testcases)) + "\x1b[0m")
    print("Testcases failed: \x1b[96m" + str(len(failed_testcases))+ " out of " + str(len(testcases)) + "\x1b[0m")

    failed_with_output_mismatches = 0
    failed_with_memory_unsafety = 0
    failed_with_timeout = 0
    for testcase in failed_testcases:
        if not testcase[1]:#Corresponds to mismatched output
            failed_with_output_mismatches = failed_with_output_mismatches + 1
        if not testcase[3]:#Corresponds to memory unsafety
            failed_with_memory_unsafety = failed_with_memory_unsafety + 1
        if not testcase[4]:#Corresponds to timeouts (not in on time)
            failed_with_timeout = failed_with_timeout + 1

    print("Testcases with output mismatches: \x1b[96m" + str(failed_with_output_mismatches)+ " out of " + str(len(testcases)) + "\x1b[0m")
    print("Testcases with memory unsafety: \x1b[96m" + str(failed_with_memory_unsafety)+ " out of " + str(len(testcases)) + "\x1b[0m")
    print("Testcases that timed-out: \x1b[96m" + str(failed_with_timeout)+ " out of " + str(len(testcases)) + "\x1b[0m")

    if (uwid == "JZJ"):
        print("\x1b#6\x1b#3\x1b[95mYour JekelScore(TM) is", str((float(len(testcases) - len(failed_testcases)) / float(len(testcases))) * 100) + "%\x1b[0m")
        print("\x1b#6\x1b#4\x1b[95mYour JekelScore(TM) is", str((float(len(testcases) - len(failed_testcases)) / float(len(testcases))) * 100) + "%\x1b[0m\n")
    else:
        print("\x1b[95mYour JekelScore(TM) is", str((float(len(testcases) - len(failed_testcases)) / float(len(testcases))) * 100) + " %\x1b[0m\n")

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
    testing_path = os.path.expanduser(TESTING_DIR)
    if os.path.exists(testing_path):
        try:
            shutil.rmtree(testing_path)#We no longer need the testing directory anymore!
        except OSError:
            general_warning("Failed to remove the temporary directory " + TESTING_DIR, "Likely this is an issue with NFS; you can probably ignore this")
    sys.exit(1)

def general_unrecoverable_mistake(mistake_string, tip):
    print("\x1b[90m\n---------- snip snip ----------\x1b[0m")
    print("\x1b[91;1mShoot, I might have found a mistake: \x1b[0m\x1b[91;4m" + mistake_string + "\x1b[0m")
    print("Maybe this tip will help: \x1b[92m" + tip + "\x1b[0m")
    print("\x1b[95mFrom the ashes of disaster grow the roses of success!\x1b[0m")
    testing_path = os.path.expanduser(TESTING_DIR)
    if os.path.exists(testing_path):
        try:
            shutil.rmtree(testing_path)#We no longer need the testing directory anymore!
        except OSError:
            general_warning("Failed to remove the temporary directory " + TESTING_DIR, "Likely this is an issue with NFS; you can probably ignore this")
    sys.exit(1)

def general_warning(warning_string, tip):
    print("\x1b[90m\n---------- snip snip ----------\x1b[0m")
    print("\x1b[93;1mShoot, something didn't quite work: \x1b[0m\x1b[93;4m" + warning_string + "\x1b[0m")
    print("Maybe this tip will help: \x1b[92m" + tip + "\x1b[0m")
    print("\x1b[95mDo, or do not: there is no try.\x1b[0m")
    print("\x1b[90m---------- snip snip ----------\x1b[0m")

def die(error_string, tip):
    print("\x1b[90m\n---------- snip snip ----------\x1b[0m")
    print("\x1b[91;1mShoot, an error occured: \x1b[0m\x1b[91;4m" + error_string + "\x1b[0m")
    print("Maybe this tip will help: \x1b[92m" + tip + "\x1b[0m")
    print("\x1b[95mOh a spoonful of sugar helps the medicine go down, in the most delightful way!\x1b[0m")
    testing_path = os.path.expanduser(TESTING_DIR)
    if os.path.exists(testing_path):
        try:
            shutil.rmtree(testing_path)#We no longer need the testing directory anymore!
        except OSError:
            general_warning("Failed to remove the temporary directory " + TESTING_DIR, "Likely this is an issue with NFS; you can probably ignore this")
    sys.exit(1)

#On script entry, call main()
if __name__ == "__main__":
    main()
