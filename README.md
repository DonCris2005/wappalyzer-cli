# wappalyzer-cli
Wappalyzer CLI tool to find Web Technologies 

# Installation :

> git clone https://github.com/gokulapap/wappalyzer-cli

> cd wappalyzer-cli

> python3 -m venv venv

> source venv/bin/activate

> pip3 install .


```
root@kali:~/tools/wappalyzer-cli# wappy -h

usage: wappy [-h] [-u URL] [-f FILE]

Finds Web Technologies !

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     url to find technologies
  -f FILE, --file FILE  list of urls to find web technologies
  -wf WRITEFILE, --writefile WRITEFILE  File to write output to

```

# Demo 
![wappy](https://user-images.githubusercontent.com/57899332/141133098-906e9ac0-b85e-453d-9e16-f48b4c14303c.gif)

## Bulk Adyen detection

Use `adyen_checker.py` to classify large lists of domains:

```bash
$ adyen_checker.py -i domains.txt --workers 8 --goods goods.txt --bads bads.txt
```
