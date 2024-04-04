#! /bin/python3

# Run AWS Service Checks
# Maintained By: Lucas Rountree

# Import General Modules
import sys, argparse, json

# Import Custom Modules
sys.path.append('/git/aws/python/modules')
from auth_modules import no_session as session
from add_modules import elbv2
from ec2_modules import ec2_get_info as ec2

# Add Arguments
parser = argparse.ArgumentParser(description='Run AWS Service Checks', prog='aws')
parser.add_argument(
        '-r',
        action='store',
        type=str,
        default='us-west-2',
        help='AWS Region'
    )
parser.add_argument(
        '-c',
        action='store',
        type=str,
        required=True,
        help='Service Check'
    )
parser.add_argument(
        '-n',
        action='store',
        type=str,
        required=True,
        help='Load Balancer Name'
    )
args = parser.parse_args()

# Set up functions
ses = session(args.r)
elbv2 = elbv2(ses)
ec2 = ec2(ses)

# Process service checks
if len(args.c.split('.')) != 2:
    print('Please provide service check as: <service>.<check>')
    sys.exit(1)
sname = args.c.split('.')[0]
cname = args.c.split('.')[1]

if sname == 'elbv2':
    if cname == 'target_health':
        target_health = elbv2.lb_target_health(args.n)
        if not target_health[0]:
            print(target_health[1])
            sys.exit[1]
        target_list = []
        for TARGET in target_health:
            for GROUP in TARGET['TARGETS']:
                NAME = ec2.instance_info_by_id(GROUP['ID'])
                TAGS = NAME[1][0]['Instances'][0]['Tags']
                for T in TAGS:
                    if T['Key'] == 'Name':
                        instance_name = T['Value']
                target_list.append({'target_group': TARGET['NAME'], 'instance_name': instance_name, 'instance_id': GROUP['ID'], 'state': GROUP['State']})
        print(json.dumps(target_list))
