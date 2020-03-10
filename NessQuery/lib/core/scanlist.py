# -*- coding: utf-8 -*-

from .scan import Scan
from  threading import Thread
import requests
import json

# Global Scan for Threads
scans = []

class ScanList(object):

    def __init__(self, instance, headers):

        self.scan_list = []
        self.scan_id_name = {}
        self.scan_data = []

        self.headers = headers
        self.instance = instance

        self.RetrieveScanList()
        self.scans = scans

    def RetrieveScanList(self):

        response = requests.get(self.instance+"/scans",verify=False, headers=self.headers)

        if response.status_code == 200:
            for scan in json.loads(response.text)["scans"]:
                self.scan_list.append(scan)
        else:
            print("(!) Something went wrong")

        self.RetrieveScanIDs()

    def RetrieveScanIDs(self):

        for scan in self.scan_list:
            self.scan_id_name[scan["id"]] = scan["name"]

        threads = [None] * len(self.scan_list)

        # Start Threads Per Scan
        for i in range(len(threads)):
            threads[i] = Thread(target=self.CreateScans,args=(self.scan_list,i))
            threads[i].start()

        for i in range(len(threads)):
            threads[i].join()

        return

    def CreateScans(self,scan_list, index):

        global scans
        scans.append(Scan(scan_list[index],self.instance,self.headers))

        return

