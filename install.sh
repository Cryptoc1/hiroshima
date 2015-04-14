#!/bin/bash

echo "This install script will take (a very few) steps to setting up Hiroshima to work properly."
echo "You will be asked to enter your password multiple times throughout the process, so don't go anywhere (not that this is a long process anyway)."

if [ -d "/Library/WebServer/Documents/hiroshima" ]; then
	echo "Deleting old files..."
	sudo rm -rf /Library/WebServer/Documents/hiroshima
fi

echo "Moving files into the WebServer..."
sudo cp -R web-files /Library/WebServer/Documents/hiroshima

echo "Starting Apache (restarting if already enabled)..."
sudo apachectl restart

echo "Installing dependencies..."

echo "Installing python-twitter..."
pip install python-twitter --upgrade
if [ -d "./python-twitter" ]; then
	echo "Deleting old clone..."
	rm -rf ./twitter
fi
echo "Cloning python-twitter..."
git clone http://github.com/bear/python-twitter.git
if [ -d "./twitter" ]; then
	echo "Deleting old copy of python-twitter..."
	rm -rf ./twitter
fi
echo "Moving python-twitter/twitter to ./twitter..."
mv python-twitter/twitter ./

echo "Installing python-instagram..."
pip install python-instagram --upgrade
if [ -d "./python-instagram" ]; then
	echo "Deleting old clone..."
	rm -rf ./python-instagram
fi
echo "Cloning python-instagram..."
git clone https://github.com/instagram/python-instagram.git
if [ -d "./instagram" ]; then
	echo "Deleting old copy of python-instagram..."
	rm -rf ./instagram
fi
echo "Moving python-instagram/instagram to ./instagram..."
mv python-instagram/instagram ./instagram


echo "Process complete, wasn't so bad was it? Follow the instructions in installation-instructions.md"
