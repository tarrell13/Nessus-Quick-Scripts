# -*- coding: utf-8 -*-

from .lib.core.hosts import Host
import requests
import json

class Scan(object):

    def __init__(self, scan, instance, headers):
        self.headers = headers
        self.instance = instance
        self.scan_data = None

        self.id = scan["id"]
        self.uuid = scan["uuid"]
        self.name = scan["name"]
        self.type = scan["type"]
        self.owner = scan["owner"]
        self.enabled = scan["enabled"]
        self.folder_id = scan["folder_id"]
        self.read = scan["read"]
        self.status = scan["status"]
        self.shared = scan["shared"]
        self.user_permissions = scan["user_permissions"]
        self.creation_date = scan["creation_date"]
        self.last_modification_date = scan["last_modification_date"]
        self.control = scan["control"]
        self.starttime = scan["starttime"]
        self.timezone = scan["timezone"]
        self.rrules = scan["rrules"]

        self.hosts = []

        self.RetrieveScanData()



    def RetrieveScanData(self):

        response = requests.get(self.instance+"/scans/%s" %str(self.id), verify=False, headers=self.headers)

        if response.status_code == 200:
            self.scan_data = json.loads(response.text)
        else:
            print("(!) Something went wrong")

        self.RetrieveHostIds()
        return

    def RetrieveHostIds(self):

        for host in self.scan_data["hosts"]:
            self.hosts.append(Host(host, self.id, self.instance, self.headers))

        return