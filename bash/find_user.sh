#! /bin/bash

# Written in 2016 by Lucas Rountree
# Get LDAP user info
#

# Check dependencies
check_dependency() {
clear
echo "Checking dependencies..."
DPLIST=(ldap-utils)
for DPNAME in ${DPLIST[@]}; do
  unset -v PKGSTAT
  PKGSTAT=$(dpkg -l | grep "${DPNAME}")
  if ! [[ -z "${PKGSTAT}" ]]; then
    echo -e "\e[93m${DPNAME} installed!\e[0m"
  else
    echo -e "\e[91m${DPNAME} NOT installed, run:"
    echo -e "apt-get install -f ${DPNAME}"
    echo -e "quitting...\e[0m"
    exit
  fi
done
}

# Set up variables
get_info() {
echo -en "\e[0;33m"
read -p $'\e[0;33mEnter your AD Username: \e[0m' ADUSER
read -p $'\e[0;33mEnter your AD Domain (domain.com): \e[0m' AD_DOMAIN
read -s -p $'\e[0;33mEnter your AD Password: \e[0m' ADPASS
echo -e \n
read -p $'\e[0;33mEnter LDAP Server: \e[0m' LDAP_SERVER
AD_DC_ARR=($(echo "${AD_DOMAIN}" | sed 's/\./ /g'))
AD_DC="$(for ELEMENT in "${AD_DC_ARR[@]}"; do echo -en "dc=${ELEMENT},"; done | sed 's/.$//')"
check_password
}

run_firstlast() {
read -p $'\e[0;33mFirst and Last Name: \e[0m' FLNAME
echo ""
echo -en "\e[30;37m"
if ldapsearch -LLL -x -h "${LDAP_SERVER}" -D "${ADUSER}@${AD_DOMAIN}" -w ${ADPASS} -b "${AD_DC}" "(&(objectCategory=person)(objectClass=user)(cn=${FLNAME}))" sAMAccountName mail department co description title telephoneNumber memberof 2>/dev/null | grep -i 'sAMAccountName\|mail\|department\|co\:\|description\|title\|telephoneNumber\|memberof' | cut -d ',' -f 1 | sed "s/CN=//";
then
	echo -e "\e[0m"
else
	echo -e "\e[0;31mError! User may not exist, or possible authentication issue.\e[0m"
fi
}

run_byusername() {
read -p $'\e[0;33mEnter Username: \e[0m' USERNM
echo ""
echo -en "\e[30;37m"
if ldapsearch -LLL -x -h "${LDAP_SERVER}" -D "${ADUSER}@${AD_DOMAIN}" -w ${ADPASS} -b "${AD_DC}" "(&(objectCategory=person)(objectClass=user)(sAMAccountName=${USERNM}))" displayname mail department co description title telephoneNumber memberof 2>/dev/null | grep -i 'displayname\|mail\|department\|co\:\|description\|title\|telephoneNumber\|memberof' | cut -d ',' -f 1 | sed "s/CN=//";
then
        echo -e "\e[0m"
else
        echo -e "\e[0;31mError! User may not exist, or possible authentication issue.\e[0m"
fi
}

run_groupmembers() {
read -p $'\e[0;33mEnter Group: \e[0m' GROUPNM
echo ""
echo -en "\e[30;37m"
GROUPDN=`ldapsearch -LLL -x -h "${LDAP_SERVER}" -D "${ADUSER}@${AD_DOMAIN}" -w ${ADPASS} -b "${AD_DC}" "(&(objectCategory=group)(cn=${GROUPNM}))" dn | grep dn | awk '{print $2}'`
if ldapsearch -LLL -x -h "${LDAP_SERVER}" -D "${ADUSER}@${AD_DOMAIN}" -w ${ADPASS} -b "${AD_DC}" "(&(objectCategory=user)(memberOf=${GROUPDN}))" displayName 2>/dev/null | grep displayName | awk '{$1=""; print $0}';
then
        echo -e "\e[0m"
else
        echo -e "\e[0;31mError! Group may not exist, or possible authentication issue.\e[0m"
fi
}

run_again() {
echo -en "\e[0;33m"
read -p $'Run again? y/n: \e[0m' RAYN
if [ ${RAYN} = y -o ${RAYN} = Y ]; then
  clear
  start_search
elif [ ${RAYN} = n -o ${RAYN} = N ]; then
  echo -e "\e[0m"
  exit
else
  clear
  echo "Sorry, typo?"
  run_again
fi
}

start_search() {
echo -e "\e[0;33mChoose search option:
1.) username
2.) first and last name
3.) list group members
4.) quit"
read -p $'Option: \e[0m' OPCHC
if [ ${OPCHC} = 1 ]; then
	run_byusername
	run_again
elif [ ${OPCHC} = 2 ]; then
	run_firstlast
	run_again
elif [ ${OPCHC} = 3 ]; then
	run_groupmembers
	run_again
elif [ ${OPCHC} = 4 ]; then
	echo "Quitting!"
	echo -e "\e[0m"
else
	echo "Sorry, typo?"
	start_search
fi
}

check_password() {
if [[ ! $(ldapsearch -LLL -x -h "${LDAP_SERVER}" -D "${ADUSER}@${AD_DOMAIN}" -w ${ADPASS} -b "${AD_DC}" "(&(objectCategory=person)(objectClass=user)(cn=${FLNAME}))" 2> /dev/null) ]]; then
  echo -e "\e[41;30mBad Password!\e[0;33m"
  read -p $'Try Again? [y]: \e[0m' YORN
  if [ "${YORN}" = Y -o "${YORN}" = y ]; then
    clear
    get_info
  elif [ "${YORN}" = N -o "${YORN}" = n ]; then
    echo "Quitting!"
    echo -e "\e[0m"
    exit
  else
    clear
    echo "Please choose Y or N"
    check_password
  fi
fi
}

# Run the things
check_dependency
get_info
start_search
