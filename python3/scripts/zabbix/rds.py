#! /bin/python3

# Get AWS RDS Metric Values
# Maintained By: Lucas Rountree (lredvtree@gmail.com)
        
# Import General Modules
import sys, argparse, json
from datetime import datetime, timedelta

# Import Custom Modules
sys.path.append('/git/aws/python/modules')
from auth_modules import no_session as session
from get_metric import get_metric
from rds_modules import get_info, rds

# Get datetime
time_now = datetime.now()
time_min_1 = time_now - timedelta(seconds=60)
time_min_5 = time_now - timedelta(seconds=300)

# Add Arguments
parser = argparse.ArgumentParser(description='Zabbix get AWS RDS Cloudwatch Metric Values', prog='rds')
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
rds_info = get_info(ses)
rds = rds(ses)

def stat_metric(name_space, metric_name, dimension_name, dimension_value, time_period=60, stat_type='Average', stime=time_min_1, etime=time_now):
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

## RDS Instance Metrics
if pname == 'rds_instance':
    get_instance_arn = rds.db_arn_from_name(args.i)
    if not get_instance_arn[0]:
        print(get_instance_arn[1])
        sys.exit(1)
    instance_arn = get_instance_arn[1]

    def rds_metric(METRIC):
        return stat_metric('AWS/RDS', METRIC, 'DBInstanceIdentifier', args.i)

    if mname == 'storage':
        total_storage = rds.db_storage(args.i)
        if not total_storage[0]:
            print(total_storage[1])
            sys.exit(1)
        free_storage = round(rds_metric('FreeStorageSpace') / 1000000000)
        free_percent = (free_storage / total_storage[1]) * 100
        if free_percent > 100:
            free_percent = 100
        used_storage = (total_storage[1] - free_storage)
        if used_storage < 0:
            used_storage = 0
        response = json.dumps({'total': total_storage[1], 'free': free_storage, 'pfree': free_percent, 'used': used_storage})
        print(response)
    elif mname == 'performance':
        write_iops = rds_metric('WriteIOPS')
        read_iops = rds_metric('ReadIOPS')
        write_latency = rds_metric('WriteLatency')
        read_latency = rds_metric('ReadLatency')
        response = json.dumps({'write': [write_iops, write_latency], 'read': [read_iops, read_latency]})
        print(response)
    elif mname == 'memory':
        total_memory = rds.db_memory(args.i)
        if not total_memory[0]:
            print(total_memory[1])
            sys.exit(1)
        free_memory = round(rds_metric('FreeableMemory') / 1000000)
        free_percent = (free_memory / total_memory[1]) * 100
        used_memory = (total_memory[1] - free_memory)
        if used_memory < 0:
            used_memory = 0
        response = json.dumps({'total': total_memory[1], 'free': free_memory, 'pfree': free_percent, 'used': used_memory})
        print(response)
    elif mname == 'cpu':
        print(rds_metric('CPUUtilization'))
    elif mname == 'connections':
        print(rds_metric('DatabaseConnections'))
    else:
        print('Invalid RDS Instance Metric Provided')

elif pname == 'rds_info':
    get_instance_arn = rds.db_arn_from_name(args.i)
    if not get_instance_arn[0]:
        print(get_instance_arn[1])
        sys.exit(1)
    instance_arn = get_instance_arn[1]

    get_instance_info = rds_info.db_info_from_name(args.i)
    if not get_instance_info[0]:
        print(get_instance_info[1])
        sys.exit(1)
    db_info = get_instance_info[1]

    if mname == 'all':
        print(db_info)
    elif mname == 'id':
        print(db_info['DBInstanceIdentifier'])
    elif mname == 'type':
        print(db_info['DBInstanceClass'])
    elif mname == 'engine':
        print(db_info['Engine'])
    elif mname == 'endpoint':
        print(db_info['Endpoint']['Address'])
    elif mname == 'port':
        print(db_info['Endpoint']['Port'])
    elif mname == 'storage':
        print(db_info['AllocatedStorage'], db_info['StorageType'])
    elif mname == 'groups':
        print('Security Groups:', db_info['VpcSecurityGroups'], 'Parameter Groups:', db_info['DBParameterGroups'])
    elif mname == 'poc':
        get_poc = rds_info.db_tag_value(instance_arn, 'poc')
        if not get_poc[0]:
            print(get_poc[1])
            sys.exit(1)
        print(get_poc)
    elif mname == 'az':
        print(db_info['AvailabilityZone'])
    else:
        print('Unknown RDS instance info value provided')

else:
    print('Invalid Metric Prefix Provided')
