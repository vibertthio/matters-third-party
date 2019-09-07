from bs4 import BeautifulSoup as bs
import requests
import json
import re
import datetime

# URL = "https://matters.news/@vibertthio"
URL = "https://matters.news/@Andy"

response = requests.get(URL)
text = response.text
soup = bs(text, features="lxml")
articles = []

for script in soup('script'):
    if script.get('id') == '__NEXT_DATA__':
        data = json.loads(script.contents[0])['props']['apolloState']['data']
        for key in data.keys():
            if (re.match('^Article:', key)):
                # print(data[key])
                # print('----------')
                articles.append({
                    'title': data[key]['title'],
                    'time': re.search('^([0-9,-])*', data[key]['createdAt']).group(0),
                    'dataHash': data[key]['dataHash']
                })

# for a in articles:
# 	print(a)

with open('./index.md', 'w') as file:
    file.write('''---
title: /articles
layout: home
permalink: /
---

''')

    for a in articles:
        file.write('{} [{}](https://d26g9c7mfuzstv.cloudfront.net/ipfs/{})\n\n'.format(a['time'], a['title'], a['dataHash']))
