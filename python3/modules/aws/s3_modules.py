# General S3 tool modules
# Maintained by: Lucas Rountree (lredvtree@gmail.com)

## Import Modules
# General
import sys
# AWS
import boto3, botocore

class s3_get_info:
    '''
    s3 modules to pull info from resources
    set session first, call iam with session:
    session = general_modules.set_session(PROFILE, REGION)
    s3 = general_modules.s3(session)
    '''

    def __init__(self, session):
        self.s3_client = session.client('s3')

    def find_buckets(self, NAME = 'ALL'):
        '''
        Return a list of buckets that match pattern NAME
        NAME = bucket name pattern to match, ALL to list all roles
        '''
        try:
            Bucket_List = [X['Name'] for X in self.s3_client.list_buckets()['Buckets']]
        except:
            return False, str(sys.exc_info()[1])
        if NAME == 'ALL':
            return True, Bucket_List
        else:
            response = []
            for X in Bucket_List:
                if NAME in X:
                    response.append(X)
        if not response:
            return False, response
        return True, response

    def prefix_list(self, BUCKET, PREFIX = False):
        '''
        Return a list of prefixes for a given bucket
        BUCKET = S3 bucket name
        PREFIX = Prefix to look in
        '''
        if PREFIX:
            try:
                Object_List = self.s3_client.list_objects(Bucket=BUCKET, Prefix=PREFIX)['Contents']
            except:
                return False, str(sys.exc_info()[1])
        else:
            try:
                Object_List = self.s3_client.list_objects(Bucket=BUCKET)['Contents']
            except:
                return False, str(sys.exc_info()[1])
        Prefix_List = []
        for X in Object_List:
            Object_Line = X['Key']
            Object_Line = Object_Line.split(PREFIX + '/')[1]
            prefix = Object_Line.split('/')[0]
            if X['Key'].split(prefix)[1]:
                if prefix not in Prefix_List:
                    Prefix_List.append(prefix)
        return True, Prefix_List

class s3(s3_get_info):

    def __init__(self, session):
        s3_get_info.__init__(self, session)
        self.session = session
        self.s3_client = self.session.client('s3')

    def change_lf(self, NAME):
#        try:
#            lf_config = open(FILE, 'r')
#        except:
#            return False, str(sys.exc_info()[1])
        try:
 #           response = self.s3_client.put_bucket_lifecycle_configuration(Bucket=NAME, LifecycleConfiguration=lf_config.read().rstrip('\n'))
            response = self.s3_client.put_bucket_lifecycle_configuration(Bucket=NAME, LifecycleConfiguration={'Rules': [{'ID': 'theta_14d_lifecycle_policy','Prefix': '','Status': 'Enabled','Expiration': {'Days': 14},}]})
        except:
            return False, str(sys.exc_info()[1])
#        lf_config.close()
        return True, response
