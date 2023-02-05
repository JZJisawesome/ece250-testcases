# ECE250 Testcases

This repository contains a collection of MIT-licensed testcases for each project in ECE250.

| Project | Number Of Testcases Available |
|---------|-------------------------------|
| Project 1 | 21 (20 active in manifest) |
| Project 2 | 21 (21 active in manifest) |
| Project 3 | 0 |
| Project 4 | 0 |


# Sweet, but how do I use them?

Follow through the instructions in the "Setup" section, then actually test your project by following the "Automatic Testing" section.

## Setup

As recommended time and time again by the teaching staff, it is highly recommended you do your testing from an eceubuntu server.
Steps to connect to such a server are beyond the scope of this README.

Once you're logged into an eceubuntu server (or a local Unix/Linux system of your own), clone this repository:

```
$ git clone https://github.com/JZJisawesome/ece250-testcases
Cloning into 'ece250-testcases'...
remote: Enumerating objects: 12, done.
remote: Counting objects: 100% (12/12), done.
remote: Compressing objects: 100% (8/8), done.
remote: Total 12 (delta 1), reused 8 (delta 0), pack-reused 0
Receiving objects: 100% (12/12), done.
Resolving deltas: 100% (1/1), done.
```

If you already have a checkout but want to get the latest testcases and AutoGrader fixes, you can do this instead (from within your previous clone):

```
$ git pull
remote: Enumerating objects: 49, done.
remote: Counting objects: 100% (49/49), done.
remote: Compressing objects: 100% (19/19), done.
remote: Total 33 (delta 17), reused 30 (delta 14), pack-reused 0
Unpacking objects: 100% (33/33), 6.58 KiB | 612.00 KiB/s, done.
From https://github.com/JZJisawesome/ece250-testcases
   beb9fdb..2c1b6de  main                 -> origin/main
[...]
```

## Automatic Testing

The autograder implementation included in this repo, called the Jekel AutoGrader, **must be run from the repo root directory**.
Note down the path to your submission tarball, and open a terminal **in the root of the repo**. You can then test your tarball with

```
$ python3 ./jekelautograder.py path/to/your/tarball/example_p1.tar.gz
     _      _        _      _         _         ____               _
    | | ___| | _____| |    / \  _   _| |_ ___  / ___|_ __ __ _  __| | ___ _ __
 _  | |/ _ \ |/ / _ \ |   / _ \| | | | __/ _ \| |  _| '__/ _` |/ _` |/ _ \ '__|
| |_| |  __/   <  __/ |  / ___ \ |_| | || (_) | |_| | | | (_| | (_| |  __/ |
 \___/ \___|_|\_\___|_| /_/   \_\__,_|\__\___/ \____|_|  \__,_|\__,_|\___|_|
Copyright (c) 2023 John Jekel and Aiden Fox Ivey

Performing some basic sanity checks before we get started...
Looking good, I think I'm set to go!

To begin, let's check your tarball's file name and path...
Excellent! Based on the name of the tarball, example_p1.tar.gz, I've deduced the following:
Your UWID is: example
Your tarball is for: Project 1
[...]
```

The autograder will then test your tarball not only on the testcases for the correct project, but it will also check some other things:

- That the tarball is named correctly (it must be in order for the script to successfully infer the project version)
- That your design document is present and named correctly (matches the uwid in your tarball's name, etc.)
- That your Makefile is present and successfully produces an a.out file
- That you didn't accidentally include a precompiled a.out file in your tarball
- That your tarball dosn't contain any directories

Just like the real thing, the autograder will use Valgrind, so it is quite good at catching mistakes!

(It uses Leaks on MacOS)

## Manual Testing

This is useful if you are debugging an issue with your code that is triggered by a particular test case

The projects/ folder contains several subdirectories, one for each project.
Within the project folder you're interested in, there is an "input" and an "output" folder.

Each file in "input" is a testcase you can run with the following command (assuming you have
Valgrind installed and your code is compiled to the binary a.out)

```
$ valgrind ./a.out < path/to/testcase.in
[...]
```

You can then compare the results to the corresponding file in the "output" folder to ensure your program produces the correct output!

TODO instructions for manual testing with Leaks

# Contributing

By having your testcases included in this repository, you agree to having them released under the MIT License (of course you retain copyright).
You'll get a spot in the following "Contributors" section of the README for your contributions, indicating which test files are yours.

Only input files with a corresponding expected output file will be accepted for inclusion.

Just **submit a PR** to participate, or if you're a big enough contributor, I'll grant you maintainer status :)

# Contributors

## Jekel AutoGrader

| Contributor |
|-------------|
| Aiden Fox Ivey |
| John Jekel |

## Project 1

| Contributor | Number Of Testcases Contributed | Testcase Names |
|-------------|---------------------------------|-------|
| Azizul Chowdhury | 1 | test_REM |
| ChatGPT (with manual fixes) | 3 | chatgpt_autogenerated_0, chatgpt_autogenerated_1, chatgpt_autogenerated_2 |
| Chris (HyperFire12#3764) | 1 | specificboy |
| ECE 250 Teaching Staff | 3 | LEARN_test01, LEARN_test02, LEARN_test03 |
| Farzan Mirshekari | 3 | ECE250-Projects-Testcases_test04, ECE250-Projects-Testcases_test05, ECE250-Projects-Testcases_test06 |
| John Jekel (JZJ) | 6 | insanity, list_size_1, pushpop_yum, sanity, supports_double, support_valid_cpp_names |
| Luc Edes | 1 | delete |
| Nathan Cheng | 1 | edge_cases |
| Nick Chan | 1 | doingstuff |
| Tri Dao | 1 | test_DEF |

## Project 2

| Contributor | Number Of Testcases Contributed | Testcase Names |
|-------------|---------------------------------|-------|
| ChatGPT (with manual fixes) | 2 | chatgpt_autogenerated_0, chatgpt_autogenerated_1 |
| ECE 250 Teaching Staff | 4 | LEARN_test01open, LEARN_test01ordered, LEARN_test02ordered, LEARN_test03ordered |
| Farzan Mirshekari | 3 | ECE250-Projects-Testcases_test02open, ECE250-Projects-Testcases_test03open, ECE250-Projects-Testcases_test04ordered |
| John Jekel (JZJ) | 8 | insanity_open, insanity_ordered, integer_limits_open, integer_limits_ordered, oob_open, oob_ordered, printer, respect_capacity_open, respect_capacity_ordered, sanity_open, sanity_ordered |
| Ryan (RyEggGit) | 1 | linkingtest |
