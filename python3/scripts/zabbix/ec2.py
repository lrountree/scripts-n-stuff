#! /bin/python3

# Get AWS EC2 Metric Values
# Maintained By: Lucas Rountree (lredvtree@gmail.com)
        
# Import General Modules
import sys, argparse
from datetime import datetime, timedelta

# Import Custom Modules
sys.path.append('/git/aws/python/modules')
from auth_modules import no_session as session
from get_metric import get_metric
from ec2_modules import ec2_get_info, ec2
from add_modules import get_info, elbv2

# Get datetime
time_now = datetime.now()
time_min_1 = time_now - timedelta(seconds=60)
time_min_5 = time_now - timedelta(seconds=300)

# Add Arguments
parser = argparse.ArgumentParser(description='Zabbix get AWS EC2 Cloudwatch Metric Values', prog='ec2')
parser.add_argument(
        '-i',
        action='store',
        type=str,
        required=True,
        help='Resource Name'
    )  
parser.add_argument(
        '-r',
        action='store',
        type=str,
        default='us-west-2',
        help='AWS Region'
    )
parser.add_argument(
        '-m',
        action='store',
        type=str,
        help='Metric Name'
    )
parser.add_argument(
        '-t',
        action='store',
        type=int,
        default=60,
        help='Time period'
    )
parser.add_argument(
        '-s',
        action='store',
        type=str,
        default='Average',
        help='Statistic type'
    )
args = parser.parse_args()

# Set up functions
ses = session(args.r)
metric = get_metric(ses)
ec2_info = ec2_get_info(ses)
ec2 = ec2(ses)
get_info = get_info(ses)
elbv2 = elbv2(ses)

def stat_metric(name_space, metric_name, dimension_name, dimension_value, time_period=60, stat_type='Average', stime=time_min_5, etime=time_now):
    response = metric.cw_stat(
                name_space,
                metric_name,
                dimension_name,
                dimension_value,
                time_period,
                stat_type,
                stime,
                etime
            )
    return response

# Process metric requests
if len(args.m.split('.')) != 2:
    print('Please provide metric as: <service>.<metric>')
    sys.exit(1)
pname = args.m.split('.')[0]
mname = args.m.split('.')[1]

## Nat Gateway Metrics
if pname == 'ngw':
    nat_gateway_list = ec2.list_all_nat_gateways()
    nat_gateway_id = ''
    if nat_gateway_list[0]:
        for NGW in nat_gateway_list[1]:
            if NGW['Name'] == args.i:
                nat_gateway_id = NGW['ID']
    else:
        print(nat_gateway_list[1])
    if not nat_gateway_id:
        print('No NAT Gateway found with name:', args.i)

    def ngw_metric(METRIC):
        return stat_metric('AWS/NATGateway', METRIC, 'NatGatewayId', nat_gateway_id)

    if mname == 'state':
        state = ec2.nat_gateway_state(nat_gateway_id)
        print(state[1])
    elif mname == 'id':
        print(nat_gateway_id)
    elif mname == 'connection_attempt':
        print(ngw_metric('ConnectionAttemptCount'))
    elif mname == 'connections_established':
        print(ngw_metric('ConnectionEstablishedCount'))
    elif mname == 'connections':
        print(ngw_metric('ActiveConnectionCount'))
    elif mname == 'idle':
        print(ngw_metric('IdleTimeoutCount'))
    elif mname == 'bytes_in_des':
        print(ngw_metric('BytesInFromDestination'))
    elif mname == 'bytes_out_des':
        print(ngw_metric('BytesOutToDestination'))
    elif mname == 'bytes_in_source':
        print(ngw_metric('BytesInFromSource'))
    elif mname == 'bytes_out_source':
        print(ngw_metric('BytesOutToSource'))
    else:
        print('Invalid NAT Gateway Metric Provided')

