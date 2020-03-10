#!/usr/bin/env python3

from lib.core.user import User
from lib.core.output import Output
import sys
import getpass

def ParseData(user):
    # Severity Classification
    # 0 - Informational
    # 1 - Low
    # 2 - Medium
    # 3 - High
    # 4 - Critical

    data = {
        "c": {},
        "h": {},
        "m": {},
        "l": {},
        "i": {}
    }

    for scan in user.scan_list_instance.scans:
        for host in scan.hosts:
            for vuln in host.vulnerabilities:
                if vuln.severity == 0:
                    if vuln.plugin_name in data["i"]:
                        data["i"][vuln.plugin_name]["hosts"].append(host.hostname)
                    else:
                        data["i"][vuln.plugin_name] = {}
                        data["i"][vuln.plugin_name]["hosts"] = []
                        data["i"][vuln.plugin_name]["plugin_id"] = vuln.plugin_id
                        data["i"][vuln.plugin_name]["hosts"].append(host.hostname)

                elif vuln.severity == 1:
                    if vuln.plugin_name in data["l"]:
                        data["l"][vuln.plugin_name]["hosts"].append(host.hostname)
                    else:
                        data["l"][vuln.plugin_name] = {}
                        data["l"][vuln.plugin_name]["hosts"] = []
                        data["l"][vuln.plugin_name]["plugin_id"] = vuln.plugin_id
                        data["l"][vuln.plugin_name]["hosts"].append(host.hostname)

                elif vuln.severity == 2:
                    if vuln.plugin_name in data["m"]:
                        data["m"][vuln.plugin_name]["hosts"].append(host.hostname)
                    else:
                        data["m"][vuln.plugin_name] = {}
                        data["m"][vuln.plugin_name]["hosts"] = []
                        data["m"][vuln.plugin_name]["plugin_id"] = vuln.plugin_id
                        data["m"][vuln.plugin_name]["hosts"].append(host.hostname)

                elif vuln.severity == 3:
                    if vuln.plugin_name in data["h"]:
                        data["h"][vuln.plugin_name]["hosts"].append(host.hostname)
                    else:
                        data["h"][vuln.plugin_name] = {}
                        data["h"][vuln.plugin_name]["hosts"] = []
                        data["h"][vuln.plugin_name]["plugin_id"] = vuln.plugin_id
                        data["h"][vuln.plugin_name]["hosts"].append(host.hostname)

                elif vuln.severity == 4:
                    if vuln.plugin_name in data["c"]:
                        data["c"][vuln.plugin_name]["hosts"].append(host.hostname)
                    else:
                        data["c"][vuln.plugin_name] = {}
                        data["c"][vuln.plugin_name]["hosts"] = []
                        data["c"][vuln.plugin_name]["plugin_id"] = vuln.plugin_id
                        data["c"][vuln.plugin_name]["hosts"].append(host.hostname)
    return data

def CheckPluginID(data,id):

    for name,value in data.items():
        if int(id) == int(value["plugin_id"]):
            return True
        else:
            continue

    return False


def RetrievePluginIDList(data,id):

    print("==========")
    print("HOST LIST")
    print("==========")

    for name, value in data.items():
        if int(id) == int(value["plugin_id"]):
            for host in value["hosts"]:
                print(host)

def usage():
    print("Usage: ./ness-query <nessus_instance>")
    print("       ./ness-query https://localhost:8834")
    sys.exit()


def main():

    if len(sys.argv) < 2:
        usage()

    instance = sys.argv[1]
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    user = User(instance, username=username,password=password)
    data = ParseData(user)
    output = Output()

    while True:
        choice = input("\n[c]ritical :: [h]igh :: [m]edium :: [l]ow :: [i]nfo => ")
        if choice.lower() in ["c","h","m","l","i"]:
            severity = choice.lower()
            output.TerminalOutput(data[severity], type=severity)
            choice = input("Enter Plugin ID or 'b' to go back: ")
            if choice.lower() == "b":
                continue
            elif bool(type(int(choice)) is int) and CheckPluginID(data[severity],choice):
                RetrievePluginIDList(data[severity],choice)
            else:
                print("(!) Invalid Option or Plugin ID")
        else:
            print("(!) Invalid Option")


main()