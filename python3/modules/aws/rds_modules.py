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

class rds(rds_get_info):
    
    def __init__(self, session):
        rds_get_info.__init__(self, session)
        self.session = session
        self.rds_client = session.client('rds')
        
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
