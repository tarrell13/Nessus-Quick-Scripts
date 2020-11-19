#!/usr/bin/python


import argparse
import time
import getpass
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import re
import sys
import progress

# Disable Insecure Warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

HEADERS = "" 

parser = argparse.ArgumentParser(description="Script will download all scans in every format")
parser.add_argument("-n", "--nessus", help="Points Script to Nessus Instance", default="https://localhost:8834")
parser.add_argument("-p", "--path", default="/home/%s/Downloads" %getpass.getuser(), help="Path to save downloaded files")
parser.add_argument("-f", "--formats", help="Specify format, nessus, pdf, html, csv, default is all")
parser.add_argument("--folder",help="Download scans from a folder",action="store_true")
args = parser.parse_args()

NESSUS_INSTANCE = args.nessus
PATH = args.path
FORMATS = []
FOLDER = False

if args.folder:
    FOLDER = True

if args.formats:
    if re.search(",",args.formats):
        formats = str(args.formats).split(",")

        for format in formats:
            FORMATS.append(str(format))
    else:
        FORMATS.append(args.formats)

else:
    FORMATS = ["nessus", "pdf", "html", "csv"]

# Function is used to login to the Nessus Instance
def nessus_login():

    print(("[*] Log into Nessus Instance => %s" %NESSUS_INSTANCE))
    print(("="*len("[*] Log into Nessus Instance => %s" %NESSUS_INSTANCE))) 

    while True:
        username = input("[*] Username: ")
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
def retrieve_scans(folderid=None):

    scan_list = {}

    if FOLDER:
        scans = json.loads(requests.get(NESSUS_INSTANCE + "/scans", verify=False, data={"folder_id":folderid},headers=HEADERS).content)["scans"]
    else:
        scans = json.loads(requests.get(NESSUS_INSTANCE+"/scans", verify=False, headers=HEADERS).content)["scans"]

    for scan in scans:
        if scan["status"] != "empty":
            scan_list[scan["name"].encode()] = scan["id"]

    return scan_list


def retrieve_export_request(scan_list):

    increment = 0

    print(("[*] Save Directory: %s" %PATH))
    print(("[*] Formats => " + str(FORMATS)))
    print("[*] Downloading Files....")

    for name,id in scan_list.items():
        for format in FORMATS:  
            if format == "nessus" or format == "csv":
                export_request = json.loads(requests.post(NESSUS_INSTANCE+"/scans/%s/export" %str(id), headers=HEADERS, verify=False, data=json.dumps({"format": format})).content)["token"]
            elif format == "pdf" or format == "html":
                export_request = json.loads(requests.post(NESSUS_INSTANCE+"/scans/%s/export" %str(id), headers=HEADERS, verify=False, data=json.dumps({"format" : format, "chapters" : "vuln_hosts_summary"})).content)["token"]

            export_request_check(name,id,export_request, format)

            increment += 1
            progress.progress(increment, len(scan_list))


def export_request_check(name,id,file_request,format):

    while True:
        if json.loads(requests.get(NESSUS_INSTANCE+"/tokens/%s/status" %(str(file_request)), verify=False, headers=HEADERS).content)["status"] == "ready":
            download_file_request(name,id,file_request,format)
            break
        else:
            time.sleep(1)

def download_file_request(name,id, file_request,format):

    download = requests.get(NESSUS_INSTANCE+"/tokens/%s/download" %(str(file_request)), verify=False, headers=HEADERS)

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


def RetrieveFolderChoice():

    folder_list = []
    dump = json.loads(requests.get(NESSUS_INSTANCE+"/folders",verify=False,headers=HEADERS).content)["folders"]

    for folder in dump:
        if folder["type"] == "trash":
            continue
        else:
            folder_list.append(folder)

    print(("="*len("NESSUS FOLDERs")))
    print("NESSUS FOLDERS ")
    print(("="*len("NESSUS FOLDERS")))

    for folder in folder_list:
        print(("ID [ %s  ] :: %s" %(folder["id"], folder["name"])))

    found = False
    while found is False:

        choice = input("Choose Folder ID: ")
        for folder in folder_list:
            if str(folder["id"]) == choice:
                found = True

        if found is False:
            print("(!) Invalid Selection")

    print("\n")
    return choice

def main():

    global HEADERS

    HEADERS = {"X-Cookie" : "token=%s" %nessus_login(),
            "Content-Type" : "application/json"}

    if FOLDER:
        scans = retrieve_scans(RetrieveFolderChoice())
    else:
        scans = retrieve_scans()

    retrieve_export_request(scans)
    print("\n[+] Downloads Complete")



main()








