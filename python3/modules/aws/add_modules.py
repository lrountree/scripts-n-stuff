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

    def lb_listener_arns(self, ARN):
        '''
        Return a list of listeners on the load balancer
        ARN = Load balancer ARN
        '''
        try:
            lb_listeners = self.elbv2_client.describe_listeners(LoadBalancerArn=ARN)['Listeners']
        except:
            return False, str(sys.exc_info()[1])
        arn_list = []
        for ITEM in lb_listeners:
            arn_list.append(ITEM['ListenerArn'])
        if not arn_list:
            return False, 'Listener Not Found!'
        return True, arn_list

    def lb_listener_rules(self, ARN):
        '''
        Return rule info for a load balancer listener
        ARN = Listener ARN
        '''
        try:
            listener_rules = self.elbv2_client.describe_rules(ListenerArn=ARN)['Rules']
        except:
            return False, str(sys.exc_info()[1])
        rule_list = []
        for ITEM in listener_rules:
            tag_list = self.elbv2_client.describe_tags(ResourceArns=[ITEM['RuleArn']])['TagDescriptions'][0]['Tags']
            rule_name = ''
            for TAG in tag_list:
                if TAG['Key'] == 'Name':
                    rule_name = TAG['Value']
            if not rule_name:
                rule_name = 'UNKNOWN'
            rule_list.append({'Name': rule_name, 'Arn': ITEM['RuleArn'], 'TargetGroupArns': [I['TargetGroupArn'] for I in ITEM['Actions']]})
        if not rule_list:
            return False, 'No Rules Found!'
        return True, rule_list

    def lb_target_groups(self, ARN):
        '''
        Return info about load balancer target groups
        ARN = Load balancer ARN
        '''
        try:
            target_groups = self.elbv2_client.describe_target_groups(LoadBalancerArn=ARN)['TargetGroups']
        except:
            return False, str(sys.exc_info()[1])
        tg_list = []
        for ITEM in target_groups:
            tg_list.append({'ARN': ITEM['TargetGroupArn'], 'Name': ITEM['TargetGroupName'], 'HealthCheck': ITEM['HealthCheckEnabled']})
        if not tg_list:
            return False, 'No Target Groups Found!'
        return True, tg_list

    def lb_target_info(self, ARN):
        '''
        Return load balancer target info
        ARN = Target Group ARN
        '''
        try:
            target_health = self.elbv2_client.describe_target_health(TargetGroupArn=ARN)['TargetHealthDescriptions']
        except:
            return False, str(sys.exc_info()[1])
        th_list = []
        for ITEM in target_health:
            th_list.append({'ID': ITEM['Target']['Id'], 'State': ITEM['TargetHealth']['State']})
        if not th_list:
            return False, 'No Target Found!'
        return True, th_list

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

    def lb_arn_from_name(self, NAME):
        '''
        Return Load Balancer ARN by name
        NAME = Load Balancer Name
        can use wildcards
        '''
        lb_info = get_info(self.session).lb_info_from_name(NAME)
        if not lb_info[0] or not lb_info[1]:
            return False, lb_info[1]
        lb_arn = lb_info[1]['LoadBalancerArn']
        return True, lb_arn

    def lb_target_health(self, NAME):
        '''
        Return load balancer target health by lb name
        NAME = Load Balancer Name
        '''
        lb_arn = self.lb_arn_from_name(NAME)
        if lb_arn[0]:
            lb_arn = lb_arn[1]
        else:
            return False, lb_arn[1]
        target_list = self.lb_target_groups(lb_arn)
        if target_list[0]:
            target_list = target_list[1]
        else:
            return False, target_list[1]
        response_list = []
        for TARGET in target_list:
            target_health = self.lb_target_info(TARGET['ARN'])
            if not target_health[0]:
                return False, target_health[1]
            response_list.append({'NAME': TARGET['Name'], 'TARGETS': target_health[1]})
        return response_list
