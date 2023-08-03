# Get resource counts of specific types from AWS
# number of EC2 instances
# number of Amazon RedShift Clusters
# number of ELB
# number of Internet gateways
# NAT Gateways
# ECS - Clusters
# EKS - Clusters
# number of hosts not running containers
# number of hosts running containers

# Maintained by: Lucas Rountree (lredvtree@gmail.com)

# Import General Modules
import sys

# Import AWS Modules
import boto3, botocore

# Import Custom Modules
sys.path.append('../../modules/aws')
from auth_modules import set_session as ses
import ec2_modules, rds_modules, other_modules

set_session = ses

# Run as script
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
            description='Get resource counts.',
            prog='aws_audit.py',
            epilog='Example: python3 aws_audit.py -p <aws_mfa_profile> -r <region>')
    parser.add_argument('-p',
            action='store',
            default=False,
            required=True,
            type=str,
            help='AWS CLI profile name, from credentials file')
    parser.add_argument('-r',
            action='store',
            default='us-west-2',
            required=False,
            type=str,
            help='AWS region to run script in')

    args = parser.parse_args()
    print('Account:', args.p)
    session = set_session(args.p, args.r)
    region_list = ec2_modules.ec2_get_info(session).get_regions()

    if not region_list[0]:
        print('Could not get region list:')
        print(region_list[1])
        sys.exit(1)

    ec2_total = 0
    elbv2_total = 0
    redshift_total = 0
    rds_total = 0
    igw_total = 0
    nat_total = 0
    ecs_total = 0
    eks_total = 0

#    region_list = [True, ['us-west-2']]

    for REGION in region_list[1]:
        SES = set_session(args.p, REGION)
        print('\n\tREGION:', REGION)

        ec2_count = ec2_modules.ec2_get_info(SES).list_all_instances()
        if not ec2_count[0]:
            print('Could not get ec2 count:')
            print(ec2_count[1])
        else:
            ec2_total += len(ec2_count[1])
            print('\t\tEC2 COUNT:', len(ec2_count[1]))

        elbv2_count = other_modules.elbv2_get_info(SES).list_all_elbs()
        if not elbv2_count[0]:
            print('Could not get elbv2 count:')
            print(elbv2_count[1])
        else:
            elbv2_total += len(elbv2_count[1])
            print('\t\tELBV2 COUNT:', len(elbv2_count[1]))

        redshift_count = other.redshift_get_info(SES).list_all_clusters()
        if not redshift_count[0]:
            print('Could not get redshift cluster count:')
            print(redshift_count[1])
        else:
            redshift_total += len(redshift_count[1])
            print('\t\tREDSHIFT CLUSTER COUNT:', len(redshift_count[1]))

        rds_instance_count = rds_modules.rds_get_info(SES).list_all_instances()
        if not rds_instance_count[0]:
            print('Could not get RDS instance count:')
            print(rds_instance_count[1])
        else:
            rds_total += len(rds_instance_count[1])
            print('\t\tRDS INSTANCE COUNT:', len(rds_instance_count[1]))

        igw_count = ec2_modules.ec2_get_info(SES).list_all_internet_gateways()
        if not igw_count[0]:
            print('Could not get internet gateway count:')
            print(igw_count[1])
        else:
            igw_total += len(igw_count[1])
            print('\t\tINTERNET GATEWAY COUNT:', len(igw_count[1]))

        nat_count = ec2_modules.ec2_get_info(SES).list_all_nat_gateways()
        if not nat_count[0]:
            print('Could not get NAT gateway count:')
            print(nat_count[1])
        else:
            nat_total += len(nat_count[1])
            print('\t\tNAT GATEWAY COUNT:', len(nat_count[1]))

        ecs_count = ec2_modules.ecs_get_info(SES).list_all_clusters()
        if not ecs_count[0]:
            print('Could not get ECS cluster count:')
            print(ecs_count[1])
        else:
            ecs_total += len(ecs_count[1])
            print('\t\tECS CLUSTER COUNT:', len(ecs_count[1]))

        eks_count = other_modules.eks_get_info(SES).list_all_clusters()
        if not eks_count[0]:
            print('Could not get EKS cluster count:')
            print(eks_count[1])
        else:
            eks_total += len(eks_count[1])
            print('\t\tEKS CLUSTER COUNT:', len(eks_count[1]))

    print('\nTOTALS:')
    print('\tEC2:', ec2_total)
    print('\tELBv2:', elbv2_total)
    print('\tREDSHIFT:', redshift_total)
    print('\tRDS:', rds_total)
    print('\tIGW:', igw_total)
    print('\tNAT:', nat_total)
    print('\tECS:', ecs_total)
    print('\tEKS:', eks_total)
