# ECE250 Testcases

This repository contains a collection of MIT-licensed testcases for each project in ECE250.

# Sweet, but how do I use them?

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

The projects/ folder contains several subdirectories, one for each project.
Within the project folder you're interested in, there is an "input" and an "output" folder.

Each file in "input" is a testcase you can run with the following command (assuming you have
Valgrind installed and your code is compiled to the binary a.out)

```
$ valgrind ./a.out < path/to/testcase.in

```

You can then compare the results to the corresponding file in the "output" folder to ensure your program produces the correct output!

In the future, I (John) will be writing an "autograder" of my own that will eventually automate this process for you (not the git clone part)!

# Contributing

By having your testcases included in this repository, you agree to having them released under the MIT License (of course you retain copyright).
You'll get a spot in the following "Contributors" section of the README for your contributions, indicating which test files are yours.

Only input files with a corresponding expected output file will be accepted for inclusion.

Just submit a PR to participate, or if you're a big enough contributor, I'll grant you maintainer status :)

# Contributors

| Contributor | Testcases contributed |
|-------------|-------------------|
| John Jekel (JZJ) | sanity, supports_double, |
