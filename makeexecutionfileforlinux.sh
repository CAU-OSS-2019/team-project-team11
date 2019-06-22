#!/bin/sh

echo " installing python3 "
sudo apt-get install python3

echo " apt-get update "
sudo apt-get update

echo " upgrading python3 "
sudo apt-get upgrade python3

echo " installing pyQT5 "
sudo apt-get install python-pyqt5
sudo apt-get install python3-pyqt5

echo " installing pip and pip3 "
sudo apt-get install python-pip
sudo apt-get install python3-pip

echo " installing modules "
pip install cmake dlib opencv-python face_recognition numpy

echo " setting PATH and PYTHONPATH for modules "
export PATH="${PATH}:/usr/local/lib/python2.7/dist-packages"
export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/python2.7/dist-packages"

sudo chmod +x face_recog\&mosaic.py

cd OSS_UI/
sudo chmod +x *
cd ..

cd face_mosaic\&track/
sudo chmod +x *
cd ..

cd nsfw_trian/
sudo chmod +x *
cd ..

echo " make an execution file in a dist folder "
sudo pyinstaller 'face_recog&mosaic.py' -F
