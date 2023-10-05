# General RDS tool modules
# Maintained by: Lucas Rountree (lredvtree@gmail.com)

## Import Modules
# General
import sys
# AWS
import boto3, botocore

class rds_get_info:
    '''
    rds core modules
    set session first, call rds with session
    session = general_modules.set_session(PROFILE, REGION)
    rds = add_modules.get_info.rds(session)
    '''

    def __init__(self, session):
        self.rds_client = session.client('rds')
        
    def list_all_instances(self):
        '''
        Return a list of all rds instances by identifier
        '''
        try:
            grab_instances = self.rds_client.describe_db_instances()['DBInstances']
        except:
            return False, str(sys.exc_info()[1])
        response = []
        for ITEM in grab_instances:
            response.append(ITEM['DBInstanceIdentifier'])
        return True, response

    def db_info_from_name(self, NAME):
        '''
        Return rds instance info by name
        NAME = rds instance name
        ''' 
        try:
            rds_info = self.rds_client.describe_db_instances(DBInstanceIdentifier=NAME)['DBInstances'][0]
        except:
            return False, str(sys.exc_info()[1])
        if not rds_info:
            return False, 'Load Balancer Not Found'
        return True, rds_info

    def db_tag_value(self, ARN, TAG):
        '''
        Return rds instance tag value by name
        ARN = RDS instance ARN
        TAG = RDS instance tag name
        '''
        try:
            db_tags = self.rds_client.list_tags_for_resource(ResourceName=ARN)['TagList']
        except:
            return False, str(sys.exc_info()[1])
        db_tag = ''
        for ITEM in db_tags:
            if ITEM['Key'] == TAG:
                    db_tag = ITEM['Value']
        if not db_tag:
            return False, 'Tag Not Found!'
        return True, db_tag

class rds(rds_get_info):
    
    def __init__(self, session):
        rds_get_info.__init__(self, session)
        self.session = session
        self.rds_client = session.client('rds')

    def db_arn_from_name(self, NAME):
        '''
        Return RDS instance ARN by name
        NAME = RDS instance name
        '''
        db_arn = get_info(self.session).db_info_from_name(NAME)
        if not db_arn[0]:
            return False, db_info[1]
        return True, db_arn[1]['DBInstanceArn']

    def db_storage(self, NAME):
        '''
        Return RDS instance allocated storage
        NAME = RDS instance name
        '''
        allocated_storage = get_info(self.session).db_info_from_name(NAME)
        if not allocated_storage[0]:
            return False, allocated_storage[1]
        return True, allocated_storage[1]['AllocatedStorage']

    def db_type(self, NAME):
        '''
        Return RDS instance type
        NAME = RDS instance name
        '''
        instance_type = get_info(self.session).db_info_from_name(NAME)
        if not instance_type[0]:
            return False, instance_type[1]
        return True, instance_type[1]['DBInstanceClass']

    def db_engine(self, NAME):
        '''
        Return RDS instance engine
        NAME = RDS instance name
        '''
        instance_engine = get_info(self.session).db_info_from_name(NAME)
        if not instance_engine[0]:
            return False, instance_engine[1]
        return True, instance_engine[1]['Engine']

    def db_endpoint(self, NAME):
        '''
        Return RDS instance endpoint
        NAME = RDS instance name
        '''
        instance_endpoint = get_info(self.session).db_info_from_name(NAME)
        if not instance_endpoint[0]:
            return False, instance_endpoint[1]
        return True, instance_endpoint[1]['Endpoint']['Address']

    def db_memory(self, NAME):
        '''
        Return RDS instance total memory
        NAME = RDS instance name
        '''
        self.ec2_client = self.session.client('ec2')
        instance_type = self.db_type(NAME)
        if not instance_type[0]:
            return False, instance_type[1]
        instance_type = instance_type[1].replace('db.', '')
        try:
            total_memory = float(self.ec2_client.describe_instance_types(InstanceTypes=[instance_type])['InstanceTypes'][0]['MemoryInfo']['SizeInMiB'])
        except:
            return False, str(sys.exc_info()[1])
        return True, total_memory
        
    def iam_token(self, HOST, USER, PORT):
        '''
        Generate IAM authentication token
        HOST = RDS cluster or instance endpoint
        PORT = RDS connection port, normally 5432
        USER = Database user or role name
        '''
        try:
            response = self.rds_client.generate_db_auth_token(HOST, PORT, USER)
        except:
            return False, str(sys.exc_info()[1])
        return True, response
