#! /bin/python3

# Run Jmeter test and parse the CSV output to a list of dictonary items
# Maintained By: Lucas Rountree

# Import General Modules
import csv, subprocess, sys, json, os, re, logging
from datetime import datetime
from zabbix_utils import Sender

# Set up logging
logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        filename='/var/log/zabbix/zabbix_sender.log',
        encoding='utf-8',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S'
)

# Set Variables
time_now = datetime.now().strftime('%Y_%m_%d_%H%M%S')
jmeter = '/usr/local/bin/apache-jmeter-5.6.2/bin/jmeter'
csv_dir = '/git/aws/python/scripts/zabbix/'
csv_file = 'jmeter_' + time_now + '.csv'
csv_path = csv_dir + csv_file
jmx_path = '/git/Jmeter/'
dev_exclude = ['CyberActivityAPI', 'API_Test_Prod', '_Prod', 'API_Tests']
prod_exclude = ['CyberActivityAPI', 'API_Test_Prod', 'API_Tests']
sender = Sender(server='localhost', port=10051)

# Run Jmeter test
def run_jmeter(jmx_dir, jmx_file):
    try:
        subprocess.run(jmeter + ' -n' + ' -t ' + jmx_dir + jmx_file + ' -l ' + csv_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    except:
        return [False, sys.exc_info()[1]]
    return [True]

# Read CSV into json
def to_json(csv_path, new_line=''):
    with open(csv_path, newline=new_line) as CSV:
        response = csv.DictReader(CSV)
        response_list = []
        test_list = []
        response_dict = {}
        for OBJECT in response:
            response_list.append(OBJECT)
            test_list.append(OBJECT['label'].split(':')[0])
        for TEST in set(test_list):
            response_dict[TEST] = []
            for OBJECT in response_list:
                if OBJECT['label'].split(':')[0] == TEST:
                    response_dict[TEST].append(OBJECT)
    if not response_dict:
        return [False, sys.exc_info()[1]]
    return [True, response_dict]

def check_response(RES):
    bad_response = {}
    send_response = False
    for KEY, VALUE in RES.items():
        bad_response[KEY] = []
        for ITEM in VALUE:
            if ITEM['responseCode'] not in ['200', '307', '502']:
                bad_response[KEY].append(ITEM)
                send_response = True
    return [send_response, bad_response]

def zabbix_sender(DATA):
    TRAP_DATA = ''
    for KEY, VALUE in DATA.items():
        if VALUE:
            for ITEM in VALUE:
                if len(ITEM['label'].split(':')) == 1:
                    LABEL = ITEM['label']
                else:
                    LABEL = ITEM['label'].split(':')[1]
                TRAP_DATA += "<b>Test Name:</b> " + KEY + "<br><b>Label:</b> " + LABEL + "<br><b>Response Code:</b> " + ITEM['responseCode'] + "<br><b>Thread Name:</b> " + ITEM['threadName'] + "<br><b>URL:</b> " + ITEM['URL'] + "<br>----<br>"
    return TRAP_DATA

# Clean Up
def clean_up(DIR, MATCH):
    for FILE in os.listdir(DIR):
        if re.search(MATCH, FILE):
            os.remove(os.path.join(DIR, FILE))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate UI test output with jmeter', prog='jmeter')
    parser.add_argument('-e', action='store', choices=['dev', 'prod'], type=str, help='Environment to run against')

    args = parser.parse_args()

    if args.e is False:
        parser.error('environment (-e) is required!')

    else:
        send_data = ''
        if args.e == 'dev':
            target_host = 'host01.domain.com'
            jmx_dir = jmx_path + 'PATH_1/'
            for X in os.listdir(jmx_dir):
                if not [I for I in dev_exclude if I in X] and '.jmx' in X:
                    generate_file = run_jmeter(jmx_dir, X)
                    if generate_file[0]:
                        get_list = to_json(csv_path)
                        results_list = check_response(get_list[1])
                        if results_list[0]:
                            send_data += '<b>[' + X.split('.')[0] + ']</b>' + '<br>' + zabbix_sender(results_list[1])
                clean_up(csv_dir, csv_file)

        elif args.e == 'prod':
            target_host = 'host02.domain.com'
            jmx_dir = jmx_path + 'PATH_2/'
            for X in os.listdir(jmx_dir):
                if not [I for I in prod_exclude if I in X] and '.jmx' in X and '_Prod' in X:
                    generate_file = run_jmeter(jmx_dir, X)
                    if generate_file[0]:
                        get_list = to_json(csv_path)
                        results_list = check_response(get_list[1])
                        if results_list[0]:
                            send_data += '<b>' + X.split('.')[0] + '</b>' + '<br>' + zabbix_sender(results_list[1])
                clean_up(csv_dir, csv_file)

        else:
            print(generate_file[1])
            sys.exit(1)

        if send_data:
            sender.send_value(target_host, 'jmeter_test', send_data)
        else:
            sender.send_value(target_host, 'jmeter_test', 'OKAY')

