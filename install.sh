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

echo "Installing tweepy..."
pip install tweepy --upgrade

echo "Installing python-instagram..."
pip install python-instagram --upgrade

echo "Process complete, wasn't so bad was it? Follow the instructions in installation-instructions.md"
