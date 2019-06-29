#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd ~
source ./set-secrets.sh
cd ~/gifcam
sudo python gifcam.py
cd /
