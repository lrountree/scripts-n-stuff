# Perform EC2 instance tasks
# Maintained by: Lucas Rountree (lredvtree@gmail.com)

# Import General Modules
import sys

# Import Custom Modules
sys.path.append('../../modules/aws')
import ec2_modules as ec2mod
import auth_modules as authmod

def get_state(IN):
    try:
        Instance_State = ec2.state(IN)
    except:
        print('Can not find state for instance ID: ', Instance_Id)
        print(sys.exc_info()[1])
        sys.exit(1)
    if not Instance_State[0]:
        print(Instance_State[1])
        sys.exit(1)
    return Instance_State

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Peform standard tasks against ec2 instances', prog='ec2')
    parser.add_argument('-p', action='store', type=str, default='default', help='AWS profile to use, from credentials file. Default is "default"')
    parser.add_argument('-r', action='store', type=str, default='us-west-2', help='AWS region, default is "us-west-2"')
    parser.add_argument('-i', action='store', type=str, required=True, help='Instance identifier, either value of Name tag or instance ID')
    parser.add_argument('-c', action='store', type=str, choices=['state', 'start', 'stop'], required=True, help='Command to issue to instance, options are: state, start, stop')

    args = parser.parse_args()

    if args.p is False and args.r is False:
        parser.error('Profile (-p) and Region (-r) are REQUIRED')
    else:
        ses = authmod.set_session(args.p, args.r)
        ec2 = ec2mod.ec2(ses)
        ec2_client = ses.client('ec2')
        ec2_info = ec2mod.ec2_get_info(ses)

    check_value = ec2_info.instance_info_by_name(args.i)
    if check_value[0] and check_value[1]:
        instance_id = check_value[1][0]['Instances'][0]['InstanceId']
    else:
        instance_id = args.i

    if args.c == 'state':
        response = get_state(instance_id)
        print(response[1])
    elif args.c == 'start':
        response = ec2.start(instance_id)
        print(response[1]['StartingInstances'][0]['CurrentState']['Name'])
    elif args.c == 'stop':
        response = ec2.stop(instance_id)
        print(response[1]['StoppingInstances'][0]['CurrentState']['Name'])

else:
    AWS_Profile = input('AWS Profile Name: ')
    AWS_Region = input('AWS Region: ')
    ses = authmod.set_session(AWS_Profile, AWS_Region)
    ec2 = ec2mod.ec2(ses)
    ec2_client = ses.client('ec2')
    ec2_info = ec2mod.ec2_get_info(ses)
