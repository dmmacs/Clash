#! /home/dmmacs/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""ClanHistory"""
from _version import __version__
import glob
import datetime
import json
import ClanCommon
import sys
import operator
import os
import myTimer
import requests


class warData:
    def __init__(self, warId, rank, warData):
        self.warId = warId
        self.warData = warData
        self.rank = rank
        
        #20190520T151400.000Z
        year = int(warId[0:4])
        month = int(warId[4:6])
        day = int(warId[6:8])
        hour = int(warId[9:11])
        minute = int(warId[11:13])
        seconds = int(warId[13:15])
        self.warDate = datetime.datetime(year, month, day, hour, minute, seconds, tzinfo=ClanCommon.UTC_TZ)
        
    def __str__(self):
        return ('warId:' + self.warId + ' warData:' + json.dumps(self.warData, indent=4))


def processClanWar(clan_tag, clan_data):

    ClanCommon.init()
    
    record_folder = 'record' + ClanCommon.DirSlash()
    record_folder = clan_tag + ClanCommon.DirSlash() + 'record' + ClanCommon.DirSlash()
    print('\nProcess Clan War History for Clan Tag {} in {}'.format(clan_tag, record_folder))



    clan_war = []
    fNames = []
    currentWarFname = ''

    file_filter = record_folder + '*' + '*.txt'
    files = glob.glob(file_filter)
    
    for file in files:
        if file.find('warlog') > -1:
            idx1 = file.rfind('-') + 1
            idx2 = file.rfind('.')
            fTime = ClanCommon.getFileNameDate(file[idx1:idx2])
#            if fTime.weekday() == ClanCommon.FRI:
            fNames.append(ClanCommon.myFnames(file,fTime))
            
        if file.find('currentwar') > -1:
            idx1 = file.rfind('-') + 1
            idx2 = file.rfind('.')
            idx3 = currentWarFname.rfind('-') + 1
            idx4 = currentWarFname.rfind('.')
            if currentWarFname == '':
                currentWarFname = file
            elif ClanCommon.getFileNameDate(file[idx1:idx2]) > ClanCommon.getFileNameDate(currentWarFname[idx3:idx4]):
                currentWarFname = file
                currentWarTime = ClanCommon.getFileNameDate(currentWarFname[idx3:idx4])

    fin = open(currentWarFname, 'r')
    currentWar = json.load(fin)
    fin.close()



    CwParticipants = currentWar['participants']
    if currentWar['state'] == 'warDay':
        CwParticipants .sort(key=lambda k: (k['wins'],k['cardsEarned']), reverse=True)
    else:
        CwParticipants .sort(key=lambda k: (k['cardsEarned']), reverse=True)

    fNames.sort(key=operator.attrgetter('fDate'))
    

    for fName in fNames:
        fin = open(fName.fName , 'r')
        clan_war.append(json.load(fin))
        fin.close()


    wars = []
    
    for i, data in  enumerate(clan_war):
#        print('File = ' + fNames[i].fName)
        for item in data['items']:
            found = False
            for war in wars:
                if war.warId == item['createdDate']:
                    found = True
                    break;
            if found is False:
#                print("This is the current War: " + item['createdDate'] + ', ' + fNames[i].fName)
##                if item['createdDate'] == '20190520T151400.000Z':
#                print("Got Here: " + item['createdDate'] + ', ' + fNames[i].fName)
#                try:
#                    print(item['createdDate'],item['participants'][0]['numberofBattles'])
                wars.append(warData(item['createdDate'], 0, item))
#                except KeyError:
#                    print('Missing numberof Battles')

#    for data in clan_war:
    wars.sort(key=operator.attrgetter('warDate'), reverse=True)
    for war in wars:
#        print(war.warId)
        for i,clan in enumerate(war.warData['standings']):
            #print(clan['clan']['tag'])
            if clan['clan']['tag'] == '#' + clan_tag:
#                print(clan['clan']['participants'],clan['clan']['battlesPlayed'], clan['clan']['wins'], clan['clan']['crowns'],clan['trophyChange'])
                clan_name = clan['clan']['name']
                clan_score = clan['clan']['clanScore']
                war.rank = i
#        print(war.warData['standings'])

