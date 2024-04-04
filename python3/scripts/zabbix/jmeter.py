#! /bin/python3

# Run Jmeter test and parse the CSV output to a list of dictonary items
# Maintained By: Lucas Rountree

# Import General Modules
import csv, subprocess, sys, json, os, re
from datetime import datetime

# Set Variables
time_now = datetime.now().strftime('%Y_%m_%d_%H%M%S')
jmeter = '/usr/local/bin/apache-jmeter-5.6.2/bin/jmeter'
csv_dir = '/git/aws/python/scripts/zabbix/'
csv_file = 'jmeter_' + time_now + '.csv'
csv_path = csv_dir + csv_file
jmx_path = '/git/Jmeter/'

# Run Jmeter test
def run_jmeter(jmx_file):
    try:
        subprocess.run(jmeter + ' -n' + ' -t ' + jmx_path + jmx_file + ' -l ' + csv_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    except:
        return [False, sys.exc_info()[1]]
    return [True]

# Read CSV into json
def to_json(csv_path, new_line=''):
    with open(csv_path, newline=new_line) as CSV:
        response = csv.DictReader(CSV)
        response_list = []
        for (I, ROW) in enumerate(response, start=1):
            ROW['test_count'] = I
            response_list.append(ROW)
    if not response_list:
        return [False, sys.exc_info()[1]]
    return [True, json.dumps(response_list)]

# Clean Up
def clean_up(DIR, MATCH):
    for FILE in os.listdir(DIR):
        if re.search(MATCH, FILE):
            os.remove(os.path.join(DIR, FILE))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate UI test output with jmeter', prog='jmeter')
    parser.add_argument('-j', action='store', type=str, help='JMX file name to run jmeter against')

    args = parser.parse_args()

    if args.j is False:
        parser.error('JMX file (-j) is required!')
    else:
        generate_file = run_jmeter(args.j)
        if generate_file[0]:
            get_list = to_json(csv_path)
            print(get_list[1])
            if get_list[0]:
                clean_up(csv_dir, csv_file)
        else:
            print(generate_file[1])
            sys.exit(1)

