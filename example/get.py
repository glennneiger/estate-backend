#! /usr/bin/env python3 

import requests as r

response = r.get('http://127.0.0.1:5000')
print(response.text)
