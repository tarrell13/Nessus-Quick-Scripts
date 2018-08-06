# Synopsis:

This script export all Nessus Scan reports in the following formats: CSV, HTML, PDF and NESSUS

# Usage:

```
[user@nessusbox]$ python ness-exporter.py -h
usage: ness-exporter.py [-h] [-n NESSUS] [-p PATH]

Script will download all scans in every format

optional arguments:
  -h, --help            show this help message and exit
  -n NESSUS, --nessus NESSUS
                        Points Script to Nessus Instance
  -p PATH, --path PATH  Path to save downloaded files

```
### Scan reports have been downloaded to the Downloads directory

```
[user@nessusbox]$ python ness-exporter.py -n https://localhost:8834 -p ~/Downloads
[*] Log into Nessus Instance => https://localhost:8834
======================================================
[*] Username: user
[*] Password: 
[+] Authentication Successful
[*] Save Directory: /home/user/Downloads
[*] Downloading Files....
[============================================================] 100.0% ...
[+] Downloads Complete

```






