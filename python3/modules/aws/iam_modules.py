# General IAM tool modules
# Maintained by: Lucas Rountree (lredvtree@gmail.com)

## Import Modules
# General
import sys
# AWS
import boto3, botocore

class iam_get_info:
    '''
    iam modules
    set session first, call iam with session:
    session = general_modules.set_session(PROFILE, REGION)
    iam = general_modules.iam(session)
    '''

    def __init__(self, session):
        self.iam_client = session.client('iam')

    def find_roles(self, NAME = 'ALL'):
        '''
        Return a list of IAM roles that match pattern NAME
        NAME = Role name pattern to match, ALL to list all roles
        '''
        try:
            list_roles = self.iam_client.list_roles()
        except:
            return False, str(sys.exc_info()[1])
        Role_List = []
        for ROLE in list_roles['Roles']:
            Role_List.append(ROLE['RoleName'])
        while 'Marker' in list_roles:
            list_roles = self.iam_client.list_roles(Marker=list_roles['Marker'])
            for ROLE in list_roles['Roles']:
                Role_List.append(ROLE['RoleName'])
        if NAME == 'ALL':
            return True, Role_List 
        Found_Roles = []
        for ROLE in Role_List:
            if NAME in ROLE:
                Found_Roles.append(ROLE)
        return True, Found_Roles

    def role_info_by_name(self, NAME):
        '''
        Return IAM resource info by Name
        NAME = Role name
        '''
        try:
            response = self.iam_client.get_role(RoleName=NAME)
        except:
            return False, str(sys.exc_info()[1])
        return True, response

class iam(iam_get_info):

    def __init__(self, session):
        iam_get_info.__init__(self, session)
        self.session = session

    def list_roles(self, NAME = 'ALL'):
       '''
       Return a list of role names, can pattern match
       NAME = Pattern to match, or ALL to list all roles (default)
       '''
       try:
           response = iam_get_info(self.session).find_roles(NAME)
       except:
           return False, str(sys.exc_info()[1])
       if not response[0]:
           return False, response[1]
       return True, response[1]

    def role_arn(self, NAME):
       try:
           response = iam_get_info(self.session).role_info_by_name(NAME)
       except:
           return False, str(sys.exc_info()[1])
       if not response[0]:
           return False, response[1]

       return True, response[1]['Role']['Arn']
