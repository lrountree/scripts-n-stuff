# Modules to perform tag work on specified resource
# Each resource has it's own function
# Supported Resources: EC2, AutoScalling Groups, RDS, ELBv2
# Maintained By: Lucas Rountree (lredvtree@gmail.com)

# Import General Modules
import sys

# Import Custom Modules
import boto3, botocore.exceptions
sys.path.append('../../modules/aws')
from auth_modules import set_session

# Set up class to create tags
class create_tag:

    def __init__(self, PROFILE, REGION, KEY, VALUE):
        self.Tag_Key = KEY
        self.Tag_Value = VALUE
        try:
            self.session = boto3.Session(profile_name=PROFILE, region_name=REGION)
        except:
            print(sys.exc_info()[1])
            sys.exit(1)

    # Add tag to EC2 resource
    def ec2(self, ID):
        ec2_client = session.client('ec2')
        try:
            ec2_client.create_tags(Resources=[ID], Tags=[{'Key': Tag_Key, 'Value': Tag_Value}])
        except:
            return False, str(sys.exc_info())
        return True

    # Add tag to AutoScaling Group
    def asg(self, ID):
        asg_client = self.session.client('autoscaling')
        try:
            asg_client.create_or_update_tags(Tags=[{'ResourceId': ID, 'Key': Tag_Key, 'Value': Tag_Value}])
        except:
            return False, str(sys.exc_info())
        return True

    # Add tag to RDS resource
    def rds(self, ID):
        '''
        ID = RDS ARN
        '''
        rds_client = self.session.client('rds')
        try:
            rds_client.add_tags_to_resource(ResourceName=ID, Tags=[{'Key': Tag_Key, 'Value': Tag_Value}])
        except:
            return False, str(sys.exc_info())
        return True

    # Add tag to ELBv2 resource
    def elb(self, ID):
        '''
        ID = load balancer ARN
        '''
        elb_client = self.session.client('elbv2')
        try:
            elb_client.add_tags(ResourceArns=ID, Tags=[{'Key': Tag_Key, 'Value': Tag_Value}])
        except:
            return False, str(sys.exc_info())
        return True

    # Add tag to DocumentDB resource
    def ddb(self, ID):
        ddb_client = self.session.client('docdb')
        try:
            ddb_client.add_tags_to_resource(ResourceName=ID, Tags=[{'Key': Tag_Key, 'Value': Tag_Value}])
        except:
            return False, str(sys.exc_info())
        return True

    # Add tag to DynamoDB resource
    def dynamo(self, ID):
        '''
        ID = dynamodb ARN
        '''
        dynamo_client = self.session.client('dynamodb')
        try:
            dynamo_client.tag_resource(ResourceArn=ID, Tags=[{'Key': Tag_Key, 'Value': Tag_Value}])
        except:
            return False, str(sys.exc_info())
        return True

    # Add tag to EMR resource
    def emr(self, ID):
        '''
        ID = emr cluster ID
        '''
        emr_client = self.session.client('emr')
        try:
            emr_client.add_tags(ResourceId=ID, Tags=[{'Key': Tag_Key, 'Value': Tag_Value}])
        except:
            return False, str(sys.exc_info())
        return True

    # Add tag to Key Management Service resource
    def kms(self, ID):
        '''
        ID = key ID
        '''
        kms_client = self.session.client('kms')
        try:
            kms_client.tag_resource(KeyId=ID, Tags=[{'TagKey': Tag_Key, 'TagValue': Tag_Value}])
        except:
            return False, str(sys.exc_info())
        return True

    # Add tag to ElasticSearch resource
    def es(self, ID):
        '''
        ID = elastic search ARN
        '''
        es_client = self.session.client('es')
        try:
            es_client.add_tags(ARN=ID, TagList=[{'Key': Tag_Key, 'Value': Tag_Value}])
        except:
            return False, str(sys.exc_info())
        return True

    # Add tag to Elastic Container Service resource
    def ecs(self, ID):
        '''
        ID = cluster ARN
        '''
        ecs_client = self.session.client('ecs')
        try:
            ecs_client.tag_resource(resourceArn=ID, tags=[{'key': Tag_Key, 'value': Tag_Value}])
        except:
            return False, str(sys.exc_info())
        return True

    # Add tag to Elastic Kubernetes Service resource
    def eks(self, ID):
        '''
        ID = ARN
        '''
        eks_client = self.session.client('eks')
        try:
            eks_client.tag_resource(resourceArn=ITEM['arn'], tags={Tag_Key: Tag_Value})
        except:
            return False, str(sys.exc_info())
        return True

    # Add tag to Elastic Container Registry resource
    def ecr(self, ID):
        '''
        ID = repository ARN
        '''
        ecr_client = self.session.client('ecr')
        try:
            ecr_client.tag_resource(resourceArn=ID, tags=[{'Key': Tag_Key, 'Value': Tag_Value}])
        except:
            return False, str(sys.exc_info())
        return True

    # Add tag to Lambda resource
    def lam(self, ID):
        '''
        ID = lambda function ARN
        '''
        lam_client = self.session.client('lambda')
        try:
            lam_client.tag_resource(Resource=ID, Tags={Tag_Key: Tag_Value})
        except:
            return False, str(sys.exc_info())
        return True

    # Add tag to API Gateway resource
    def agw(self, ID):
        '''
        ID = gateway ARN
        '''
        agw_client = self.session.client('apigateway')
        try:
            agw_client.tag_resource(resourceArn=ID, tags={Tag_Key: Tag_Value})
        except:
            return False, str(sys.exc_info())
        return True

    # Add tag to API Gateway v2 resource
    def agw2(self, ID):
        '''
        ID = gateway ARN
        '''
        agw2_client = self.session.client('apigatewayv2')
        try:
            agw2_client.tag_resource(resourceArn=ID, tags={Tag_key: Tag_Value})
        except:
            return False, str(sys.exc_info())
        return True

    # Add tag to Simple Queue Service resource
    def sqs(self, ID):
        '''
        ID = Queue URL
        '''
        sqs_client = self.session.client('sqs')
        try:
            sqs_client.tag_queue(QueueUrl=ID, Tags={Tag_Key: Tag_Value})
        except:
            return False, str(sys.exc_info())
        return True

    # Add tag to Simple Notification Service resource
    def sns(self, ID):
        '''
        ID = Topic ARN
        '''
        sns_client = self.session.client('sns')
        try:
            sns_client.tag_resource(ResourceArn=ID, Tags=[{'Key': Tag_Key, 'Value': Tag_Value}])
        except:
            return False, str(sys.exc_info())
        return True

