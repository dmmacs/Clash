# -*- coding: utf-8 -*-
"""
Created on Sat May 18 10:07:23 2019

@author: dmmacs
"""

import subprocess
import time 
import requests

link = 'https://api.clashroyale.com/v1/clans/QQG200V/members'
link = 'http://myexternalip.com/raw'

f = requests.get(link)


cmd = 'cmd.exe' #, "/C", "start /B", "powercfg", "-requests

#result = subprocess.run([cmd, '/C','powercfg','-requests'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

cmd = 'cmd.exe'

result = subprocess.run([cmd, '/C','ipconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


#print(result.stderr.decode())
#print(result.stdout.decode())

tmpStr = result.stdout.decode()
print(tmpStr)
idx = tmpStr.find('IPv4 Address')

lines = tmpStr.split('\n')

for line in lines:
    idx = line.find('IPv4 Address')
    if idx >= 0:
        vals = line.split(':')
        ipAddr = vals[1].strip()
        print(ipAddr)
        break

out = open('ipAddr.txt', 'a')
timeStr = time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime(time.time()))
out.write('{} | {} | {}\n'.format(timeStr, ipAddr, f.text))
out.close()
    
print(f.text)

f.close()
