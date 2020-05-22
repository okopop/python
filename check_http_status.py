#!/usr/bin/python
"""check http status"""
import requests
try:
    urls = ["http://www.x.se", "http://www.x.se", "http://www.x.se"]
    i = 0
    while i < len(urls):
        r = requests.head(urls[i])
        print("Status of", urls[i], ":", r.status_code)
        i += 1
except requests.ConnectionError:
    print("failed to connect")
