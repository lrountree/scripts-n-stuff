# python 3.9
# This script is intended to build an IPA server in a docker container
# EC2 Instance Host: IAM Role ec2-default
# Required Packages: python 3.9, docker 20, pip3
# Required Python Modules: docker
# Required Files: custom_docker_modules.py, genpass.py, log.py, ipa.Dockerfile, parameters.yaml

# Import Common Modules
import os, sys, yaml

# Import Custom Modules
from log import LOG
import genpass
import custom_docker_modules as CDM

# Set Up Generic Variables
Context_Path = '.'
Parameter_File = 'parameters.yaml'
Log_File = 'ipa.log'
IPA_Net = 'ipanet'

# Grab Parameter File Data
parameters = yaml.full_load(open(r'%s' %Parameter_File))

# Populate Custom Variables
Image_Version = parameters['Container_Image']
Docker_File = parameters['Docker_File']
Password_File = parameters['Password_File']
Domain_Name = parameters['Domain_Name']
Host_FQDN = parameters['Node_FQDN']
Host_Shortname = Host_FQDN.split('.')[0]
Ports = parameters['Ports']
Volumes = parameters['Volumes']
Zone_Rev_IP = parameters['Zone_Rev_IP']
Zone_Fwd_DNS = parameters['Zone_Fwd_DNS']
Realm_KRB = Zone_Fwd_DNS.upper()
IPA_Master_FQDN = parameters['Master_Nodes']['MASTER_1'][0] + '.' + Zone_Fwd_DNS

# Set Up Modules
log = LOG('IPA_Logger', Log_File, 'critical', 'info')

# Check For IPA Image, build if not found
check_image = CDM.check_image(Image_Version)
if check_image[0]:
    log.info(check_image[1])
elif check_image[1].split() == 'Failed':
    log.critical(check_image[1])
    sys.exit(1)
else:
    log.info(check_image[1])
    log.info('Building new image from dockerfile...')
    build_result = CDM.build_image(Docker_File, Image_Version, Context_Path)
    if build_result[0]:
        log.info(build_result[1])
    else:
        log.critical(build_result[1])
        sys.exit(1)

# Check for IPA Network, build if not found
net_result = CDM.create_net(IPA_Net, 'bridge', IPV6=True, SCOPE='local')
if net_result[0]:
    log.info(net_result[1])
else:
    log.critical(net_result[1])
    sys.exit(1)

# Run IPA Container
run_result = CDM.run_container(Host_FQDN, Image_Version, IPA_Net, Ports, Volumes)
if run_result[0]:
    log.info(run_result[1])
else:
    log.critical(run_result[1])
    sys.exit(1)

# Configure IPA
container_status = CDM.get_status(Host_Shortname)
if not container_status[0]:
    log.critical(container_status)
    sys.exit(1)
elif container_status[1] != 'running':
    log.critical(f'Container status: {container_status}')
    sys.exit(1)
else:
    log.info(f'Container is running')

##-generate and encrypt passwords, save encrypted passwords to local file
if not os.path.exists(Password_File):
    Get_Admin = genpass.encrypt_password(genpass.random_characters(24))
    Get_DM = genpass.encrypt_password(genpass.random_characters(24))
    yaml.dump({'admin': {'lock': Get_Admin[0], 'key': Get_Admin[1]}}, open(Password_File, 'w'))
    yaml.dump({'directorymanager': {'lock': Get_DM[0], 'key': Get_DM[1]}}, open(Password_File, 'a'))
Read_Yaml = yaml.full_load(open(Password_File, 'r'))
Admin_Block = Read_Yaml['admin']
DM_Block = Read_Yaml['directorymanager']
Admin_Password = genpass.decrypt_password(Admin_Block['lock'], Admin_Block['key'])
DM_Password = genpass.decrypt_password(DM_Block['lock'], DM_Block['key'])

##-modify filesystem for IPA
command_result = CDM.send_command(Host_Shortname, 'echo "0" > /proc/sys/fs/protected_regular')
if command_result[0]:
    log.info('Modified protected_regular file')
    command_result = CDM.send_command(Host_Shortname, 'sysctl -p')
    if command_result[0]:
        log.info('Loaded sysctl config')
    else:
        log.warning('Failed to load sysctl config')
else:
    log.warning('Could not modify protected_regular file')

##-install IPA
Install_Command = 'bash -c \''
if Host_Shortname == parameters['Master_Nodes']['MASTER_1'][0]:
    Install_Command += parameters['Master1_Command'] + ' '
    for OPT in parameters['Master1_Options']:
        if OPT.split('=')[0] == 'reverse-zone':
            Install_Command += '--' + OPT.replace('VAL', Zone_Rev_IP) + ' '
        elif OPT.split('=')[0] == 'realm':
            Install_Command += '--' + OPT.replace('VAL', Realm_KRB) + ' '
        elif OPT.split('=')[0] == 'hostname':
            Install_Command += '--' + OPT.replace('VAL', IPA_Master_FQDN) + ' '
        elif OPT.split('=')[0] == 'ds-password':
            Install_Command += '--' + OPT.replace('VAL', f'\"{DM_Password}\"') + ' '
        else:
            Install_Command += '--' + OPT + ' '
elif Host_Shortname == parameters['Master_Nodes']['MASTER_2'][0]:
    Install_Command += parameters['Replica_Command'] + ' '
    for OPT in parameters['Master2_Options']:
        Install_Command += '--' + OPT + ' '
    for OPT in parameters['Replica_Options']:
        if OPT.split('=')[0] == 'server':
            Install_Command += '--' + OPT.replace('VAL', IPA_Master_FQDN) + ' '
        elif OPT.split('=')[0] == 'principal':
            Install_Command += '--' + OPT.replace('VAL', 'admin') + ' '
        else:
            Install_Command += '--' + OPT + ' '
elif Host_Shortname == parameters['Satellite_Nodes']['SAT_1'][0] or Host_Shortname == parameters['Satellite_Nodes']['SAT_2'][0]:
    Install_Command += parameters['Replica_Command'] + ' '
    for OPT in parameters['Replica_Options']:
        if OPT.split('=')[0] == 'server':
            Install_Command += '--' + OPT.replace('VAL', IPA_Master_FQDN) + ' '
        elif OPT.split('=')[0] == 'principal':
            Install_Command += '--' + OPT.replace('VAL', 'admin') + ' '
        else:
            Install_Command += '--' + OPT + ' '
for OPT in parameters['IPA_Install_Options']:
    if OPT.split('=')[0] == 'domain':
        Install_Command += '--' + OPT.replace('VAL', Zone_Fwd_DNS) + ' '
    elif OPT.split('=')[0] == 'admin-password':
        Install_Command += '--' + OPT.replace('VAL', f'\"{Admin_Password}\"')
    else:
        Install_Command += '--' + OPT + ' '
Install_Command += '\''
command_result = CDM.send_command(Host_Shortname, Install_Command)
log.info(f'INSTALL COMMAND: {Install_Command}')
if command_result[0]:
    log.info('IPA has been successfully installed')
else:
    log.warning(f'IPA failed to install: ' + str(command_result[1]))
