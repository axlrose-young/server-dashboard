#!/bin/bash

# Script to check disk health

echo "Checking /dev/sda disk..."
if smartctl -H /dev/sda | grep -q "PASSED";then
	echo "healthy"
	echo
else 
	echo "/dev/sda disk: warning"
	echo
fi

echo "Checking /dev/sdb disk..."
if smartctl -H /dev/sdb | grep -q "PASSED";then
	echo "healthy"
	echo
else 
	echo "/dev/sdb disk: warning"
	echo
fi
