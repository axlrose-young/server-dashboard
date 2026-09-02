#!/bin/bash

# Perfoms system updates
# Script run using sudo which removes redudant sudo usage

apt update
apt upgrade -y
apt autoremove -y
apt autoclean 
