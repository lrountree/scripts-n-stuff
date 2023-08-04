# General EC2 tool modules
# Maintained by: Lucas Rountree (lredvtree@gmail.com)

## Import Modules
# General
import sys
# AWS
import boto3, botocore

class ec2_get_info:
    '''
    ec2 modules
    set session first, call ec2 with session:
    session = general_modules.set_session(PROFILE, REGION)
    ec2 = general_modules.ec2(session)
    '''

    def __init__(self, session):
        self.ec2_client = session.client('ec2')

    def get_regions(self):
        '''
        Return a list of all regions
        '''
        try:
            response = [X['RegionName'] for X in self.ec2_client.describe_regions()['Regions']]
        except:
            return False, str(sys.exc_info()[1])
        return True, response

    def list_all_instances(self):
        '''
        Return a list of dictonary items containing name:id of all instances
        '''
        try:
            grab_data = self.ec2_client.describe_instances()['Reservations']
        except:
            return False, str(sys.exc_info()[1])
        response = []
        for ITEM in grab_data:
            for INSTANCE in ITEM['Instances']:
                name_id = False
                for NAME in INSTANCE['Tags']:
                    if NAME['Key'] == 'Name':
                        name_id = [NAME['Value'], INSTANCE['InstanceId']]
                if not name_id:
                    response.append(['', INSTANCE['InstanceId']])
                else:
                    response.append(name_id)
        return True, response

    def list_all_internet_gateways(self):
        '''
        Return a list of dictionary items containing name:id of all internet gateways
        '''
        try:
            grab_igws = self.ec2_client.describe_internet_gateways()['InternetGateways']
        except:
            return False, str(sys.exc_info()[1])
        response = []
        for ITEM in grab_igws:
            name_id = 'No_Name'
            for NAME in ITEM['Tags']:
                if NAME['Key'] == 'Name':
                    name_id = NAME['Value']
            response.append({name_id, ITEM['InternetGatewayId']})
        return True, response

    def list_all_nat_gateways(self):
        '''
        Return a list of dictionary items containing name:id of all nat gateways
        '''
        try:
            grab_nats = self.ec2_client.describe_nat_gateways()['NatGateways']
        except:
            return False, str(sys.exc_info()[1])
        response = []
        for ITEM in grab_nats:
            name_id = 'No_Name'
            for NAME in ITEM['Tags']:
                if NAME['Key'] == 'Name':
                    name_id = NAME['Value']
                response.append({name_id, ITEM['NatGatewayId']})
        return True, response

    def instance_info_by_name(self, NAME):
        '''
        Return instance json by using Name tag
        NAME = value of Name tag
        TIP: use wildcard on either end to match part of the Name tag
        '''
        try:
            response = self.ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [NAME]}])['Reservations']
        except:
            return False, str(sys.exc_info()[1])
        if not response:
            return False, 'No instance named ' + NAME + ', value is case sensative!'
        return True, response

    def instance_info_by_id(self, ID):
        '''
        Return instance json by instance ID
        ID = Instance ID
        '''
        try:
            response = self.ec2_client.describe_instances(Filters=[{'Name': 'instance-id', 'Values': [ID]}])['Reservations']
        except:
            return False, str(sys.exc_info()[1])
        return True, response

    def instance_info_by_ip(self, IP):
        '''
        Return instance json by private or public IP
        IP = private IP address
        '''
        try:
            response = self.ec2_client.describe_instances(Filters=[{'Name': 'private-ip-address', 'Values': [IP]}])['Reservations']
        except:
            return False, str(sys.exc_info()[1])
        if not response:
            try:
                response = self.ec2_client.describe_instances(Filters=[{'Name': 'network-interface.association.public-ip', 'Values': [IP]}])['Reservations']
            except:
                return False, str(sys.exc_info()[1])
        return True, response

    def find_ami_name(self, OWNER, ARCH, PUB, NAME):
        '''
        Return list of AMI IDs that match search filter NAME
        OWNER = Owner account ID
        ARCH = Image architecture value, options: i386, x86_64, arm64
        PUB = Wether the image is public or not, options: true, false
        NAME = String to match with filter Name
        '''
        try:
            response = self.ec2_client.describe_images(Owners=[OWNER], Filters=[{'Name': 'architecture', 'Values': [ARCH]}, {'Name': 'is-public', 'Values': [PUB]}, {'Name': 'state', 'Values': ['available']}, {'Name': 'name', 'Values': [NAME]}])['Images']
        except:
            return False, str(sys.exc_info()[1])
        return True, response

    def get_volumes(self, ID):
        '''
        Return a list of volumes attached to instance ID
        ID = Instance ID
        '''
        try:
            response = self.ec2_client.describe_volumes(Filters=[{'Name': 'attachment.instance-id', 'Values': [ID]}])['Volumes']
        except:
            return False, str(sys.exc_info()[1])
        return True, response

