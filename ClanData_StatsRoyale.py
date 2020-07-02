# -*- coding: utf-8 -*-
"""
Created on Sat May 18 09:45:50 2019

@author: dmmacs
"""

import requests

link = 'https://api.clashroyale.com/v1/clans/QQG200V/members'

f = requests.get(link)
#print(f.text)

#tmpStr = f.text

out = open('tmp.txt','w', encoding='UTF-8')
out.write(f.text)
#out.write(tmpStr[30000:34999])
out.close()
