#!/usr/bin/env python3

import requests
from time import sleep

url = 'http://www.az'
name = "demo"

def check_url_status(url):
    req = requests.get(url)
    return req.status_code

def name_reverser(name):
    print(name[::-1])
    #sleep(2)
    return name[::-1]

def summ(a, b):
    return a + b


# run if run directly
if __name__ == '__main__':
    print(check_url_status(url))
    name_reverser(name)

