#! /home/dmmacs/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 19 17:10:54 2019

@author: dmmacs
"""
from _version import __version__
import glob
import platform
import datetime
import json
import ClanCommon
#import sys

import myTimer

def DirSlash():
    if platform.system() == 'Windows':
        return ('\\')
    elif platform.system() == 'Linux':
        return('/')


def getFileNameDate(fname_date):
    year = int(fname_date[0:4])
    month = int(fname_date[4:6])
    day = int(fname_date[6:8])
    hour = 0
    minute = 0
    seconds = 0
    
    retVal = datetime.datetime(year, month, day, hour, minute, seconds, tzinfo=ClanCommon.UTC_TZ)
    return retVal
    
class memberData:
    def __init__(self, name, rank, numMonths):
        self.name = name
        self.donations = ['N/A'] * numMonths
        self.rank = rank
        
        
    def __str__(self):
        return('member:' + self.name + ' rank:' + str(self.rank) + ' donations:' + str(self.donations))
        

def processDailyHistory(clan_tag):
    
    ClanCommon.init()
    
    record_folder = 'record' + DirSlash()
    record_folder = clan_tag + DirSlash() + 'record' + DirSlash()
    print('\nProcessHistory for Clan Tag {} in {}\n'.format(clan_tag, record_folder))
    
    myTimer.start()
    clan_data = []
    
    # List all the files in the Clan History directory
    file_filter = record_folder + '*' + '*.txt'
    files = glob.glob(file_filter)
    
    
    start_of_week  = datetime.datetime.now()
    
    print(start_of_week .weekday(), start_of_week .day)
    
    start_of_week = start_of_week .replace(day = start_of_week .day - start_of_week .weekday(), hour=0, minute=0, second=0, microsecond=0, tzinfo=ClanCommon.UTC_TZ)
          
    print(start_of_week )
    print()
        
    
    fDates = []
    for file in files:
        if file.find('clan_data') > -1:
#            print(file)
            idx1 = file.rfind('-') + 1
            idx2 = file.rfind('.')
            fTime = getFileNameDate(file[idx1:idx2])
            print('File Time: {}'.format(fTime))
            if fTime >= start_of_week :
                fin = open(file, 'r')
                clan_data.append(json.load(fin))
                fin.close()
                fDates.append(fTime)
            #print(clan_data)
            
            
    for fDate in fDates:
        print(fDate)
        
    members = []
    for i, data in enumerate(clan_data):
#        print(i)
        for j, person in enumerate(data['memberList']):
#            print(j, person['name'])
            found = False
            for member in members:
                #print(j, person['name'], member['name'])
                if person['name'] == member.name:
                    member.donations[i] = str(person['donations'])
                    member.rank = person['clanRank']
                    found = True
                    break;
            if found == False:
                members.append(memberData(person['name'],person['clanRank'], len(fDates)))
                members[len(members)-1].donations[i] = str(person['donations'])

    clan_idx = len(clan_data)-1
    clan_badge = 'https://statsroyale.com/images/clanwars/'
    clan_badge += str(clan_data[clan_idx]['badgeId'])
    
    if clan_data[clan_idx]['clanWarTrophies'] < 600:
        clan_badge += '_bronze3'
    elif clan_data[clan_idx]['clanWarTrophies'] < 1500:
        clan_badge += '_silver3'
    elif clan_data[clan_idx]['clanWarTrophies'] < 3000:
        clan_badge += '_gold3'
    else:
        clan_badge += '_magical'
    clan_badge += '.png'
    
    htmlout = ''
    htmlout += ClanCommon.buildhtmlHeader(clan_data[0]['name'])
    
    # Add Clan Data
    htmlout += '<div style="width:100%;">\n' 
    htmlout += '<div style="float: left; width:50%;">'
    htmlout += '<img style="float:left;margin-bottom:20px;" src="'
    htmlout += clan_badge
    htmlout += '" height="100px" width="72px">\n'
    
    htmlout += '<div style="font-weight:bold;font-size:35px;margin-left:77px;line-height:60px">'
    htmlout +=  clan_data[clan_idx]['name']
    htmlout += '</div>\n'
    htmlout += '<div style="font-size:14px;margin-left=77px">'
    htmlout += clan_data[clan_idx]['description']
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
    # Left Section for Clan Trophies
    htmlout += '<div style="float: left; width:33%;">\n'
    htmlout += '<img style="float:left;margin-bottom:20px;text-align:center;" src="https://cdn.statsroyale.com/images/trophy.png" height="51px" width="51px">\n'
    htmlout += '<div style="font-weight:bold;line-height:20px;font-size:15px">'
    htmlout += str(clan_data[clan_idx]['clanScore'])
    htmlout += '</div>\n'
    htmlout += '<div style="line-height:20px;font-size:15px">Trophies</div>'
    htmlout += '</div>\n' #End Left Section Div

    # Middle Section for Clan War Trophies
    htmlout += '<div style="float: left; width:33%;">\n'
    htmlout += '<img  style="float:left" src="https://cdn.statsroyale.com/images/clan-trophies.png" height="51px" width="51px">\n'
    htmlout += '<div style="font-weight:bold;line-height:20px;font-size:15px">'
    htmlout += str(clan_data[clan_idx]['clanWarTrophies'])
    htmlout += '</div>\n'
    htmlout += '<div style="line-height:20px;font-size:15px">Trophies</div>'

    htmlout += '</div>\n' # End Middle Section Div
    
    #Right Secton (nothing in there yet)
    htmlout += '<div style="float: left; width:33%;"></div>\n'
    htmlout += '<img style="float:left;margin-bottom:20px;text-align:center;" src="https://cdn.statsroyale.com/images/cards.png" height="51px" width="51px">\n'
    htmlout += '<div style="font-weight:bold;line-height:20px;font-size:15px">'
    htmlout += str(clan_data[clan_idx]['donationsPerWeek'])
    htmlout += '</div>\n'
    htmlout += '<div style="line-height:20px;font-size:15px">Donations/week</div>'    
    
    htmlout += '</div>\n' # End Clan Information Section Div
    htmlout += '</div>\n'
    
    htmlout += '<div style="clear:both;"></div>\n'
        
    
    
    #Build Table
    #Add Table Headings
    htmlout += '<div style="clear:both;"></div>\n'
    htmlout += '<div class="container_12">\n'
    htmlout += '<table class="sortable" cellpadding="0" cellspacing="0"  width=90%>\n'
    htmlout += "<thead>\n"
    htmlout += ClanCommon.createTH('Name')
    for fDate in fDates:
        print(fDate.strftime("%d-%b-%Y"))
        htmlout += ClanCommon.createTH(fDate.strftime("%d-%b-%Y"))
    htmlout += '</thead>\n'
    
    htmlout += '<tbody>\n'
    for i,member in enumerate(members):
        htmlout += '<tr>'
        if i == 0:
            css = 'goldbkd'
        elif i == 1:
            css = 'silverbkd'
        elif i == 2:
            css = 'bronzebkd'
        else:
            css = ''
        htmlout += ClanCommon.createTD(member.name, css)
        for j, donation in enumerate(member.donations):
#            print(i, member.name, j, str(donation))
            htmlout += ClanCommon.createTD(donation, css, 'center')
        
        htmlout += '</tr>\n'
        
    htmlout += '</tbody>\n'
    htmlout += '</table>\n'
    htmlout += '<div align=\"right\">\n'
    htmlout += '<p style=\"font-size:10px;right:auto\"> Last Updated: '

    htmlout += datetime.datetime.now().astimezone(tz=ClanCommon.Eastern_TZ).strftime('%d-%b-%Y %I:%M:%S %p %Z')
    htmlout += ' with Version: ' + __version__
    htmlout += '</p>\n'

    htmlout += '</div>\n'
        
    htmlout += ClanCommon.buildhtmlFooter()
#    print(htmlout)
    
    
    htmlFname = clan_tag + DirSlash() + clan_tag + '_daily_donations' + '.html'
    out = open(htmlFname, 'w', encoding='UTF-8')
    out.write(htmlout)
    out.close()
    
    myTimer.end()
    print('Completed in {}'.format(myTimer.elapsedTime()))


def processWeeklyHistory(clan_tag):

    ClanCommon.init()
    
    record_folder = 'record' + DirSlash()
    record_folder = clan_tag + DirSlash() + 'record' + DirSlash()
    print('\nProcessHistory for Clan Tag {} in {}\n'.format(clan_tag, record_folder))
    
    myTimer.start()
    
    # List all the files in the Clan History directory
    file_filter = record_folder + '*' + '*.txt'
    files = glob.glob(file_filter)
    
    
    start_of_week  = datetime.datetime.now()
    start_of_week = start_of_week .replace(day = start_of_week .day - start_of_week .weekday(), hour=0, minute=0, second=0, microsecond=0, tzinfo=ClanCommon.UTC_TZ)
          
    
    fDates = []
    for file in files:
        if file.find('clan_data') > -1:
#            print(file)
            idx1 = file.rfind('-') + 1
            idx2 = file.rfind('.')
            fTime = getFileNameDate(file[idx1:idx2])
#            print('File Time: {}'.format(fTime))
#                fin = open(file, 'r')
#                clan_data.append(json.load(fin))
#                fin.close()
            if fTime.weekday() == ClanCommon.FRI:
                fDates.append(fTime)
            #print(clan_data)

    members = []
            
    for fidx, fDate in enumerate(fDates):
        if fDate.weekday() == ClanCommon.FRI:
            
            fin = open(files[fidx], 'r')
            clan_data = json.load(fin)
            fin.close()

#            for i, data in enumerate(clan_data):
        #        print(i)
            for j, person in enumerate(clan_data['memberList']):
    #            print(j, person['name'])
                found = False
                for member in members:
                    #print(j, person['name'], member['name'])
                    if person['name'] == member.name:
                        member.donations[fidx] = str(person['donations'])
                        member.rank = person['clanRank']
                        found = True
                        break;
                if found == False:
                    members.append(memberData(person['name'],person['clanRank'], len(fDates)))
                    members[len(members)-1].donations[fidx] = str(person['donations'])
        
    for member in members:
        print(member)

    htmlout = ''
    htmlout += ClanCommon.buildhtmlHeader(clan_data['name'])
    
    # Add Clan Data
    htmlout += '<div style="width:100%;">\n' 
    htmlout += '<div style="float: left; width:50%;">'
    
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
#    print(clan_badge)
    
    
    htmlout += '<img style="float:left;margin-bottom:20px;" src="'
    htmlout += clan_badge
    htmlout += '" height="100px" width="72px">\n'
    
    htmlout += '<div style="font-weight:bold;font-size:35px;margin-left:77px;line-height:60px">'
    htmlout +=  clan_data['name']
    htmlout += '</div>\n'
    htmlout += '<div style="font-size:14px;margin-left=77px">'
    htmlout += clan_data['description']
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
    htmlout += str(clan_data['clanWarTrophies'])
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
    htmlout += '<div style="clear:both;"></div>\n'
    htmlout += '<div class="container_12">\n'
    htmlout += '<table class="sortable" cellpadding="0" cellspacing="0"  width=90%>\n'
    htmlout += "<thead>\n"
    htmlout += ClanCommon.createTH('Name')
    for fidx, fDate in enumerate(fDates):
#        if fDate.weekday() == ClanCommon.FRI:
#        print(fDate.strftime("%d-%b-%Y"))
        htmlout += ClanCommon.createTH(fDate.strftime("%d-%b-%Y"))
    htmlout += '</thead>\n'
    
 
    htmlout += '<tbody>\n'
    for i,member in enumerate(members):
        htmlout += '<tr>'
        if i == 0:
            css = 'goldbkd'
        elif i == 1:
            css = 'silverbkd'
        elif i == 2:
            css = 'bronzebkd'
        else:
            css = ''
        htmlout += ClanCommon.createTD(member.name, css)
        for j, donation in enumerate(member.donations):
#            print(i, member.name, j, str(donation))
            htmlout += ClanCommon.createTD(donation, css, 'center')
        
        htmlout += '</tr>\n'
        
    htmlout += '</tbody>\n'
    htmlout += '</table>\n'
    htmlout += '<div align=\"right\">\n'
    htmlout += '<p style=\"font-size:10px;right:auto\"> Last Updated: '

    htmlout += datetime.datetime.now().astimezone(tz=ClanCommon.Eastern_TZ).strftime('%d-%b-%Y %I:%M:%S %p %Z')
    htmlout += ' with Version: ' + __version__
    htmlout += '</p>\n'

    htmlout += '</div>\n'
    htmlout += ClanCommon.buildhtmlFooter()
#    print(htmlout)
    
    
    htmlFname = clan_tag + DirSlash() + clan_tag + '_weekly_donations' + '.html'
    out = open(htmlFname, 'w', encoding='UTF-8')
    out.write(htmlout)
    out.close()
    
    myTimer.end()
    print('Completed in {}'.format(myTimer.elapsedTime()))

            
# Start of main
if __name__ == '__main__':

#    modInit()    
    processDailyHistory('QQG200V')
    processWeeklyHistory('QQG200V')

    
    
    