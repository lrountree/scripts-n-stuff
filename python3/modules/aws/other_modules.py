# General AWS tool modules
# Maintained by: Lucas Rountree (lredvtree@gmail.com)

## Import Modules
# General
import sys
# AWS
import boto3, botocore

class elbv2_get_info:
    '''
    elbv2 core modules
    set session first, call elbv2 with session:
    session = general_modules.set_session(PROFILE, REGION)
    '''

    def __init__(self, session):
        self.elbv2_client = session.client('elbv2')

    def list_all_elbs(self):
        '''
        Return a name:arn dictionary list of all elbs in given region 
        '''
        try:
            grab_elbs = self.elbv2_client.describe_load_balancers()['LoadBalancers']
        except:
            return False, str(sys.exc_info()[1])
        response = []
        for ITEM in grab_elbs:
            response.append({ITEM['LoadBalancerName']: ITEM['LoadBalancerArn']})
        return True, response

class redshift_get_info:
    '''
    redshift core modules
    set session first, call redshift with session
    session = general_modules.set_session(PROFILE, REGION)
    '''

    def __init__(self, session):
        self.redshift_client = session.client('redshift')

    def list_all_clusters(self):
        '''
        Return a list of all clusters by identifier
        '''
        try:
            grab_clusters = self.redshift_client.describe_clusters()['Clusters']
        except:
            return False, str(sys.exc_info()[1])
        response = []
        for ITEM in grab_clusters:
            response.append(ITEM['ClusterIdentifier'])
        return True, response

class ecs_get_info:
    '''
    ecs core modules
    set session first, call ecs with session
    session = general_modules.set_session(PROFILE, REGION)
    '''

    def __init__(self, session):
        self.ecs_client = session.client('ecs')

    def list_all_clusters(self):
        '''
        Return a list of ecs cluster arns
        '''
        try:
            response = self.ecs_client.list_clusters()['clusterArns']
        except:
            return False, str(sys.exc_info()[1])
        return True, response

class eks_get_info:
    '''
    eks core modules
    set session first, call eks with session
    session = general_modules.set_session(PROFILE, REGION)
    '''

    def __init__(self, session):
        self.eks_client = session.client('eks')

    def list_all_clusters(self):
        '''
        Return a list of all eks clusters
        '''
        try:
            response = self.eks_client.list_clusters()['clusters']
        except:
            return False, str(sys.exc_info()[1])
        return True, response

class asm:
    '''
    AWS Secrets Manager Modules
    Set session first, call secrets with session:
    session = general_modules.set_session(PROFILE, REGION)
    secrets = general_modules.secrets(session)
    '''

    def __init__(self, session):
        self.secrets_client = session.client('secretsmanager')

    def list_secrets(self):
        '''
        Return a list of all secrets
        '''
        try:
            get_secrets = self.secrets_client.list_secrets()
        except:
            return False, str(sys.exc_info()[1])
        full_secrets = [get_secrets]
        while 'NextToken' in get_secrets:
            try:
                get_secrets = self.secrets_client.list_secrets(NextToken=get_secrets['NextToken'])
            except:
                return False, str(sys.exc_info()[1])
            full_secrets.append(get_secrets)
        response = []
        for LIST in full_secrets:
            for ITEM in LIST['SecretList']:
                response.append(ITEM['Name'])
        return True, response

    def get_secret(self, SECRET):
        '''
        Get secret
        '''
        try:
            secret_output = self.secrets_client.describe_secret(SecretId=SECRET)
        except:
            return False, str(sys.exc_info()[1])
        return True, secret_output
    
    def secret_keys(self, SECRET):
        '''
        Get secret keys
        '''
        try:
            get_keys = json.loads(self.secrets_client.get_secret_value(SecretId=SECRET)['SecretString'])
        except:
            return False, str(sys.exc_info()[1])
        response = [KEY for KEY in get_keys]
        return True, response

    def secret_value(self, SECRET, KEY):
        '''
        Get secret key value
        '''
        try:
            get_value = json.loads(self.secrets_client.get_secret_value(SecretId=SECRET)['SecretString'])
        except:
            return False, str(sys.exc_info()[1])
        return True, get_value[KEY]
