#!/bin/bash

# Quick system info

pprint(){
	printf "%-15s %s\n" "$1" "$2"
}

check_reboot(){
	if [ -f /var/run/reboot-required ];then
		echo "yes"
	else
		echo "no"
	fi
}

check_upgradable(){
	apt-get -s upgrade | grep -E "^[0-9]+ upgraded" | awk '{print $1}'
}

echo "System Info"
echo "-----------"

echo -e "OS\n"
pprint "$(uname -o)" ""
pprint "Kernel" "$(uname -r)"
pprint "Hostname" "$(hostname)"

echo -e "\nSystem Status\n"
pprint "Uptime" "$(uptime -p)"
pprint "Reboot req" "$(check_reboot)"

echo -e "\nUpdates\n"
pprint "Last Update" "$(date -r /var/log/dpkg.log "+%d-%m-%Y %H:%M:%S")"
pprint "Updates" "$(check_upgradable) available"

echo -e "\nStat\n"
pprint "Mem usage" ""