## EC2 Instance Metrics
elif pname == 'ec2':
    get_instance_id = ec2.id(args.i)
    if not get_instance_id[0]:
        print(get_instance_id[1])
    instance_id = get_instance_id[1][0]

    def ec2_metric(METRIC):
        return stat_metric('AWS/EC2', METRIC, 'InstanceId', instance_id)

    if mname == 'status':
        print(ec2_metric('StatusCheckFailed'))
    elif mname == 'cpu':
        print(ec2_metric('CPUUtilization'))
    elif mname == 'read':
        print(ec2_metric('EBSReadOps'))
    elif mname == 'write':
        print(ec2_metric('EBSWriteOps'))
    elif mname == 'netin':
        print(ec2_metric('NetworkIn'))
    elif mname == 'netout':
        print(ec2_metric('NetworkOut'))
    else:
        print('Invalid EC2 Instance Metric Provided')

elif pname == 'ec2_info':
    get_instance_id = ec2.id(args.i)
    if not get_instance_id[0]:
        print(get_instance_id[1])
    instance_id = get_instance_id[1][0]

    get_instance_info = ec2_info.instance_info_by_name(args.i)
    if not get_instance_info[0]:
        print(get_instance_info[1])
    instance_info = get_instance_info[1][0]['Instances'][0]
    
    if mname == 'all':
        print(instance_info)
    elif mname == 'type':
        print(instance_info['InstanceType'])
    elif mname == 'tags':
        print(instance_info['Tags'])
    elif mname == 'az':
        print(instance_info['Placement']['AvailabilityZone'])
    elif mname == 'subnet':
        subnet_id = instance_info['SubnetId']
        print(ec2_info.subnet_name(subnet_id)[1])
    elif mname == 'groups':
        groups = ''
        for ITEM in instance_info['SecurityGroups']:
            groups += ITEM['GroupName'] + '\n'
        print(groups)
    elif mname == 'poc':
        poc = ec2_info.instance_tag_value(instance_id, 'poc')
        print(poc[1])
    else:
        print('Invalid EC2 Info Key Provided')

## Application Load Balancer Metrics
elif pname == 'app':
    lb_id = elbv2.lb_id_from_name(args.i)
    if not lb_id[0]:
        print(lb_id[1])
        sys.exit(1)

    def elbv2_metric(METRIC):
        return stat_metric('AWS/ApplicationELB', METRIC, 'LoadBalancer', lb_id[1])
    
    if mname == 'id':
        print(lb_id[1])
    elif mname == 'response':
        print(elbv2_metric('TargetResponseTime'))
    elif mname == 'unhealthy':
        print(elbv2_metric('UnhealthyRoutingRequestCount'))
    elif mname == 'consumed':
        print(elbv2_metric('ConsumedLCUs'))
    elif mname == 'connections':
        print(elbv2_metric('ActiveConnectionCount'))
    elif mname == 'requests':
        print(elbv2_metric('RequestCount'))
    elif mname == 'new':
        print(elbv2_metric('NewConnectionCount'))
    elif mname == 'bytes':
        print(elbv2_metric('ProcessedBytes'))
    else:
        print('Invalid ELBv2 Metric Provided')

elif pname == 'app_info':
    lb_info = elbv2.lb_info_from_name(args.i)
    if not lb_info[0]:
        print(lb_info[1])
        sys.exit(1)

    if mname == 'all':
        print(lb_info[1])
    elif mname == 'arn':
        print(lb_info[1]['LoadBalancerArn'])
    elif mname == 'dns':
        print(lb_info[1]['DNSName'])
    elif mname == 'name':
        print(lb_info[1]['LoadBalancerName'])
    elif mname == 'type':
        print(lb_info[1]['Type'], lb_info[1]['Scheme'])
    elif mname == 'vpc':
        print(lb_info[1]['VpcId'])
    elif mname == 'state':
        print(lb_info[1]['State']['Code'])
    elif mname == 'az':
        zones = ''
        for ITEM in lb_info[1]['AvailabilityZones']:
            zones += 'Zone: ' + ITEM['ZoneName'] + ' Subnet: ' + ITEM['SubnetId'] + '\n'
        print(zones)
    elif mname == 'groups':
        groups = ''
        for ITEM in lb_info[1]['SecurityGroups']:
            groups += ITEM + '\n'
        print(groups)
    elif mname == 'poc':
        poc = elbv2.lb_tag_value(lb_info[1]['LoadBalancerArn'], 'poc')
        print(poc[1])
    else:
        print('Invalid ELBv2 Info Key Provided')

else:
    print('Invalid Metric Prefix Provided')
