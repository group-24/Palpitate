from palpitate/ffmpeg-image

run echo "Building Palpitate docker image"

# install flask for server
run pip install flask

run apt-get install -y -q libhdf5-serial-dev

run pip install openpyxl
run pip install xlrd
run pip install h5py

# Install Keras
run apt-get install -y -q python-numpy python-scipy
run apt-get install --upgrade python-scipy
run apt-get install -y -q libhdf5-serial-dev
add build_keras.sh /build_keras.sh
run /bin/sh /build_keras.sh
run rm -rf /build_keras.sh

run apt-get install -y -q libblas-dev liblapack-dev libatlas-base-dev gfortran
run /usr/bin/yes | pip install --upgrade scipy

run pip install tables
run pip install sklearn

WORKDIR /home

EXPOSE 5000
