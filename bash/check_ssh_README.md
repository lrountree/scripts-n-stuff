# check_ssh README file

## Info
Script will read hosts from a file and check each for:
1) ssh key works
2) openssh version is current, if not update
3) ssh authentication is restricted to key

Script will iterate through each host line in the file, errors for each host will be printed to the terminal and sent to a log file.

## Running from terminal
bash check_ssh.sh [optional host file]

#### Optional Host File
This is the path to a file, useful for git repos etc where up to date host files are kept.
Default file is: ./hosts.txt

#### Compatibility
This script will run on systems with yum, apt, and pacman package managers.

#### Dependencies
None beyond standard Linux systems.
