#! /bin/python3

# Get AWS Cloudwatch Metrics
# Maintained By: Lucas Rountree (lredvtree@gmail.com)
        
# Import General Modules
import sys, boto3, botocore

# Get Metrics
class get_metric:
    '''
    Get AWS Cloudwatch Metrics
    from get_metric import get_metric
    get_metric = get_metric(<session>)
    get_metric.cw_stat(<metric name space>, <metric name>, <dimension name>, <dimension value>, <time period>, <statistic type>, <start time>, <end time>)
    outputs average value
    '''

    def __init__(self, session):
        self.cw_client = session.client('cloudwatch')

    def cw_stat(self, name_space, metric_name, id_name, id_id, time_period, stat_type, stime, etime):
        try:
            response = self.cw_client.get_metric_statistics(
                Namespace=name_space,
                MetricName=metric_name,
                Dimensions=[
                    {
                        'Name': id_name,
                        'Value': id_id
                    }
                ],
                Period=time_period,
                Statistics=[
                    stat_type
                ],
                StartTime=stime,
                EndTime=etime
            )
        except Exception as ERROR:
            print(ERROR)
            sys.exit(1)

    
        response_list = [X['Average'] for X in response['Datapoints']]
        if not response_list:
            return 0
        get_average = sum(response_list) / len(response_list)
        return get_average
