<<<<<<< HEAD
#!/usr/bin/env python3
=======
#!/usr/bin/python3
>>>>>>> dev


import argparse
import time
import getpass
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import re
import progress

# Disable Insecure Warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

HEADERS = ""

parser = argparse.ArgumentParser(description="Script will download all scans in every format")
parser.add_argument("-n", "--nessus", help="Points Script to Nessus Instance", default="https://localhost:8834")
parser.add_argument("-p", "--path", default="/home/%s/Downloads" % getpass.getuser(),
                    help="Path to save downloaded files")
parser.add_argument("-f", "--formats", help="Specify format, nessus, pdf, html, csv, default is all")
parser.add_argument("--folder", help="Download scans from a folder", action="store_true")
args = parser.parse_args()

NESSUS_INSTANCE = args.nessus
PATH = args.path
FORMATS = []
FOLDER = False

if args.folder:
    FOLDER = True

if args.formats:
    if re.search(",", args.formats):
        formats = str(args.formats).split(",")

        for format in formats:
            FORMATS.append(str(format))
    else:
        FORMATS.append(args.formats)

else:
    FORMATS = ["nessus", "pdf", "html", "csv"]


# Function is used to login to the Nessus Instance
def nessus_login():
<<<<<<< HEAD

    print(("[*] Log into Nessus Instance => %s" %NESSUS_INSTANCE))
    print(("="*len("[*] Log into Nessus Instance => %s" %NESSUS_INSTANCE))) 

=======
    print("[*] Log into Nessus Instance => %s" % NESSUS_INSTANCE)
    print("=" * len("[*] Log into Nessus Instance => %s" % NESSUS_INSTANCE))

>>>>>>> dev
    while True:
        username = input("[*] Username: ")
        password = getpass.getpass("[*] Password: ")

<<<<<<< HEAD
        login_request = requests.post(NESSUS_INSTANCE+"/session", data={"username": username, "password": password}, verify=False) 

        if login_request.status_code == 200:
            print("[+] Authentication Successful")
            time.sleep(0.5)        
=======
        login_request = requests.post(NESSUS_INSTANCE + "/session", data={"username": username, "password": password},
                                      verify=False)

        if login_request.status_code == 200:
            print("[+] Authentication Successful")
            time.sleep(0.5)
>>>>>>> dev

            return json.loads(login_request.content)["token"]
        else:
            print("[!] Check Authentication")
            continue


# Function will retrieve list of scans
def retrieve_scans(folderid=None):
    scan_list = {}

<<<<<<< HEAD
    scan_list = {}

    if FOLDER:
        scans = json.loads(requests.get(NESSUS_INSTANCE + "/scans", verify=False, data={"folder_id":folderid},headers=HEADERS).content)["scans"]
    else:
        scans = json.loads(requests.get(NESSUS_INSTANCE+"/scans", verify=False, headers=HEADERS).content)["scans"]

    for scan in scans:
        if scan["status"] != "empty":
            scan_list[scan["name"].encode()] = scan["id"]
=======
    if FOLDER:
        scans = json.loads(requests.get(NESSUS_INSTANCE + "/scans", verify=False, data={"folder_id": folderid},
                                        headers=HEADERS).content)["scans"]
    else:
        scans = json.loads(requests.get(NESSUS_INSTANCE + "/scans", verify=False, headers=HEADERS).content)["scans"]

    for scan in scans:
        if scan["status"] != "empty":
            scan_list[scan["name"]] = scan["id"]
>>>>>>> dev

    return scan_list


def retrieve_export_request(scan_list):

    increment = 0
<<<<<<< HEAD

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
=======

    print("[*] Save Directory: %s" % PATH)
    print("[*] Formats => " + str(FORMATS))
    print("[*] Downloading Files....")

    for name, id in scan_list.items():

        for format in FORMATS:
            if format == "nessus" or format == "csv":
                export_request = json.loads(requests.post(NESSUS_INSTANCE + "/scans/%s/export" % str(id), headers=HEADERS, verify=False, data=json.dumps({"format": format})).content.decode())
            elif format == "pdf" or format == "html":
                export_request = json.loads(requests.post(NESSUS_INSTANCE + "/scans/%s/export" % str(id), headers=HEADERS, verify=False,data=json.dumps({"format": format, "chapters": "vuln_hosts_summary"})).content.decode())
