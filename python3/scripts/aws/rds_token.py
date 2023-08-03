# Output RDS Token
# Maintained By: Lucas Rountree (lredvtree@gmail.com)

# Import General Modules
import sys

# Import Custom Modules
sys.path.append('../../modules/aws')
from auth_modules import set_session as session
from rds_modules import rds

def get_token(PROFILE, REGION, ENDPOINT, USER, PORT):
    ses = session(PROFILE, REGION)
    rds_client = rds(ses)

    iam_token = rds_client.iam_token(ENDPOINT, USER, PORT)

    return iam_token[1]

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate token for RDS IAM authentication (SSO)', prog='rds_token')
    parser.add_argument('-p', action='store', type=str, help='AWS profile to use, from credentials/config file.')
    parser.add_argument('-r', action='store', type=str, help='Region specification')
    parser.add_argument('-e', action='store', type=str, help='RDS endpoint')
    parser.add_argument('-u', action='store', type=str, help='IAM auth role name')
    parser.add_argument('-c', action='store', type=str, default='5432', help='RDS connection port. Default is 5432')
   
    args = parser.parse_args()

    if args.p is False:
        parser.error('You must specify config file profile name with -p')
    if args.r is False:
        parser.error('You must specify AWS region with -r')
    if args.e is False:
        parser.error('You must specify RDS endpoint with -e')
    if args.u is False:
        parser.error('You must specify role/username with -u')
    
    else:
        print(get_token(args.p, args.r, args.e, args.u, args.c))
