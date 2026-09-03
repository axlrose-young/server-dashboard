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

mem_usage(){
	free | awk '/Mem:/ {printf "%.0f%%", ($2-$7)/$2*100}'
}

mem_total(){
	free -h | awk '/Mem:/ {print $2}'
}

mem_used(){
	free -h | awk '/Mem:/ {print $3}'
}

mem_avail(){
	free -h | awk '/Mem:/ {print $7}'
}

root_storage(){
	df -h /dev/sda2 | awk 'NR==2 {print $5}'
}

root_mount(){
	df -h /dev/sda2 | awk 'NR==2 {print $6}'	
}

backup_storage(){
	df -h /dev/sdb1 | awk 'NR==2 {print $5}'	
}

backup_mount(){
	df -h /dev/sdb1 | awk 'NR==2 {print $6}'
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
pprint "Mem total" "$(mem_total)"
pprint "Mem used" "$(mem_used)"
pprint "Mem available" "$(mem_avail)"
pprint "Mem usage" "$(mem_usage)"

echo -e "\nStorage\n"
pprint "$(root_mount)" "$(root_storage) used"
pprint "$(backup_mount)" "$(backup_storage) used"

echo -e "\nNetwork\n"
pprint
