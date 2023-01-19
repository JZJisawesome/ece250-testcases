# ECE250 Testcases

This repository contains a collection of MIT-licensed testcases for each project in ECE250.

# Sweet, but how do I use them?

Follow through the instructions in the "Setup" section, then actually test your project by following the "Manual Testing" or "Automatic Testing" sections based on your preference.

## Setup

As recommended time and time again by the teaching staff, it is highly recommended you do your testing from an eceubuntu server.
Steps to connect to such a server is beyond the scope of this README.

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

## Manual Testing

The projects/ folder contains several subdirectories, one for each project.
Within the project folder you're interested in, there is an "input" and an "output" folder.

Each file in "input" is a testcase you can run with the following command (assuming you have
Valgrind installed and your code is compiled to the binary a.out)

```
$ valgrind ./a.out < path/to/testcase.in
[...]
```

You can then compare the results to the corresponding file in the "output" folder to ensure your program produces the correct output!

## Automatic Testing

In the future, I will be writing an "autograder" of my own that will eventually automate this process for you (not the git clone part)!
So the following steps will be roughly how it works once it is implemented.

The autograder implementation included in this repo, called the Jekel AutoGrader, must be run from the project root directory.
Note down the path to your submission tarball, and open a terminal in the root. You can then test your tarball with

```
$ python3 jekelautograder.py path/to/your/tarball/example_p1.tar.gz
     _      _        _      _         _         ____               _
    | | ___| | _____| |    / \  _   _| |_ ___  / ___|_ __ __ _  __| | ___ _ __
 _  | |/ _ \ |/ / _ \ |   / _ \| | | | __/ _ \| |  _| '__/ _` |/ _` |/ _ \ '__|
| |_| |  __/   <  __/ |  / ___ \ |_| | || (_) | |_| | | | (_| | (_| |  __/ |
 \___/ \___|_|\_\___|_| /_/   \_\__,_|\__\___/ \____|_|  \__,_|\__,_|\___|_|
Copyright (c) 2023 John Jekel

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

Just like the real thing, the autograder will use valgrind, so it is quite comprehensive at catching mistakes!

# Contributing

By having your testcases included in this repository, you agree to having them released under the MIT License (of course you retain copyright).
You'll get a spot in the following "Contributors" section of the README for your contributions, indicating which test files are yours.

Only input files with a corresponding expected output file will be accepted for inclusion.

Just submit a PR to participate, or if you're a big enough contributor, I'll grant you maintainer status :)

# Contributors

## Project 1

| Contributor | Testcases contributed |
|-------------|-------------------|
| John Jekel (JZJ) | sanity, supports_double, |
