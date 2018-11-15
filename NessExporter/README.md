# Synopsis:

This script export all Nessus Scan reports in the following formats: CSV, HTML, PDF and NESSUS

# Usage:

```
python ness-exporter.py -h
usage: ness-exporter.py [-h] [-n NESSUS] [-p PATH]

Script will download all scans in every format

optional arguments:
  -h, --help            show this help message and exit
  -n NESSUS, --nessus NESSUS
                        Points Script to Nessus Instance
  -p PATH, --path PATH  Path to save downloaded files
  -f FORMATS, --formats FORMATS
                        Specify format, nessus, pdf, html, csv, default is all

  Note: You are only able to download in PDF format if your system has Java installed
```
### Scan reports have been downloaded to the Downloads directory. In two (2) different formats.

```
python ness-exporter.py -n https://localhost:8834 -p ~/Downloads/ -f nessus,html
[*] Log into Nessus Instance => https://localhost:8834
=========================================================
[*] Username: user
[*] Password: 
[+] Authentication Successful
[*] Save Directory: /root/Downloads/
[*] Formats => ['nessus', 'html']
[*] Downloading Files....
[============================================================] 100.0% ...
[+] Downloads Complete

```






