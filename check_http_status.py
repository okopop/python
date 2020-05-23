#!/usr/bin/python
"""check http status"""
import requests
try:
    URLS = ["http://www.x.se", "http://www.x.se", "http://www.x.se"]
    i = 0
    while i < len(URLS):
        R = requests.head(URLS[i])
        print("Status of", URLS[i], ":", R.status_code)
        i += 1
except requests.ConnectionError:
    print("failed to connect")
