# Python 3.9
# Custom modules for docker things
# Requires: Dockerfile, docker, python3

# Import common modules
import sys, docker
from subprocess import run, PIPE

# Set up variables

# Set up Modules
client = docker.from_env()

# Check for image
def check_image(IMAGE):
    '''
    custom_docker_modules.check_image(<IMAGE>)
    IMAGE: image name and tag, like ubuntu:latest
    '''
    try:
        Check_Result = client.images.list(IMAGE)
    except:
        return False, f'Failed to check for image {IMAGE}: ' + str(sys.exc_info()[1])
    if not Check_Result:
        return False, f'Image {IMAGE} not found in local cache'
    return True, f'Image {IMAGE} already in local cache'

# Create image
def build_image(FILE, TAG, PATH):
    '''
    custom_docker_modules.build_image(<FILE>, <TAG>, <PATH>)
    FILE: name of relevant dockerfile
    TAG: image name and tag, like ubuntu:latest
    PATH: context path, where relevant files are located
    '''
    try:
        client.images.build(dockerfile = FILE, tag = TAG, path = PATH)
    except:
        return False, f'Failed to build image {TAG}: ' + str(sys.exc_info()[1])
    return True, f'Built image {TAG}'

# Check for and create network
def create_net(NAME, DRIVER, SCOPE, IPV6 = None):
    '''
    custom_docker_modules.network.create(<NAME>, <DRIVER>, <IPV6>, <SCOPE>)
    NAME: name of docker network
    DRIVER: bridge, host, overlay, macvlan, none
    IPV6: optional, enable ipv6- True, False
    SCOPE: local, global, swarm
    '''
    Ipam_Config = docker.types.IPAMConfig(pool_configs=[docker.types.IPAMPool(subnet='2001:db8:1::/64')])
    try:
        Check_Net = client.networks.get(NAME)
    except docker.errors.NotFound:
        Check_Net = 'Create'
    except:
        return False, f'Failed to check for network {NAME}: ' + str(sys.exc_info()[1])
    else:
        return True, f'Network {NAME} exists, skipping create'
    if Check_Net == 'Create':
        if IPV6 is None:
            try:
                Create_Net = client.networks.create(NAME, driver=DRIVER, scope=SCOPE)
            except:
                return False, f'Failed to create network {NAME}: ' + str(sys.exc_info()[1])
        else:
            try:
                Create_Net = client.networks.create(NAME, driver=DRIVER, enable_ipv6=IPV6, ipam=Ipam_Config, scope=SCOPE)
            except:
                return False, f'Failed to create network {NAME} with ipv6: ' + str(sys.exc_info()[1])
        return True, f'Created network {NAME}'

# Run container
def run_container(HOSTNAME, IMAGE, NET='bridge', PORTS = None, VOLS = None):
    '''
    custom_docker_modules.run_container(<HOSTNAME>, <IMAGE>, <VOLS>)
    HOSTNAME: FQDN of container
    IMAGE: image name and tag to build container from
    VOLS: optional list of volumes to mount/bind to container, use standard docker format- 
          '/source/path:/dest/path:opts', seperated by commas
    '''
    NAME = HOSTNAME.split('.')[0]
    DOMAIN = '.'.join(HOSTNAME.split('.')[1:])
    NAMESERVER = run(['grep', 'nameserver', '/etc/resolv.conf'], stdout=PIPE).stdout.decode().split()[1]
    def gen_ports(LIST):
        gen_dict = {}
        for ITEM in LIST:
            ITEM = ITEM.split(':')
            gen_dict[ITEM[0]] = ITEM[1]
        return gen_dict
    def gen_vols(LIST):
        gen_dict = {}
        for ITEM in LIST:
            ITEM = ITEM.split(':')
            if len(ITEM) > 3:
                return False, f'Too many values in container run volume option: {ITEM}'
            elif len(ITEM) == 3:
                gen_dict[ITEM[0]] = {'bind': ITEM[1], 'mode': ITEM[2]}
            else:
                gen_dict[ITEM[0]] = {'bind': ITEM[1]}
        return gen_dict
    if PORTS is None and VOLS is None:
        try:
            run_results = client.containers.run(IMAGE, \
                    detach=True, \
                    stdin_open=True, \
                    tty=True, \
                    privileged=True, \
                    dns=[NAMESERVER], \
                    dns_search=[DOMAIN], \
                    network=NET, 
                    name=NAME, \
                    hostname=HOSTNAME)
        except:
            return False, f'Failed to run container {NAME}: ' + str(sys.exc_info()[1])
    elif PORTS is not None and VOLS is None:
        Port_Dict = gen_ports(PORTS)
        try:
            run_results = client.containers.run(IMAGE, \
                    detach=True, \
                    stdin_open=True, \
                    tty=True, \
                    privileged=True, \
                    dns=[NAMESERVER], \
                    dns_search=[DOMAIN], \
                    ports=Port_Dict, \
                    network=NET, \
                    name=NAME, \
                    hostname=HOSTNAME)
        except:
            return False, f'Failed to run container {NAME}: ' + str(sys.exc_info()[1])
    elif PORTS is None and VOLS is not None:
        Vol_Dict = gen_vols(VOLS)
        if not Vol_Dict[0]:
            return False, Vol_Dict[1]
        try:
            run_results = client.containers.run(IMAGE, \
                    detach=True, \
                    stdin_open=True, \
                    tty=True, \
                    privileged=True, \
                    dns=[NAMESERVER], \
                    dns_search=[DOMAIN], \
                    volumes=Vol_Dict, \
                    network=NET, \
                    name=NAME, \
                    hostname=HOSTNAME)
        except:
            return False, f'Failed to run {NAME}: ' + str(sys.exc_info()[1])
    else:
        Port_Dict = gen_ports(PORTS)
        Vol_Dict = gen_vols(VOLS)
        try:
            run_results = client.containers.run(IMAGE, \
                    detach=True, \
                    stdin_open=True, \
                    tty=True, \
                    privileged=True, \
                    dns=[NAMESERVER], \
                    dns_search=[DOMAIN], \
                    ports=Port_Dict, \
                    volumes=Vol_Dict, \
                    network=NET, \
                    name=NAME, \
                    hostname=HOSTNAME)
        except:
            return False, f'Failed to run container {NAME}: ' + str(sys.exc_info()[1])
    if not client.containers.list(filters={'name': NAME}):
        return False, f'Container {NAME} was NOT created!'
    return True, f'Container {NAME} has been created'

# Check container status
def get_status(NAME):
    try:
        Target_Container = client.containers.get(NAME)
    except:
        return False, f'Failed to get target container: ' + str(sys.exc_info()[1])
    try:
        Container_Status = Target_Container.status
    except:
        return False, f'Failed to get container status: ' + str(sys.exc_info()[1])
    return True, Container_Status

# Execute Command on container
def send_command(NAME, COMMAND):
    '''
    custom_docker_modules.send_command(<NAME>, <COMMAND>)
    NAME: name of docker container
    COMMAND: the command to be run on the docker container
    OUTPUT: success or failure, as well as command output
    '''
    try:
        Target_Container = client.containers.get(NAME)
    except:
        return False, f'Failed to get target container: ' + str(sys.exc_info()[1])
    try:
        Command_Output = Target_Container.exec_run(COMMAND)
    except:
        return False, f'Failed to run command on {NAME}: ' + str(sys.exc_info()[1])
    if Command_Output[0] != 0:
        return False, Command_Output
    return True, Command_Output
