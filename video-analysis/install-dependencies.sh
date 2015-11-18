#!/bin/sh
NC='\033[0m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'

# NAMES
OPENCV_SOURCE_DIR=usr/local
OPENCV_BUILD_DIR=opencv-build

URL="https://codeload.github.com/Itseez/opencv/zip/3.0.0"

echo ${CYAN}"Installing OpenCV..." ${NC}
curl ${URL} > opencv.zip &&
echo ${GREEN}"Download complete!" &&
echo ${CYAN}"Unzipping..!"${NC} &&
unzip opencv.zip &&
echo ${GREEN}"Unzippig complete!" &&
echo ${CYAN}"Building Build Directory"${NC} &&
mkdir ${OPENCV_BUILD_DIR} &&
cd ${OPENCV_BUILD_DIR} &&
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ../${OPENCV_SOURCE_DIR} &&
echo ${GREEN}"Build Directory Created!" &&
echo ${CYAN}"Compiling and installing"${NC} &&
make &&
make install &&
echo ${GREEN}"Complete!"
