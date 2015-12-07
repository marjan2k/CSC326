#!/bin/bash
export DEBIAN_FRONTEND=noninteractive
echo "Running installation script"
echo "Installing git.."
sudo apt-get install -y git
echo "Installing gcc..."
sudo apt-get update -y
echo -ne '\n' | apt-get upgrade -y
sudo apt-get install -y build-essential
echo "Installing python-dev..."
sudo apt-get install -y python-dev
echo "Installing pip.."
sudo apt-get install -y python-pip
echo "Installing MongoDB.."
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
sudo apt-get update -y
sudo apt-get install -y mongodb-org
echo "Run MongoDB"
sudo service mongod start
echo "Cloning package from github"
sudo git clone "https://github.com/nayeemzen/CSC326.git"
sudo chmod -R 777 CSC326/
cd CSC326/lab
sudo pip install setuptools 'cython>=0.23.4' git+git://github.com/gevent/gevent.git#egg=gevent
sudo pip install -r requirements.txt
python crawler.py
python server.py