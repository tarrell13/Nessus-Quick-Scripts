# Synopsis:

This script will take an input list of IP addresses and create scans based on these addresses. Can be helpful when you have a long list of addresses and you would like to chunk them up into groups per scan. 

# Usage:

```
┌─[user@nessusbox]─[~/Nessus-Quick-Scripts/NessCraft]
└──╼ $python ness-craft.py -h
usage: python ness-craft.py -n https://localhost:8834 -i ipList.txt -c 5

Script will create Nessus Scans using specified input file

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Increase Output Verbosity
  -c CHUNKS, --chunks CHUNKS
                        Creates scans in specified chunks
  -n NESSUS, --nessus NESSUS
                        Points script to specified Nessus Instance
  -i INPUT_FILE, --input-file INPUT_FILE
                        Input File containing IP addresses/Hostnames to create
                        scans from

```
### In the codeblock below, we have an IP list 'tmp.txt' that has a total of 25 IP addresses.

```
┌─[user@nessusbox]─[~/Nessus-Quick-Scripts/NessCraft]
└──╼ $cat tmp.txt ; wc -l tmp.txt
192.168.0.0
192.168.0.1
192.168.0.2
192.168.0.3
192.168.0.4
...(snip)
      25 tmp.txt
```

### We want to create nessus scans with these addresses using 5 different groups. Currently our nessus instance is blank but it doesn't need to blank for the script to create the scans. It will first query nessus to see how many scans you have and then increment the scan count as it creates.
```
python ness-craft.py -n https://localhost:8834 -i tmp.txt -c 5

┌─[user@nessusbox]─[~/Nessus-Quick-Scripts/NessCraft]
└──╼ $python ness-craft.py -n https://192.168.1.8:8834 -i tmp.txt -c 5 -v
[*] Log into Nessus Instance => https://192.168.1.8:8834
========================================================
[*] Username: user
[*] Password:
[+] Authentication Successful
[+] Scan - 1 Created
[+] Scan - 2 Created
[+] Scan - 3 Created
[+] Scan - 4 Created
[+] Scan - 5 Created
[+] Total Scans Created: 5
```
### Our nessus instance now has 5 scans created using those IP addresses. 

- If you do not specify a chunk group, then it will create only 1 scan using all the addresses. 
- If the chunk group specified is more than the file contains, then all addresses will be added to one scan as well. 
 
<insert-picture>