#    print()

    clan_badge = 'https://statsroyale.com/images/clanwars/'
    clan_badge += str(clan_data['badgeId'])
    
    if clan_data['clanWarTrophies'] < 600:
        clan_badge += '_bronze3'
    elif clan_data['clanWarTrophies'] < 1500:
        clan_badge += '_silver3'
    elif clan_data['clanWarTrophies'] < 3000:
        clan_badge += '_gold3'
    else:
        clan_badge += '_magical'
    clan_badge += '.png'

    htmlout = ClanCommon.buildhtmlHeader(clan_name)
    # Add Clan Data
    htmlout += '<div style="width:100%;">\n' 
    htmlout += '<div style="float: left; width:50%;">'
    htmlout += '<img style="float:left;margin-bottom:20px;" src="'
    htmlout += clan_badge
    htmlout += '" height="100px" width="72px">\n'
    
    htmlout += '<div style="font-weight:bold;font-size:35px;margin-left:77px;line-height:60px">'
    htmlout +=  clan_name
    htmlout += '</div>\n'
    htmlout += '<div style="font-size:14px;margin-left=77px">'
    htmlout += clan_name
    htmlout += '</div>\n'
    htmlout += '</div>\n'

    htmlout += '<div style="float: left; width:50%;">'
    htmlout += '<img  style="float:left" src="../img/War_Shield.png" height="100px" width="86px">'
    htmlout += '<div style="font-weight:bold;line-height:20px;font-size:15px">Current War Status: '
    htmlout += 'War State '#clan_current_war['state']
    htmlout += '</div>'
    htmlout += '<div style="line-height:20px;font-size:15px">'
#    if clan_current_war['state'] == 'warDay':
#        warEndTime = processClashDate(clan_current_war['warEndTime'])
#        htmlout += 'War Ends:'
#        htmlout += warEndTime.astimezone(tz=ClanCommon.Eastern_TZ).strftime('%I:%M:%S %p %Z %d-%b-%Y')
#        htmlout += ' </div></div>'
#    elif clan_current_war['state'] == 'collectionDay':
#        warEndTime = processClashDate(clan_current_war['collectionEndTime'])
#        htmlout += 'Collection Ends:'
#        htmlout += warEndTime.astimezone(tz=ClanCommon.Eastern_TZ).strftime('%I:%M:%S %p %Z %d-%b-%Y')
    htmlout += ' </div></div>'
    
    
    htmlout += '</div>\n'
    htmlout += '</div>\n'
    
    htmlout += '<div style="clear:both"></div>\n'    
    htmlout += '<div style="width:100%;">\n' 
    
    # Left Section for Clan Trophies
    htmlout += '<div style="float: left; width:33%;">\n'
    htmlout += '<img style="float:left;margin-bottom:20px;text-align:center;" src="https://cdn.statsroyale.com/images/trophy.png" height="51px" width="51px">\n'
    htmlout += '<div style="font-weight:bold;line-height:20px;font-size:15px">'
    htmlout += str(clan_data['clanScore'])
    htmlout += '</div>\n'
    htmlout += '<div style="line-height:20px;font-size:15px">Trophies</div>'
    htmlout += '</div>\n' #End Left Section Div

    # Middle Section for Clan War Trophies
    htmlout += '<div style="float: left; width:33%;">\n'
    htmlout += '<img  style="float:left" src="https://cdn.statsroyale.com/images/clan-trophies.png" height="51px" width="51px">\n'
    htmlout += '<div style="font-weight:bold;line-height:20px;font-size:15px">'
    htmlout += str(clan_score)
    htmlout += '</div>\n'
    htmlout += '<div style="line-height:20px;font-size:15px">Trophies</div>'

    htmlout += '</div>\n' # End Middle Section Div
    
    #Right Secton (nothing in there yet)
    htmlout += '<div style="float: left; width:33%;"></div>\n'
    htmlout += '<img style="float:left;margin-bottom:20px;text-align:center;" src="https://cdn.statsroyale.com/images/cards.png" height="51px" width="51px">\n'
    htmlout += '<div style="font-weight:bold;line-height:20px;font-size:15px">'
    htmlout += str(clan_data['donationsPerWeek'])
    htmlout += '</div>\n'
    htmlout += '<div style="line-height:20px;font-size:15px">Donations/week</div>'    
    
    htmlout += '</div>\n' # End Clan Information Section Div
    htmlout += '</div>\n'
    
    htmlout += '<div style="clear:both;"></div>\n'
        
    
    
    #Build Table
    #Add Table Headings
    htmlout += '<div class="container_12">\n'
    htmlout += '<table class="sortable" cellpadding="0" cellspacing="0"  width=90%>\n'
    htmlout += "<thead>\n"
#    for war in wars:
    htmlout += ClanCommon.createTH('Start date', '')
    htmlout += ClanCommon.createTH('Rank', '')
    htmlout += ClanCommon.createTH('Participants', '')
    htmlout += ClanCommon.createTH('Battles Played', '')
    htmlout += ClanCommon.createTH('Wins', '')
    htmlout += ClanCommon.createTH('Crowns', '')
    htmlout += ClanCommon.createTH('Trophy Change', '')
    htmlout += ClanCommon.createTH('War Trophies', '')
