# -*- coding: utf-8 -*-

from lib.core.scanlist import ScanList
import requests
import json
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class User(object):

    def __init__(self, instance, username=None, password=None, api_key=None):
        self.instance = instance
        self.username = username
        self.password = password
        self.api_key = api_key
        self.header = {}

        # Initialize Session
        self.RetrieveToken()
        print("[+] Ness-Query Generating Data")
        self.scan_list_instance = ScanList(self.instance, self.header)

    def RetrieveToken(self):

        if self.username and self.password:
            response = requests.post(self.instance+"/session", verify=False, timeout=10,data={"username":self.username, "password":self.password})
            if response.status_code == 200:
                print("[+] Authentication Successful")
                self.header["X-Cookie"] = "token="+json.loads(response.text)["token"]
            else:
                print("(!) Incorrect Credentials")
                sys.exit()
        elif self.api_key:
            pass
        else:
            print("(!) Something went wrong")
            sys.exit()

    def CheckTokenValidity(self):

        response = json.loads(requests.get(self.instance+"/session", verify=False, headers=self.header).content)
        if "error" in response.keys():
            return False

        return True
