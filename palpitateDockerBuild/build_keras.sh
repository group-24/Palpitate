git clone https://github.com/fchollet/keras.git  &&
cd /keras  &&
# git checkout 46bfa18a57b9808b1cf80985c3ed72286ba6d4b0 &&
# git checkout tags/0.3.0 &&
git checkout 92f66a279a3564420c9b7003f297c2fc12d40a7e &&
python setup.py install  &&
/usr/bin/yes | sudo pip uninstall theano  &&
sudo pip install git+git://github.com/Theano/Theano.git