# function to return requested tag/s
def get_tags(TAG, Tag_List):
    if TAG == 'ALL':
        return True, Tag_List
    for ITEM in Tag_List:
        if 'Key' in ITEM:
            X = 'Key'
        else:
            X = 'key'
        if ITEM[X] == TAG:
            Tag_Value = ITEM['Value']
    if 'Tag_Value' not in locals():
        return False, f'No Tag with key {TAG} found.'
    return True, Tag_Value

# Set up class to get tags from resource
class find_tags:
    '''
    This class contains functions to return tags for AWS resources.
    Use: tag_modules.find_tags(session)
    '''

    def __init__(self, session, KEY = '', VALUE = ''):
        self.Tag_Key = KEY
        self.Tag_Value = VALUE
        self.session = session

    # get EC2 tags
    def ec2(self, ID, TAG = 'ALL'):
        '''
        ID = instance ID
        TAG = Tag key to get value for, use ALL to list all tag keys with values
        '''
        ec2_client = self.session.client('ec2')
        try:
            Tag_List = ec2_client.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [ID]}])['Tags']
        except:
            return False, str(sys.exc_info())
        return get_tags(TAG, Tag_List)

    # get AutoScale Group tags
    def asg(self, ID, TAG = 'ALL'):
        '''
        ID = autoscale group ID
        TAG = Tag key to get value for, use ALL to list all tag keys with values
        '''
        asg_client = self.session.client('autoscaling')
        try:
            Tag_List = asg_client.describe_tags(Filters=[{'Name': 'auto-scaling-group', 'Values': [ID]}])['Tags']
        except:
            return False, str(sys.exc_info())
        return get_tags(TAG, Tag_List)

    # get RDS tags
    def rds(self, ID, TAG = 'ALL'):
        '''
        ID = RDS ARN
        TAG = Tag key to get value for, use ALL to list all tag keys with values
        '''
        rds_client = self.session.client('rds')
        try:
            Tag_List = rds_client.list_tags_for_resource(ResourceName=ID)['TagList']
        except:
            return False, str(sys.exc_info())
        return get_tags(TAG, Tag_List)

    # get Elastic Load Balancer tags
    def elb(self, ID, TAG = 'ALL'):
        '''
        ID = elastic load balancer ARN
        TAG = Tag key to get value for, use ALL to list all tag keys with value
        '''
        elb_client = self.session.client('elbv2')
        try:
            Tag_List = elb_client.describe_tags(ResourceArns=[ID])['TagDescriptions'][0]['Tags']
        except:
            return False, str(sys.exc_info())
        return get_tags(TAG, Tag_List)

    # get DocumentDB tags
    def ddb(self, ID, TAG = 'ALL'):
        '''
        ID = documentdb ARN
        TAG = Tag key to get value for, use ALL to list all tag keys with value
        '''
        ddb_client = self.session.client('docdb')
        try:
            Tag_List = ddb_client.list_tags_for_resource(ResourceName=ID)['TagList']
        except:
            return False, str(sys.exc_info())
        return get_tags(TAG, Tag_List)

    # get DynamoDB tags
    def dynamo(self, ID, TAG = 'ALL'):
        '''
        ID = dynamodb ARN
        TAG = Tag key to get value for, use ALL to list all tag keys with value
        '''
        dynamo_client = self.session.client('dynamodb')
        try:
            Tag_List = dynamo_client.list_tags_of_resource(ResourceArn=ID)['Tags']
        except:
            return False, str(sys.exc_info())
        return get_tags(TAG, Tag_List)

    # get Elastic Map Reduce tags
    def emr(self, ID, TAG = 'ALL'):
        '''
        ID = emr cluster ID
        TAG = Tag key to get value for, use ALL to list all tag keys with value
        '''
        emr_client = self.session.client('emr')
        try:
            Tag_List = emr_client.describe_cluster(ClusterId=ID)['Cluster']['Tags']
        except:
            return False, str(sys.exc_info())
        return get_tags(TAG, Tag_List)

    # get Key Management Service tags
    def kms(self, ID, TAG = 'ALL'):
        '''
        ID = Key ID
        TAG = Tag key to get value for, use ALL to list all tag keys with value
        '''
        kms_client = self.session.client('kms')
        try:
            Tag_List = kms_client.list_resource_tags(KeyId=ID)['Tags']
        except:
            return False, str(sys.exc_info())
        return get_tags(TAG, Tag_List)

    # get Elastic Search Service tags
    def es(self, ID, TAG = 'ALL'):
        '''
        ID = elasticsearch domain name ARN
        TAG = Tag key to get value for, use ALL to list all tag keys with value
        '''
        es_client = self.session.client('es')
        try:
            Tag_list = es_client.list_tags(ARN=ID)['TagList']
        except:
            return False, str(sys.exc_info())
        return get_tags(TAG, Tag_List)

    # get Elastic Container Service tags
    def ecs(self, ID, TAG = 'ALL'):
        '''
        ID = elastic container cluster ARN
        TAG = Tag key to get value for, use ALL to list all tag keys with value
        '''
        ecs_client = self.session.client('ecs')
        try:
            Tag_List = ecs_client.list_tags_for_resource(resourceArn=ID)['tags']
        except:
            return False, str(sys.exc_info())
        return get_tags(TAG, Tag_List)

    # get Elastic Kubernetes Service tags
    def eks(self, ID, TAG = 'ALL'):
        '''
        ID = elastic kubernetes cluster ARN
        TAG = Tag key to get value for, use ALL to list all tag keys with value
        '''
        eks_client = self.session.client('eks')
        try:
            Tag_List = eks_client.list_tags_for_resource(resourceArn=ID)['tags']
        except:
            return False, str(sys.exc_info())
        return get_tags(TAG, Tag_List)

    # get Elastic Container Repository tags
    def ecr(self, ID, TAG = 'ALL'):
        '''
        ID = elastic container repository ARN
        TAG = Tag key to get value for, use ALL to list all tag keys with value
        '''
        ecr_client = self.session.client('ecr')
        try:
            Tag_List = ecr_client.list_tags_for_resource(resourceArn=ID)['tags']
        except:
            return False, str(sys.exc_info())
        return get_tags(TAG, Tag_List)

    # get Lambda function tags
    def lam(self, ID, TAG = 'ALL'):
        '''
        ID = lambda function ARN
        TAG = Tag key to get value for, use ALL to list all tag keys with value
        '''
        lam_client = self.session.client('lambda')
        try:
            Tag_List = lam_client.list_tags(Resource=ID)['Tags']
        except:
            return False, str(sys.exc_info())
        return get_tags(TAG, Tag_List)

    # get apigateway tags
    def agw(self, ID, TAG = 'ALL'):
        '''
        ID = Rest API ID
        TAG = Tag key to get value for, use ALL to list all tag keys with value
        '''
        agw_client = self.session.client('apigateway')
        try:
            Tag_List = agw_client.get_rest_api(restApiId=ID)['tags']
        except:
            return False, str(sys.exc_info())
        return get_tags(TAG, Tag_List)

    # get apigatewayv2 tags
    def agw2(self, ID, TAG = 'ALL'):
        '''
        ID = API ID
        TAG = Tag key to get value for, use ALL to list all tag keys with value
        '''
        agw2_client = self.session.client('apigatewayv2')
        try:
            Tag_List = agw2_client.get_api(ApiId=ID)['Tags']
        except:
            return False, str(sys.exc_info())
        return get_tags(TAG, Tag_List)

    # get Simple Queue Service tags
    def sqs(self, ID, TAG = 'ALL'):
        '''
        ID = sqs queue URL
        TAG = Tag key to get value for, use ALL to list all tag keys with value
        '''
        sqs_client = self.session.client('sqs')
        try:
            Tag_List = sqs_client.list_queue_tags(QueueUrl=ID)['Tags']
        except:
            return False, str(sys.exc_info())
        return get_tags(TAG, Tag_List)

    # get Simple Notification Service tags
    def sns(self, ID, TAG = 'ALL'):
        '''
        ID =
        TAG = Tag key to get value for, use ALL to list all tag keys with value
        '''
        sns_client = self.session.client('sns')
        try:
            Tag_List = sns.list_tags_for_resource(ResourceArn=ID)['Tags']
        except:
            return False, str(sys.exc_info())
        return get_tags(TAG, Tag_List)

