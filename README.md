Palpitate - Machine Learning thingy

[![Build Status](https://travis-ci.org/group-24/Palpitate.svg?branch=master)](https://travis-ci.org/group-24/Palpitate)

Java code should go into src/main/java. Tests should go into src/test/java.

Use gradle (http://gradle.org/) to build and run the project. Use gradle check command to compile and run the project. This ensures compatibility with TravisCI. IntelliJ (and presumably other IDEs) can be configured to use gradle.
Do not submit pull requests before running tests and running gradle check as they will not be accepted and will waste time.

Code reviews/workflow - https://guides.github.com/introduction/flow/
Ensure that you submit pull requests from a forked project and on a specific branch

Travis CI docs - http://docs.travis-ci.com/

FileSystemDataBase can be used to get the BCM data. It relies on the following folder structure
<path_passed_in>/Subject(\d+)/BPM.txt and <path_passed_in>/Subject(\d+)/.*close.wav . An example
for the purposes of unit tests is found in exampleData.

DO NOT COMMIT LARGE FILES TO GIT

Git commit rules:

-1st line of max 70 characters - brief summary of the commit
-empty line
-(optional) Longer description of the aims this commit is trying to do

Make the commit message comform to the sentance. If this commit is applied it will ...
