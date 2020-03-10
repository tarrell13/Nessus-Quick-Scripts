# -*- coding: utf-8 -*-

from lib.core.vuln import Vulnerability
import requests
import urllib3
import json

urllib3.disable_warnings()

class Host(object):

    def __init__(self, host, id, instance, headers):
        self.instance = instance
        self.headers = headers
        self.scan_id = id

        self.host_id = host["host_id"]
        self.host_index = host["host_index"]
        self.hostname = host["hostname"]
        self.progress = host["progress"]
        self.critical = host["critical"]
        self.high = host["high"]
        self.medium = host["medium"]
        self.low = host["low"]
        self.info = host["info"]
        self.totalchecksconsidered =  host["totalchecksconsidered"]
        self.numchecksconsidered = host["numchecksconsidered"]
        self.scanprogresstotal = host["scanprogresstotal"]
        self.scanprogresscurrent = host["scanprogresscurrent"]
        self.score = host["score"]

        self.vulnerabilities = []
        self.RetrieveVulnerabilites()

    def RetrieveVulnerabilites(self):

        response = requests.get(self.instance+"/scans/%s/hosts/%s" %(str(self.scan_id),str(self.host_id)),verify=False,headers=self.headers)

        if response.status_code == 200:
            for vuln in json.loads(response.text)["vulnerabilities"]:
                self.vulnerabilities.append(Vulnerability(vuln))
        else:
            print("(!) Something went wrong")

        return