#        htmlout += ClanCommon.createTH(war.warDate.strftime('%d-%b-%Y'),'')
    htmlout += '</thead>\n'
    
    htmlout += '<tbody>\n'

#    if currentWar['state'] == 'warDay':
#        print('War End Time: ' + currentWar['warEndTime'])
#    else:
#        print('Collection End Time: ' + currentWar['collectionEndTime'])

    htmlout += '<tr>'
    if currentWar['state'] == 'warDay':
        tmpStr = '<a href="#' + currentWar['warEndTime'] + '">' + currentWarTime.strftime('%d-%b-%Y') + '</a>'
    else:
        tmpStr = '<a href="#' + currentWar['collectionEndTime'] + '">' + currentWarTime.strftime('%d-%b-%Y') + '</a>'
    
    clan_rank = 0
    for i, clan in enumerate(currentWar['clans']):
        if clan['tag'] == '#'+ clan_tag:
            clan_rank = i

    htmlout += ClanCommon.createTD(tmpStr,'','')
    htmlout += ClanCommon.createTD(str(clan_rank),'','center')
    htmlout += ClanCommon.createTD(str(currentWar['clan']['participants']),'', 'center')
    htmlout += ClanCommon.createTD(str(currentWar['clan']['battlesPlayed']),'', 'center')
    htmlout += ClanCommon.createTD(str(currentWar['clan']['wins']),'', 'center')
    htmlout += ClanCommon.createTD(str(currentWar['clan']['crowns']),'', 'center')
    htmlout += ClanCommon.createTD('N/A','', 'center')
    htmlout += ClanCommon.createTD(str(currentWar['clan']['clanScore']),'', 'center')
    

#    htmlout += ClanCommon.createTD(str(war.warData['standings'][war.rank]['trophyChange']), '', 'center')
#    htmlout += ClanCommon.createTD(str(war.warData['standings'][war.rank]['clan']['clanScore']), '', 'center')
    htmlout += '</tr>\n'

    for war in wars:
        htmlout += '<tr>'
        tmpStr = '<a href="#' + war.warId + '">' + war.warDate.strftime('%d-%b-%Y') + '</a>'
        htmlout += ClanCommon.createTD(tmpStr,'','')
        htmlout += ClanCommon.createTD(str(war.rank),'','center')
        htmlout += ClanCommon.createTD(str(war.warData['standings'][war.rank]['clan']['participants']), '', 'center')
        htmlout += ClanCommon.createTD(str(war.warData['standings'][war.rank]['clan']['battlesPlayed']), '', 'center')
        htmlout += ClanCommon.createTD(str(war.warData['standings'][war.rank]['clan']['wins']), '', 'center')
        htmlout += ClanCommon.createTD(str(war.warData['standings'][war.rank]['clan']['crowns']), '', 'center')
        htmlout += ClanCommon.createTD(str(war.warData['standings'][war.rank]['trophyChange']), '', 'center')
        htmlout += ClanCommon.createTD(str(war.warData['standings'][war.rank]['clan']['clanScore']), '', 'center')
        htmlout += '</tr>\n'

    htmlout += '</tbody>\n'
    htmlout += '</table>\n'
    htmlout += '</div>\n'
    htmlout += '</div>\n'

    #Add Current War Details Here.
    if currentWar['state'] == 'warDay':
        htmlout += '<div style="clear:both;"><a name="' + currentWar['warEndTime'] + '"></a><p>' + 'Curent War: ' + currentWarTime.strftime('%d-%b-%Y') + '</p></div>\n'
    else:
        htmlout += '<div style="clear:both;"><a name="' + currentWar['collectionEndTime'] + '"></a><p>' + 'Curent War: ' + currentWarTime.strftime('%d-%b-%Y') + '</p></div>\n'
        

    if currentWar['state'] == 'warDay':
        htmlout += '<div class="container_12" name="' + currentWar['warEndTime'] + '">\n'
    else:
        htmlout += '<div class="container_12" name="' + currentWar['collectionEndTime'] + '">\n'
        
    htmlout += '<table class="sortable" cellpadding="0" cellspacing="0"  width=90%>\n'
    htmlout += "<thead>\n"
    htmlout += ClanCommon.createTH('Participants', '')
    htmlout += ClanCommon.createTH('Collection Battles', '')
    htmlout += ClanCommon.createTH('Cards Earned', '')
    htmlout += ClanCommon.createTH('Battles Played', '')
    htmlout += ClanCommon.createTH('Wins', '')
    htmlout += ClanCommon.createTH('Num Battles', '')
    htmlout += '</thead>\n'

    htmlout += '<tbody>\n'
    for person in CwParticipants:
        htmlout += '<tr>'
        htmlout += ClanCommon.createTD(person['name'],'','')
        htmlout += ClanCommon.createTD(str(person['collectionDayBattlesPlayed']),'','center')
        htmlout += ClanCommon.createTD(str(person['cardsEarned']),'','center')
        if person['battlesPlayed'] == 0:
            css = 'yelbkd'
        else:
            css = ''
        htmlout += ClanCommon.createTD(str(person['battlesPlayed']),css,'center')
        htmlout += ClanCommon.createTD(str(person['wins']),'','center')
        try:
            htmlout += ClanCommon.createTD(str(person['numberOfBattles']),'','center')
        except KeyError:
            htmlout += ClanCommon.createTD('1','','center')
        
        htmlout += '</tr>\n'

    htmlout += '</tbody>\n'
    htmlout += '</table>\n'
    htmlout += '</div>\n'
    htmlout += '</div>\n'

    for war in wars:
#        print(war.warId)
#    war = wars[0]
    
        # Add Division for first War Table
        htmlout += '<div style="clear:both;"><a name="' + war.warId + '"></a><p>' + 'Past War: ' + war.warDate.strftime('%d-%b-%Y') + '</p></div>\n'
        htmlout += '<div class="container_12" name="' + war.warId + '">\n'
        htmlout += '<table class="sortable" cellpadding="0" cellspacing="0"  width=90%>\n'
        htmlout += "<thead>\n"
        htmlout += ClanCommon.createTH('Participants', '')
        htmlout += ClanCommon.createTH('Collection Battles', '')
        htmlout += ClanCommon.createTH('Cards Earned', '')
        htmlout += ClanCommon.createTH('Battles Played', '')
        htmlout += ClanCommon.createTH('Wins', '')
        htmlout += ClanCommon.createTH('Num Battles', '')
        htmlout += '</thead>\n'
        
        htmlout += '<tbody>\n'
        Participants =  war.warData['participants']
        Participants .sort(key=lambda k: (k['wins'],k['cardsEarned']), reverse=True)
        
        for person in Participants:
#            print(person)
            htmlout += '<tr>'
            htmlout += ClanCommon.createTD(person['name'],'','')
            htmlout += ClanCommon.createTD(str(person['collectionDayBattlesPlayed']),'','center')
            htmlout += ClanCommon.createTD(str(person['cardsEarned']),'','center')
            if person['battlesPlayed'] == 0:
                css = 'redbkd'
            else:
                css = ''
            htmlout += ClanCommon.createTD(str(person['battlesPlayed']),css,'center')
            htmlout += ClanCommon.createTD(str(person['wins']),'','center')
            try:
                htmlout += ClanCommon.createTD(str(person['numberOfBattles']),'','center')
            except KeyError:
                htmlout += ClanCommon.createTD('1','','center')
            
            htmlout += '</tr>\n'
        
        # Add Table for participants
        
        htmlout += '</tbody>\n'
        htmlout += '</table>\n'
        htmlout += '</div>\n'
        htmlout += '</div>\n'

    
    htmlout += '<div align=\"right\">\n'
    htmlout += '<p style=\"font-size:10px;right:auto\"> Last Updated: '

    htmlout += datetime.datetime.now().astimezone(tz=ClanCommon.Eastern_TZ).strftime('%d-%b-%Y %I:%M:%S %p %Z')
    htmlout += ' with Version: ' + __version__
    htmlout += '</p>\n'

    htmlout += '</div>\n'
        
    htmlout += ClanCommon.buildhtmlFooter()
    
    
    htmlFname = clan_tag + ClanCommon.DirSlash() + 'war' + '.html'
    out = open(htmlFname, 'w', encoding='UTF-8')
    out.write(htmlout)
    out.close()


# Start of main
if __name__ == '__main__':

    myTimer.start()

    clan_tag = 'QQG200V'
    apiFname = 'api_key.txt'

    fname = os.path.dirname(__file__)
    fname = os.path.dirname(os.path.abspath(__file__))
    fname += ClanCommon.DirSlash()

    fname += apiFname
    fin = open(fname, 'r')
    key = fin.readline().strip()
    fin.close()


    reqHeaders = {"Accept":"application/json", "authorization":"Bearer " + key}
    link_clan = 'https://api.clashroyale.com/v1/clans/%23' + clan_tag #QQG200V'
    print('Getting Clan Data')
    req = requests.get(link_clan, headers=reqHeaders, timeout=2)
    clan_data = req.json()
    req.close()
    if (req.status_code != 200):
        print('Could not read Clan Data Api, Response Code {}'.format(req.status_code))
        sys.exit(-1)
    print('\tClan Data for ' + clan_data['name'])

#    print(json.dumps(clan_data, indent=4))
    processClanWar(clan_tag, clan_data)

    myTimer.end()
    print('Completed Clan War in {}'.format(myTimer.elapsedTime()))
    