>>>>>>> dev

            export_request_check(name, id, export_request, format)

            ''' Show Progress '''
            increment += 1
            progress.progress(increment, len(FORMATS) * len(scan_list))

<<<<<<< HEAD
    while True:
        if json.loads(requests.get(NESSUS_INSTANCE+"/tokens/%s/status" %(str(file_request)), verify=False, headers=HEADERS).content)["status"] == "ready":
            download_file_request(name,id,file_request,format)
            break
        else:
            time.sleep(1)
=======
>>>>>>> dev

def export_request_check(name, id, file_request, format):
    while True:
        if json.loads(requests.get(NESSUS_INSTANCE + "/scans/%s/export/%s/status" % (str(id), str(file_request["file"])), verify=False, headers=HEADERS).content)["status"] == "ready":
            download_file_request(name, id, file_request, format)
            break
        else:
            time.sleep(1)

<<<<<<< HEAD
    download = requests.get(NESSUS_INSTANCE+"/tokens/%s/download" %(str(file_request)), verify=False, headers=HEADERS)

    if format == "nessus":
        with open(PATH+"/%s.nessus" %name.decode(), "wb") as handle:
            for chunk in download.iter_content(chunk_size=128):
                handle.write(chunk)
    elif format == "html":
        with open(PATH+"/%s.html" %name.decode(), "wb") as handle:
            for chunk in download.iter_content(chunk_size=128):
                handle.write(chunk)
    elif format == "csv":
        with open(PATH+"/%s.csv" %name.decode(), "wb") as handle:
            for chunk in download.iter_content(chunk_size=128):
                handle.write(chunk)
    elif format == "pdf":
        with open(PATH+"/%s.pdf" %name.decode(), "wb") as handle:
            for chunk in download.iter_content(chunk_size=128):
                handle.write(chunk)
=======

def download_file_request(name, id, file_request, format):
>>>>>>> dev

    download = requests.get(NESSUS_INSTANCE + "/scans/%s/export/%s/download" % (str(id), str(file_request["file"])), verify=False, headers=HEADERS)

    if format == "nessus":
        with open(PATH + "/%s.nessus" %name, "wb") as handle:
            for chunk in download.iter_content(chunk_size=128):
                handle.write(chunk)
    elif format == "html":
        with open(PATH + "/%s.html" % name, "wb") as handle:
            for chunk in download.iter_content(chunk_size=128):
                handle.write(chunk)
    elif format == "csv":
        with open(PATH + "/%s.csv" % name, "wb") as handle:
            for chunk in download.iter_content(chunk_size=128):
                handle.write(chunk)
    elif format == "pdf":
        with open(PATH + "/%s.pdf" % name, "wb") as handle:
            for chunk in download.iter_content(chunk_size=128):
                handle.write(chunk)

<<<<<<< HEAD
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
=======

def RetrieveFolderChoice():
    folder_list = []
    dump = json.loads(requests.get(NESSUS_INSTANCE + "/folders", verify=False, headers=HEADERS).content)["folders"]

    for folder in dump:
        if folder["type"] == "trash":
            continue
        else:
            folder_list.append(folder)

    print("=" * len("NESSUS FOLDERs"))
    print("NESSUS FOLDERS ")
    print("=" * len("NESSUS FOLDERS"))

    for folder in folder_list:
        print("ID [ %s  ] :: %s" % (folder["id"], folder["name"]))

    found = False
    while found is False:

        choice = raw_input("Choose Folder ID: ")
        for folder in folder_list:
            if str(folder["id"]) == choice:
                found = True

        if found is False:
            print("(!) Invalid Selection")
>>>>>>> dev

    print("\n")
    return choice

<<<<<<< HEAD
    global HEADERS

    HEADERS = {"X-Cookie" : "token=%s" %nessus_login(),
            "Content-Type" : "application/json"}

    if FOLDER:
        scans = retrieve_scans(RetrieveFolderChoice())
    else:
        scans = retrieve_scans()

    retrieve_export_request(scans)
    print("\n[+] Downloads Complete")
=======

def main():
    global HEADERS

    HEADERS = {"X-Cookie": "token=%s" % nessus_login(),
               "Content-Type": "application/json"}

    if FOLDER:
        scans = retrieve_scans(RetrieveFolderChoice())
    else:
        scans = retrieve_scans()
>>>>>>> dev

    retrieve_export_request(scans)
    print("\n[+] Downloads Complete")


main()
