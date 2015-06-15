#!/bin/bash

echo "This install script will take (a very few) steps to setting up Hiroshima to work properly.";
echo "You will be asked to enter your password multiple times throughout the process, so don't go anywhere (not that this is a long process anyway).";

echo "Setting up the Server stuff...";
if [ -d "/Library/WebServer/Documents/hiroshima" ]; then
	echo "[-] Deleted old file";
	sudo rm -rf /Library/WebServer/Documents/hiroshima;
fi

echo "[+] Copied new files";
sudo cp -R web-files /Library/WebServer/Documents/hiroshima;

echo "[!] Restarting Apache, so changes take affect";
sudo apachectl restart;


echo "Installing dependencies...";

pip install tweepy --upgrade;
echo "[+] tweepy installed";

pip install python-instagram --upgrade;
echo "[+] python-instagram installed";

pip install mechanize --upgrade;
echo "[+] mechanize installed";

echo "Setting up default configuration files..."
if [ -f "~/.config/hiroshima/hiroshima.cfg" ]; then
  echo "[!] ~/.config/hiroshima/hiroshima.cfg already exists, would you like to overwrite, or backup? (overwrite/backup)";
  read input;
  if ["$input" = "backup"]; then
    cp ~/.config/hiroshima/hiroshima.cfg ~/.config/hiroshima/_hiroshima.cfg;
    echo "[+] Backup created at ~/.config/hiroshima/_hiroshima.cfg";
  fi

  if [ "$input" = "overwrite" ]; then
    rm -rf ~/.config/hiroshima/hiroshima.cfg;
    echo "[-] ~/.config/hiroshima/hiroshima.cfg deleted";
  fi

  cp default.cfg ~/.config/hiroshima/hiroshima.cfg;
  echo "[+] default.cfg copied to ~/.config/hiroshima/ as hiroshima.cfg";
fi

echo "Copying hiroshima..."
if [ -f "/usr/bin/hiroshima" ]; then
  echo "[!] /usr/bin/hiroshima already exists, overwrite? (y/n)";
  read input;
  if [ "$input" = "y" ]; then
    sudo cp hiroshima.py /usr/bin/hiroshima;
    echo "[+] hiroshima.py copied to /usr/bin as hiroshima";
  else
    echo "Okay, exiting.";
    exit;
  fi
else
  sudo cp hiroshima.py /usr/bin/hiroshima;
  echo "[+] hiroshima.py copied to /usr/bin as hiroshima"
fi


echo "Process complete, wasn't so bad was it? Make sure to check instructions.md."
