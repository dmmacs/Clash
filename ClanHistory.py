#! /home/dmmacs/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 19 17:10:54 2019

@author: dmmacs
"""
import glob
import platform
import datetime
import json
import ClanCommon
import sys

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
                    found = True
                    break;
            if found == False:
                members.append(memberData(person['name'],person['clanRank'], len(fDates)))
                members[len(members)-1].donations[i] = str(person['donations'])
#                    members[j].donations.append(str(person['donations']))

                

    
    htmlout = ''
    htmlout += ClanCommon.buildhtmlHeader(clan_data[0]['name'])
    
    # Add Clan Data
    
    
    
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
        
        
    htmlout += ClanCommon.buildhtmlFooter()
#    print(htmlout)
    
    
    htmlFname = clan_tag + DirSlash() + clan_tag + '_daily_donations' + '.html'
    out = open(htmlFname, 'w', encoding='UTF-8')
    out.write(htmlout)
    out.close()
    
    myTimer.end()
    print('Completed in {}'.format(myTimer.elapsedTime()))


def processWeeklyHistory(clan_tag):
    history_folder = 'history' + DirSlash()
#    record_folder = clan_tag + DirSlash() + 'record' + DirSlash()
    print('\nProcessHistory for Clan Tag {} in {}\n'.format(clan_tag, history_folder))


# Start of main
if __name__ == '__main__':

#    modInit()    
    processDailyHistory('QQG200V')
    #processWeeklyHistory('QQG200V')

    
    
    