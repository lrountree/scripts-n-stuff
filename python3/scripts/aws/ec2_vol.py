# Check volumes attached to instance
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
    parser = argparse.ArgumentParser(description='Get attached volumes of AWS EC2 instances', prog='ec2')
    parser.add_argument('-p', action='store', type=str, default='default', help='AWS profile to use, from credentials file. Default is "default"')
    parser.add_argument('-r', action='store', type=str, default='us-west-2', help='AWS region, default is "us-west-2"')

    args = parser.parse_args()

    if args.p is False and args.r is False:
        parser.error('Profile (-p) and Region (-r) are REQUIRED')
    else:
        ses = authmod.set_session(args.p, args.r)
        ec2 = ec2mod.ec2(ses)
        ec2_client = ses.client('ec2')
        ec2_info = ec2mod.ec2_get_info(ses)

else:
    AWS_Profile = input('AWS Profile Name: ')
    AWS_Region = input('AWS Region: ')
    ses = authmod.set_session(AWS_Profile, AWS_Region)
    ec2 = ec2mod.ec2(ses)
    ec2_client = ses.client('ec2')
    ec2_info = ec2mod.ec2_get_info(ses)

instance_list = ec2_info.list_all_instances()

if not instance_list[0]:
    print(instance_list[1])

for INSTANCE in instance_list[1]:
    state = get_state(INSTANCE[1])

    if state[0] and state[1] == 'stopped':
        vol_list = ec2.get_volumes(INSTANCE[1])

        if vol_list[0]:
            volumes = []

            for VOL in vol_list[1]:
                if VOL['VolumeType'] == 'gp2':
                    volumes.append([VOL['VolumeId'], VOL['VolumeType']])

            if volumes:
                print('Instance Name:', INSTANCE[0])
                print('ID:', INSTANCE[1])
                print('State:', state[1])
                print('Volumes:')
                for X in volumes:
                    print(X[0], X[1])
                print('\n')
        else:
            print('No Volumes Found!\n')
