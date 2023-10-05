# Additional AWS Service modules
# Maintained by: Lucas Rountree (lredvtree@gmail.com)

## Import Modules
# General
import sys, json
# AWS
import boto3, botocore

class get_info:
    '''
    modules and clients
    set session first, call client with session:
    session = general_modules.set_session(PROFILE, REGION)
    <client> = add_modules.get_info.<client>(session)
    '''

    def __init__(self, session):
        self.elbv2_client = session.client('elbv2')

    def list_all_lbs(self):
        '''
        Return a list of dictonary items containing name:arn of all load balancers
        '''
        try:
            grab_data = self.elbv2_client.describe_load_balancers()['LoadBalancers']
        except:
            return False, str(sys.exc_info()[1])
        response = []
        for ITEM in grab_data:
            response.append({'Name': ITEM['LoadBalancerName'], 'ARN': ITEM['LoadBalancerArn']})
        if not response:
            return False, 'No load balancers found!'
        return True, response

    def lb_info_from_name(self, NAME):
        '''
        Return load balancer info by name
        NAME = Load balanver name
        '''
        try:
            lb_list = self.elbv2_client.describe_load_balancers()['LoadBalancers']
        except:
            return False, str(sys.exc_info()[1])
        get_info = False
        for ITEM in lb_list:
            if ITEM['LoadBalancerName'] == NAME:
                get_info = ITEM
        if not get_info:
            return False, 'Load Balancer Not Found'
        return True, get_info

    def lb_tag_value(self, ARN, TAG):
        '''
        Return load balancer tag value by name
        ARN = Load balancer ARN
        TAG = Load balancer tag name
        '''
        try:
            lb_tags = self.elbv2_client.describe_tags(ResourceArns=[ARN])
        except:
            return False, str(sys.exc_info()[1])
        lb_tag = ''
        for ITEM in lb_tags['TagDescriptions']:
            for T in ITEM['Tags']:
                if T['Key'] == TAG:
                    lb_tag = T['Value']
        if not lb_tag:
            return False, 'Tag Not Found!'
        return True, lb_tag

class elbv2(get_info):

    def __init__(self, session):
        get_info.__init__(self, session)
        self.session = session
        self.elbv2_client = session.client('elbv2')

    def lb_id_from_name(self, NAME):
        '''
        Return Load Balancer ID by name
        NAME = Load Balancer Name
        can use wildcards
        '''
        lb_info = get_info(self.session).lb_info_from_name(NAME)
        if not lb_info[0] or not lb_info[1]:
            return False, lb_info[1]
        lb_id = lb_info[1]['LoadBalancerArn'].split('/', 1)[1]
        return True, lb_id
