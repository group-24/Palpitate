from ubuntu:latest

run echo "Building Palpitate docker image" 

run apt-get update
run apt-get install -y -q wget curl
run apt-get install -y -q build-essential
run apt-get install -y -q cmake
run apt-get install -y -q python2.7 python2.7-dev
run wget 'https://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11-py2.7.egg' && /bin/sh setuptools-0.6c11-py2.7.egg && rm -f setuptools-0.6c11-py2.7.egg

# insall pip
run apt-get install -y -q python-setuptools python-dev build-essential 
run easy_install pip 
run pip install --upgrade pip

# install numpy for OpenCV
run pip install numpy
run apt-get install -y -q libavformat-dev libavcodec-dev libavfilter-dev libswscale-dev
run apt-get install -y -q libjpeg-dev libpng-dev libtiff-dev libjasper-dev zlib1g-dev libopenexr-dev libxine-dev libeigen3-dev libtbb-dev

# install flask for server
run pip install flask

# install git
run apt-get install -y -q git

# run build_opencv.sh script in container
add build_opencv.sh /build_opencv.sh
run /bin/sh /build_opencv.sh
run rm -rf /build_opencv.sh

EXPOSE 5000
