git clone https://github.com/fchollet/keras.git  &&
cd /keras  &&
git checkout 46bfa18a57b9808b1cf80985c3ed72286ba6d4b0 &&
python setup.py install  &&
/usr/bin/yes | sudo pip uninstall theano  &&
sudo pip install git+git://github.com/Theano/Theano.git
