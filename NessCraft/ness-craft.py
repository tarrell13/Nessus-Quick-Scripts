#!/usr/bin/python

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import getpass
import json
from time import sleep
import argparse
import sys

# Disable Insecure Warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

###################
# Global Variables
#
#	NESSUS_INSTANCE => Points to your nessus instance
#	INPUT_FILENAME => Points to the input file containing IP addresses/Hostnames to be added to scan	
#	VERBOSE => Provides additional information
#	CHUNKS => Splits the input file into specified chunks per scan
#	MODE => Script will operate in two (2) Modes : Create Scans [1] , Download Files [2]
#	TOTAL_SCAN_COUNT => Determines the total scan count for created scans
#
###################

NESSUS_INSTANCE = ""
INPUT_FILENAME = ""
VERBOSE = False
CHUNKS = 0
HEADER = ""
TOTAL_SCAN_COUNT = 0
PREFIX = ""

# Add argument parse information here

parser = argparse.ArgumentParser(description="Script will create Nessus Scans using specified input file", usage="python ness-craft.py -n https://localhost:8834 -i ipList.txt -c 5")
parser.add_argument("-v", "--verbose", help="Increase Output Verbosity", action="store_true")
parser.add_argument("-c", "--chunks", help="Creates scans in specified chunks", type=int, default=0)
parser.add_argument("-n", "--nessus", help="Points script to specified Nessus Instance", required=True)
parser.add_argument("-i", "--input-file", help="Input File containing IP addresses/Hostnames to create scans from", required=True)
parser.add_argument("-p", "--prefix", help="Scans Prefix Name used for Scan, Default Name is Scan", type=str, default="Scan")
args = parser.parse_args()


NESSUS_INSTANCE = args.nessus 
INPUT_FILENAME = args.input_file

if args.chunks:
	CHUNKS = args.chunks

if args.verbose:
	VERBOSE = True

if args.prefix:
        PREFIX = args.prefix


# Function to log into Nessus Instance using Username and Password
def nessus_login():
    
    while True:
   
	print("[*] Log into Nessus Instance => %s" %NESSUS_INSTANCE)
	print("="*len("[*] Log into Nessus Instance => %s" %NESSUS_INSTANCE)) 
        username = raw_input("[*] Username: ")
        password = getpass.getpass("[*] Password: ")


        login_request = requests.post(NESSUS_INSTANCE+"/session", data={"username": username, "password": password}, verify=False) 

        if login_request.status_code == 200:
            print("[+] Authentication Successful")
	    sleep(0.5)        

            return json.loads(login_request.content)["token"]
        else:
            print("[!] Check Authentication")
            continue


# Function will create scans in specified chunks based on input file
def pull_current_scans():

	scan_list = []

	nessus_scan_list_json = json.loads(requests.get(NESSUS_INSTANCE+"/scans",headers=HEADER, verify=False).content)

	try:
		for scan in nessus_scan_list_json["scans"]:
    			scan_list.append(scan["name"].encode())

	except TypeError:
		return scan_list


    	if VERBOSE:
        	print("[+] Nessus Instance Created Scan Count = %d" %len(scan_list))

    	return scan_list


# Create generator object using HOSTs List file
def generator_list():

    with open(INPUT_FILENAME) as handle:
        for line in handle:
            	yield line.strip("\n")

# Function will chunk the scans up if user specified chunk groups
def chunk_input_file():

	host_list = []

	with open(INPUT_FILENAME) as handle:
		for line in handle:
			host_list.append(line.strip("\n"))

	hosts_groups = {}


	if CHUNKS > 0 and CHUNKS < len(host_list):

		host_group_counter = 1
		generated_hosts = generator_list()

		try:	
			while True:
				for chunk in range(CHUNKS):
					if host_group_counter in hosts_groups:
						hosts_groups[host_group_counter].append(generated_hosts.next())
					else:
						hosts_groups[host_group_counter] = []
						hosts_groups[host_group_counter].append(generated_hosts.next())

				host_group_counter += 1

		except StopIteration:
			pass

	else:
		hosts_groups[1] = []

		for host in host_list:
			hosts_groups[1].append(host)
			
	return hosts_groups	

# Function will pull the BASIC NETWORK SCAN template UUID
def retrieve_template_uuid():

	template_list = json.loads(requests.get(NESSUS_INSTANCE+"/editor/scan/templates", headers=HEADER, verify=False).content)["templates"]	

	for template in template_list:
		if template["title"] == "Basic Network Scan":
			uuid = template["uuid"]
			break

	return uuid


# Function will remove array elements and append each host to string for upload
def string_targets(targets):

	target_string = ""
	
	for host in range(len(targets)):
		target_string += targets[host]+","

	return target_string


# Function will create the scans within the Nessus Instance
def create_scans(scan_list, host_list):

	global TOTAL_SCAN_COUNT 

	current_scan_count = len(scan_list)

	fields = { 'uuid' : retrieve_template_uuid(), 'settings' : {'name' : "" , 'text_targets' : "" }}

    	for group,targets in host_list.iteritems():

		if len(targets) == 0:
			continue

		current_scan_count += 1
		fields["settings"]["text_targets"] = string_targets(targets)
		fields["settings"]["name"] = "%s - %d" %(PREFIX, current_scan_count)
		hmm = requests.post(NESSUS_INSTANCE+"/scans", headers=HEADER, data=json.dumps(fields), verify=False)
		
		if hmm.status_code == 200:
			TOTAL_SCAN_COUNT += 1
			if VERBOSE:
				print("[+] %s - %d Created" %(PREFIX, current_scan_count))

		else:
			print("[!] Something went wrong 'Scan - %d' => %s" %(current_scan_count, hmm.content))
			
			if VERBOSE:
				print("[-] POST Data for 'Scan - %d' => %s" %(current_scan_count, json.dumps(fields, separators=(",",":"))))	
		
	
def check_nessus_version():

	r = requests.post(NESSUS_INSTANCE+"/server/properties", headers=HEADER, verify=False)

	if r.status_code == 200:
		version = json.loads(r.content)['nessus_type']
		server = float(json.loads(r.content)['server_version'])

		if server >= 8 and version.lower() == 'nessus manager':
			return True
		elif server < 8:
			return True 
		else:
			return False 

	else:
		return False



def main():

	global HEADER 

	HEADER = {"X-Cookie": "token=%s" %nessus_login(),
		  "Content-Type": "application/json"}

	
	if check_nessus_version():
		groups = chunk_input_file()
		create_scans(pull_current_scans(),groups)
		print("[+] Total Scans Created: %d" %TOTAL_SCAN_COUNT)
	else:
		print("[!] Scanner needs to be Nessus Manager")

	sys.exit()

	    
main()




