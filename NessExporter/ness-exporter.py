#!/usr/bin/python


import argparse
import time
import getpass
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import progress

# Disable Insecure Warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

HEADERS = "" 

parser = argparse.ArgumentParser(description="Script will download all scans in every format")
parser.add_argument("-n", "--nessus", help="Points Script to Nessus Instance", default="https://localhost:8834")
parser.add_argument("-p", "--path", default="/home/%s/Downloads" %getpass.getuser(), help="Path to save downloaded files")
args = parser.parse_args()

NESSUS_INSTANCE = args.nessus
PATH = args.path


# Function is used to login to the Nessus Instance
def nessus_login():
   
	print("[*] Log into Nessus Instance => %s" %NESSUS_INSTANCE)
	print("="*len("[*] Log into Nessus Instance => %s" %NESSUS_INSTANCE)) 

	while True:
		username = raw_input("[*] Username: ")
		password = getpass.getpass("[*] Password: ")

		login_request = requests.post(NESSUS_INSTANCE+"/session", data={"username": username, "password": password}, verify=False) 

		if login_request.status_code == 200:
			print("[+] Authentication Successful")
			time.sleep(0.5)        

			return json.loads(login_request.content)["token"]
		else:
		    print("[!] Check Authentication")
		    continue


# Function will retrieve list of scans
def retrieve_scans():

	scan_list = {}

	scans = json.loads(requests.get(NESSUS_INSTANCE+"/scans", verify=False, headers=HEADERS).content)["scans"]

	for scan in scans:
		if scan["status"] != "empty":
			scan_list[scan["name"].encode()] = scan["id"]
	
	return scan_list


def retrieve_export_request(scan_list):

	formats = ["nessus", "pdf", "html", "csv"]

	increment = 0

	print("[*] Save Directory: %s" %PATH)
	print("[*] Downloading Files....")

	for name,id in scan_list.iteritems():
		for format in formats:
			if format is"nessus" or format is "csv":
				export_request = json.loads(requests.post(NESSUS_INSTANCE+"/scans/%s/export" %str(id), headers=HEADERS, verify=False, data=json.dumps({"format": format})).content)["file"]
			elif format is "pdf" or format is "html":
				export_request = json.loads(requests.post(NESSUS_INSTANCE+"/scans/%s/export" %str(id), headers=HEADERS, verify=False, data=json.dumps({"format" : format, "chapters" : "vuln_hosts_summary"})).content)["file"]

			export_request_check(name,id,export_request, format)
		
		increment += 1
		progress.progress(increment, len(scan_list))


def export_request_check(name,id,file_request,format):

	while True:
		if json.loads(requests.get(NESSUS_INSTANCE+"/scans/%s/export/%s/status" %(str(id), str(file_request)), verify=False, headers=HEADERS).content)["status"] == "ready":
			download_file_request(name,id,file_request,format)
			break
		else:
			time.sleep(1)

def download_file_request(name,id, file_request,format):

	download = requests.get(NESSUS_INSTANCE+"/scans/%s/export/%s/download" %(str(id), str(file_request)), verify=False, headers=HEADERS)

	if format == "nessus":
		with open(PATH+"/%s.nessus" %name, "wb") as handle:
			for chunk in download.iter_content(chunk_size=128):
				handle.write(chunk)
	elif format == "html":
		with open(PATH+"/%s.html" %name, "wb") as handle:
			for chunk in download.iter_content(chunk_size=128):
				handle.write(chunk)
	elif format == "csv":
		with open(PATH+"/%s.csv" %name, "wb") as handle:
			for chunk in download.iter_content(chunk_size=128):
				handle.write(chunk)
	elif format == "pdf":
		with open(PATH+"/%s.pdf" %name, "wb") as handle:
			for chunk in download.iter_content(chunk_size=128):
				handle.write(chunk)


def main():

	global HEADERS

	HEADERS = {"X-Cookie" : "token=%s" %nessus_login(),
				"Content-Type" : "application/json"}
	
	scans = retrieve_scans()
	retrieve_export_request(scans)
	print("[+] Downloads Complete")



main()








