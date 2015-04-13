#!/usr/bin/env python

import os, sys

print "This install script will take (a very few) steps to setting up Hiroshima to work properly."
print "You will be asked to enter your password multiple times throughout the process, so don't go anywhere (not that this is a long process anyway)."

print "Moving files into the WebServer..."
os.system('sudo cp -R hiroshima-web-files /Library/WebServer/Documents/hiroshima')

print "Starting Apache (restarting if already enabled)..."
os.system('sudo apachectl restart')

print "Process complete, wasn't so bad was it? Follow the instructions in installation-instructions.md"
