#!/bin/bash

# Perfoms system updates
# Script run using sudo which removes redudant sudo usage

apt-get update
apt-get upgrade -y
apt-get autoremove -y
apt-get autoclean 