class ec2(ec2_get_info):
    
    def __init__(self, session):
        ec2_get_info.__init__(self, session)
        self.session = session
        self.ec2_client = session.client('ec2')
        
    def name(self, NAME):
        '''
        Find instance name
        NAME = pattern to match, use wildcards to pattern match
        '''
        instance_info = ec2_get_info(self.session).instance_info_by_name(NAME)
        if not instance_info[0]:
            return False, instance_info[1]
        response = []
        for ITEM in instance_info[1]:
            for INSTANCE in ITEM['Instances']:
                for TAG in INSTANCE['Tags']:
                    if TAG['Key'] == 'Name':
                        response.append(TAG['Value'])
        return True, response

    def id(self, NAME):
        '''
        Return instance ID by name tag
        NAME = instance name tag value
        can use wildcards
        '''
        instance_info = ec2_get_info(self.session).instance_info_by_name(NAME)
        if not instance_info[0] or not instance_info[1]:
            return False, instance_info[1]
        response = []
        for ITEM in instance_info[1]:
            for INSTANCE in ITEM['Instances']:
                response.append(INSTANCE['InstanceId'])
        return True, response

    def ip(self, ID):
        '''
        Return IP addresses of instance by ID
        ID = Instance ID
        '''
        instance_info = ec2_get_info(self.session).instance_info_by_id(ID)
        if not instance_info[0]:
            return False, instance_info[1]
        response = []
        for ITEM in instance_info[1]:
            for INSTANCE in ITEM['Instances']:
                if 'PrivateIpAddress' in INSTANCE:
                    ip = [INSTANCE['PrivateIpAddress']]
                else:
                    ip = ['NONE']
                if 'PublicIpAddress' in INSTANCE:
                    ip.append(INSTANCE['PublicIpAddress'])
                else:
                    ip.append('NONE')
                response.append(ip)
        return True, response

    def id_from_ip(self, IP):
        '''
        Return instance ID and Tag:Name from private or public IP address
        IP = private/public IP address
        '''
        instance_info = ec2_get_info(self.session).instance_info_by_ip(IP)
        if not instance_info[0]:
            return False, instance_info[1]
        response = []
        for ITEM in instance_info[1]:
            for INSTANCE in ITEM['Instances']:
                response.append(INSTANCE['InstanceId'])
                for TAG in INSTANCE['Tags']:
                    if TAG['Key'] == 'Name':                                                                response.append(TAG['Value'])
        return True, response

    def key_pair(self, ID):
        '''
        Return key pair name by instance ID
        ID = Instance ID
        '''
        instance_info = ec2_get_info(self.session).instance_info_by_id(ID)
        if not instance_info[0]:
            return False, instance_info[1]
        if 'KeyName' in instance_info[1][0]['Instances'][0]:
            return True, instance_info[1][0]['Instances'][0]['KeyName']
        else:
             return True, ''

    def security_groups(self, ID):
        '''
        Return list of security groups by instance ID
        ID = Instance ID
        '''
        instance_info = ec2_get_info(self.session).instance_info_by_id(ID)
        if not instance_info[0]:
            return instance_info[1]
        return True, instance_info[1][0]['Instances'][0]['SecurityGroups']

    def state(self, ID):
        '''
        Return state by instance ID
        ID = Instance ID
        '''
        instance_info = ec2_get_info(self.session).instance_info_by_id(ID)
        if not instance_info[0]:
            return False, instance_info[1]
        return True, instance_info[1][0]['Instances'][0]['State']['Name']

    def start(self, ID):
        '''
        Start instance if it's in stopped state
        ID = Instance ID
        '''
        instance_state = ec2(self.session).state(ID)
        if instance_state[0] and instance_state[1] == 'stopped':
            try:
                response = self.ec2_client.start_instances(InstanceIds=[ID])
            except:
                return False, str(sys.exc_info()[1])
        elif instance_state[0] and instance_state[1] != 'stopped':
            return False, 'Instance state is ' + instance_state[1] + ' instance must be stopped!'
        return True, response

    def stop(self, ID):
        '''
        Stop instance if it's in running state
        ID = Instance ID
        '''
        instance_state = ec2(self.session).state(ID)
        if instance_state[0] and instance_state[1] == 'running':
            try:
                response = self.ec2_client.stop_instances(InstanceIds=[ID])
            except:
                return False, str(sys.exc_info()[1])
        elif instance_state[0] and instance_state[1] != 'running':
            return False, 'Instance state is ' + instance_state[1] + ' instance must be running!'
        return True, response
