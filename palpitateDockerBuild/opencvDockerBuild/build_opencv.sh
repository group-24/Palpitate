DIRECTORY=/home/

git clone https://github.com/Itseez/opencv.git &&

mkdir /opencv/release &&
cd /opencv/release &&
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_PYTHON_SUPPORT=ON -D WITH_XINE=ON -D WITH_TBB=ON -D WITH_IPP=OFF .. &&
make && make install &&
cd /

# Leave OpenCV folder intact so we can get cascades for face detection
# rm -rf opencv
