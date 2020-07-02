#!! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 16:45:33 2019

@author: dmmacs
"""


from _version import __version__
import platform
import datetime
import json
import ClanCommon
import myTimer
import pytz



def processKickData(clan_data, warData):
    #Looking for people that have missed 2 consecutive wars or not been on in 1 month
    
    current = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    for i, person in enumerate(clan_data['memberList']):
        lastSeen = ClanCommon.processClashDate(person['lastSeen'])
        #print(person)
#        print(person['name'],lastSeen, current - lastSeen)
        #print(person['name'],current - lastSeen)
        elapsedtime = current - lastSeen
        elapsedtime = elapsedtime.total_seconds() / 3600 / 24
        
#        playerData = ClanCommon.getAPIData(person['tag'], 'battlelog')
        
        #print(json.dumps(playerData.json(), indent=4))
        
#        out = open('tmp.txt', 'w', encoding='UTF-8')
#        out.write(json.dumps(playerData.json(), indent=4))
#        out.close()        
        
        if elapsedtime > 30 and person['name'] != 'Mooseknuckle':
            print(person['name'], current - lastSeen, elapsedtime)
        
        found = False
        warcnt = 0
        missedBattleCnt = 0
        missedBattles = []
        for j, war in enumerate(warData['items']):
            
            for participant in war['participants']:
                if person['name'] == participant['name']:
                    if int(participant['battlesPlayed']) == 0:
                        missedBattleCnt += 1
                        missedBattles.append(j)
                    found = True
            if found == False and j < 2:
                warcnt += 1
        if warcnt > 0 and person['name'] != 'Mooseknuckle':
            print('{} missed last {} wars and missed {} Battles, {}'.format(person['name'], warcnt, missedBattleCnt, missedBattles))
#            if j == 1:
#                break;
#        if i == 0:
#            break



# Start of main
if __name__ == '__main__':

#    modInit()    
    myTimer.start()
    print('Python Version is: ' + platform.python_version())
    print('Script Version is: ' + __version__)
    
    ClanCommon.init()
    req = ClanCommon.getAPIData('QQG200V', 'ClanData')
    clan_data = req.json()
    
    req = ClanCommon.getAPIData('QQG200V', 'WarLog')
    warData = req.json()
    
    
#    processDailyHistory('QQG200V', clan_data)
#    processWeeklyHistory('QQG200V', clan_data)
    processKickData(clan_data, warData)
#    print(json.dumps(clan_data, indent=4))
    
    myTimer.end()
    print('Completed Clan Kick in {}'.format(myTimer.elapsedTime()))

