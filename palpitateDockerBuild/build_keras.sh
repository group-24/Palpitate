git clone https://github.com/fchollet/keras.git  &&
cd /keras  &&
python setup.py install  &&
/usr/bin/yes | sudo pip uninstall theano  &&
sudo pip install git+git://github.com/Theano/Theano.git
