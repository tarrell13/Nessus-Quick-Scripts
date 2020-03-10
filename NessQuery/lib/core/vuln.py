# -*- coding: utf-8 -*-

class Vulnerability(object):

    def __init__(self, vuln):
        self.host_id = vuln["host_id"]
        self.plugin_id = vuln["plugin_id"]
        self.plugin_name = vuln["plugin_name"]
        self.plugin_family = vuln["plugin_family"]
        self.count = vuln["count"]
        self.vuln_index = vuln["vuln_index"]
        self.severity_index = vuln["severity_index"]
        self.severity = vuln["severity"]

