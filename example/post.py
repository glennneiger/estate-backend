#! /usr/bin/env python3 

import requests as r

response = r.post('http://127.0.0.1:5000', data="")
print(response.headers)
print(response.text)
