#!/bin/bash
CONTAINER_OPENCV=/opencv/
source test_utilities/functions.sh
source test_utilities/try.sh

# look at test_utilities/try.sh for help on how to write tests

step "Running Data Extraction Tests:"
try cd data_analysis/test
try python *.t.py
try cd ../..
next

step "running video analysis tests"
try cd video_analysis
try python *.t.py $CONTAINER_OPENCV
try cd ..
next

# If any tests fail, this will fail Travis
exit $ERROR_OCCURED
