# -*- coding: utf-8 -*-

class Colors:

    header = '\033[95m'
    informational = '\033[94m'
    success = '\033[92m'
    warning = '\033[93m'
    red  = '\033[91m'
    end_color = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    yellow = '\033[33m'

class Output(object):

    def __init__(self):
        pass

    def TerminalOutput(self, data, type=None):

        if type == "c":
            for name,value in data.items():
                print(Colors.red+"[+] %s "%(name)+Colors.end_color+"[ Plugin ID: %s ] :: [ Host Count %d ]" %(value["plugin_id"],len(value["hosts"])))

        if type == "h":
            for name,value in data.items():
                print(Colors.warning+"[+] %s "%(name)+Colors.end_color+"[ Plugin ID: %s ] :: [ Host Count %d ]" %(value["plugin_id"],len(value["hosts"])))

        if type == "m":
            for name,value in data.items():
                print(Colors.yellow+"[+] %s "%(name)+Colors.end_color+"[ Plugin ID: %s ] :: [ Host Count %d ]" %(value["plugin_id"],len(value["hosts"])))

        if type == "l":
            for name,value in data.items():
                print(Colors.success+"[+] %s "%(name)+Colors.end_color+"[ Plugin ID: %s ] :: [ Host Count %d ]" %(value["plugin_id"],len(value["hosts"])))

        if type == "i":
            for name,value in data.items():
                print(Colors.informational+"[+] %s "%(name)+Colors.end_color+"[ Plugin ID: %s ] :: [ Host Count %d ]" %(value["plugin_id"],len(value["hosts"])))

        return

