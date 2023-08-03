#! /bin/bash

# This script will make the following checks against remote linux servers listed in hosts.txt:
# 1.) ensure hosts are running the latest version of ssh
# 2.) ensure only ssh key authentication is possible

# Command:
# bash check_ssh.sh <optional host file>

# Set up variables
User_Name="developer"
Date="$(date +%m%d%y)"
if [ "${1}" ]; then
	Host_File="${1}"
else
	Host_File="./hosts.txt"
fi
Key_File="~/.ssh/developer_key"
Log_File="./check_ssh_${Date}.log"
PKG_List=(yum apt pacman)

touch "${Log_File}"

# Set up functions
log() { # log function to print to terminal and append to log file
	Time="$(date +%H%M%S)"
	echo "${1}"
	echo "[${Time}]: ${1}" >> "${Log_File}"
}

get_package_manager() { # ssh into remote host and find package manager
	Input=("${@}")
	local _set_var=${Input[0]}
	Command=("${Input[@]:1}")
	for PKG in "${PKG_List[@]}"; do
		exit_code="$("${Command[@]}" "${PKG}" --version 2&>/dev/null && echo "${?}")"
		if [ "${exit_code}" == "0" ]; then
			local VAR1="${PKG}"
		fi
	 done
	if [ "${VAR1}" ]; then
		eval $_set_var="${VAR1}"
	fi
}

check_ssh_version() { # update package index and update openssh if needed to ensure version is current NOTE: this will require permissions
	Input=("${@}")
	local _set_var="${Input[0]}"
	PKG="${Input[1]}"
	Command=("${Input[@]:2}")
	case "${PKG}" in
		yum)
			"${Command[@]}" yum check-update -y
			"${Command[@]}" yum update openssh -y
		;;
		apt)
			"${Command[@]}" apt update -y
			"${Command[@]}" apt install openssh -y
		;;
		pacman)
			"${Command[@]}" pacman -Sy
			"${Command[@]}" pacman -S --needed openssh -y
		;;
	esac
	eval $_set_var="${?}"
}

# Check for ssh key
if [ ! -f "${Key_File}" ]; then
	log "Key File: ${Key_File} NOT found! Quitting."
	exit 1
fi
# Check for hosts file
if [ ! -f "${Host_File}" ]; then
	log "Host File: ${Host_File} NOT found! Quitting."
	exit 1
fi

# iterate through hosts file and perform functions on each host
while read -r LINE; do
	ssh_command=(ssh -q "${Key_File}" "${User_Name}@${LINE}")
	"${ssh_command[@]}" exit
	if [ "${?}" != "0" ]; then
		log "SSH Key File: ${Key_File} FAILED on host ${LINE}!"
		continue
	fi
	get_package_manager Package_Manager "${ssh_command[@]}"
	if [ "${Package_Manager}" ]; then
		check_ssh_version exit_code "${Package_Manager}" "${ssh_command[@]}"
		if [ "${exit_code}" != "0" ]; then
			log "Failed to confirm ssh version on host ${LINE}!"
		fi
		if [ ! "$("${ssh_command[@]}" grep -e '"^PasswordAuthentication no"' "/etc/ssh/sshd_config")" &>/dev/null ]; then
			log "SSH password auth is ENABLED on ${LINE}!"
		fi
	else
		log "Could not find package manager for host: ${LINE}!"
	fi
	
done < "${Host_File}"

