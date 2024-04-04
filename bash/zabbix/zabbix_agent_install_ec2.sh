#! /bin/bash
#
# This script is intended to install the Zabbix Agent, version 2
# Maintained By: Lucas Rountree (lucas.rountree@rhombuspower.com)
#
# Command:
# sudo bash zabbix_agent_install_ec2.sh <ip address> <region> <purpose> <company>
# Example:
# sudo bash zabbix_agent_install_ec2.sh 10.0.9.219 .us-west-2 dev thiscompany
#
# Set up variables
al2_agent_url="https://repo.zabbix.com/zabbix/6.4/rhel/7/x86_64/zabbix-release-6.4-1.el7.noarch.rpm"
al2023_agent_url="https://repo.zabbix.com/zabbix/6.4/rhel/9/x86_64/zabbix-release-6.4-1.el9.noarch.rpm"
zabbix_server_ip="10.0.1.165"
help_line="Usage: sudo bash zabbix_agent_install_ec2.sh <ip address> <region> <purpose> <company>"
os_name=$(grep ^NAME /etc/os-release | cut -d '=' -f2 | tr -d '"')
os_version=$(grep ^VERSION= /etc/os-release | cut -d '=' -f2 | tr -d '"')
host_ip="${1}"
if [ -z "${host_ip}" ]; then
    echo "No host ip set!"
    echo "${help_line}"
    exit 1
fi
meta_region="${2}"
if [ -z "${meta_region}" ]; then
    echo "No region set!"
	echo "${help_line}"
    exit 1
fi
meta_purpose="${3}"
if [ -z "${meta_purpose}" ]; then
    echo "No purpose set!"
	echo "${help_line}"
    exit 1
fi
meta_company="${4}"
if [ -z "${meta_company}" ]; then
    echo "No company set!"
	echo "${help_line}"
    exit 1
fi
#
# Install Repository and Agent
if [ "${os_name}" == "Amazon Linux" ]; then
	if [ "${os_version}" == "2" ]; then
		rpm -Uvh "${al2_agent_url}" || { echo "Failed to install Zabbix agent repository! Run updates? Check version?"; exit 1; }
		yum clean all || { echo "Failed to clean yum!"; exit 1; }
		yum install zabbix-agent2 zabbix-agent2-plugin-* || { echo "Failed to install Zabbix agent via yum!"; exit 1; }
	elif [ "${os_version}" == "2023" ]; then
		rpm -Uvh "${al2023_agent_url}" || { echo "Failed to install Zabbix agent repository! Run updates? Check version?"; exit 1; }
		dnf clean all || { echo "Failed to clean dnf!"; exit 1; }
		dnf install zabbix-agent2 zabbix-agent2-plugin-* || { echo "Failed to install Zabbix agent via dnf!"; exit 1; }
	else
		echo "Currently only works on Amazon Linux version 2 and 2023 AMIs!"
		exit 1
	fi
else
        echo "Currently only works on Amazon Linux AMIs!"
        exit 1
fi
#
# Set Up Config File
systemctl stop zabbix-agent2.service || { echo "Failed to stop Zabbix agent!"; exit 1; }
cp /etc/zabbix/zabbix_agent2.conf /etc/zabbix/zabbix_agent2.conf.bak || { echo "Failed to back up Zabbix agent config file!"; exit 1; }
touch /etc/zabbix/zabbix_agent2.conf || { echo "Failed to create Zabbix agent config file!"; exit 1; }
echo "PidFile=/run/zabbix/zabbix_agent2.pid 
LogFile=/var/log/zabbix/zabbix_agent2.log
LogFileSize=10
SourceIP=${host_ip}
Server=${zabbix_server_ip}
ListenPort=10050
ListenIP=${host_ip}
ServerActive=${zabbix_server_ip}
HostnameItem=system.hostname
HostMetadata=virtual machine:os=linux:environment=aws ec2:region=${meta_region}:purpose=${meta_purpose}:company=${meta_company}:
Include=/etc/zabbix/zabbix_agent2.d/*.conf
PluginSocket=/run/zabbix/agent.plugin.sock
ControlSocket=/run/zabbix/agent.sock
AllowKey=system.run[*]
Include=./zabbix_agent2.d/plugins.d/*.conf" > /etc/zabbix/zabbix_agent2.conf || { echo "Failed to populate Zabbix agent config file!"; exit 1; }
systemctl start zabbix-agent2.service || { echo "Failed to start Zabbix agent!"; exit 1; }
systemctl enable zabbix-agent2.service || { echo "Failed to enable Zabbix agent!"; exit 1; }
