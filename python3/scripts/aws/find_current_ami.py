# Find the current release of an AMI by name
# AMI name example: 'ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server*'
# Maintained By: Lucas Rountree (lredvtree@gmail.com)

# Import General Modules
import sys

# Import Custom Modules
sys.path.append('../../modules/aws')
import auth_modules as authmod
import ec2_modules as ec2mod

def ami_list(OWNER, ARCH, PUB, NAME):
    response = ec2_info.find_ami_name(OWNER, ARCH, PUB, NAME)
    if not response[0]:
        print(response[1])
        sys.exit(1)
    return response[1]

def current_ami(LIST):
    creation_dates = []
    for IMAGE in LIST:
        creation_dates.append(IMAGE['CreationDate'])
    creation_dates.sort()
    current_release_date = creation_dates[-1]
    for IMAGE in LIST:
        if IMAGE['CreationDate'] == current_release_date:
            response = IMAGE['ImageId']
    return response

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Find the most recent release of an AMI by name', prog='find_current_ami')
    parser.add_argument('-p', action='store', type=str, default='default', help='AWS profile to use, from credentials file. Default is "default"')
    parser.add_argument('-r', action='store', type=str, default='us-west-2', help='AWS region, default is "us-west-2"')
    parser.add_argument('-o', action='store', type=str, required=True, default=False, help='AWS account ID of the AMI owner')
    parser.add_argument('-a', action='store', type=str, required=True, choices=['i386', 'x86_64', 'arm64'], help='Image system architecture')
    parser.add_argument('-i', action='store', type=str, required=True, choices=['true', 'false'], help='Boolean if the image is public or not')
    parser.add_argument('-n', action='store', type=str, required=True, help='string to find as AMI name')

    args = parser.parse_args()

    if args.p is False and args.r is False:
        parser.error('Profile (-p) and Region (-r) are REQUIRED')
    else:
        ses = authmod.set_session(args.p, args.r)
        ec2_info = ec2mod.ec2_get_info(ses)
    if args.o is False:
        parser.error('Please supply an owner ID')
    if args.a is False:
        parser.error('Please supply system architecture')
    if args.i is False:
        parser.error('Please supply bolean for public image')
    if args.n is False:
        parser.error('Please supply a name to search against')

    get_ami_list = ami_list(args.o, args.a, args.i, args.n)
    print(current_ami(get_ami_list))

else:
    AWS_Profile = input('MFA Profile Name: ')
    AWS_Region = input('AWS Region: ')
    ses = authmod.set_session(AWS_Profile, AWS_Region)
    ec2_info = ec2mod.ec2_get_info(ses)
    get_ami_list = ami_list(OWNER, ARCH, PUB, NAME)
    print(current_ami(get_ami_list))
