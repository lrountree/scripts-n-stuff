# Python modules to authenticate against AWS and cache credentials for use with CLI/SDK
# Maintained by: Lucas Rountree (lredvtree@gmail.com)

## Import Modules:
# General
import sys
# AWS
import boto3, botocore

# Set AWS session for SDK using profile and region
def set_session(PROFILE='default', REGION='us-west-2'):
    '''
    Provide AWS SDK session block
    set_session(PROFILE, REGION)
    PROFILE = AWS CLI profile to use (from credentials file), default is "default"
    REGION = AWS region to use, default is "us-west-2"
    '''
    try:
        session = boto3.Session(profile_name=PROFILE, region_name=REGION)
    except botocore.exceptions.ProfileNotFound as ERROR:
        print(ERROR)
        sys.exit(1)
    except TypeError as ERROR:
        print(ERROR)
        sys.exit(1)
    except:
        print(sys.exc_info()[1])
        sys.exit(1)
    return session
