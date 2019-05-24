#!! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 19 17:10:54 2019

@author: dmmacs
"""
import glob
import platform
import datetime
import pytz
import json

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
    
    retVal = datetime.datetime(year, month, day, hour, minute, seconds, tzinfo=UTC_TZ)
    return retVal
    
class memberData:
    def __init__(self, name):
        self.name = name
        self.donations = []
        
    def __str__(self):
        return('member: ' + self.name + ' donations: ' + str(self.donations))
        

def processHistory(clan_tag):
    print('\nProcessHistory for Clan Tag {}\n'.format(clan_tag))
    
    myTimer.start()
    clan_data = []
    
    record_folder = 'record' + DirSlash()
    # List all the files in the Clan History directory
    file_filter = record_folder + '*' + '*.txt'
    files = glob.glob(file_filter)
    
    fDates = []
    for file in files:
        if file.find('clan_data') > -1:
#            print(file)
            fin = open(file, 'r')
            clan_data.append(json.load(fin))
            fin.close()
            idx1 = file.rfind('-') + 1
            idx2 = file.rfind('.')
            fDates.append(getFileNameDate(file[idx1:idx2]))
            #print(clan_data)

    members = []
    
    for j,data in enumerate(clan_data):
        found = False
        for i,person in enumerate(data['memberList']):
            for member in members:
                if member.name == person['name']:
                    member.donations.append(person['donations'])
                    found = True
                    break
            if found is False:
                members.append(memberData(person['name']))
                members[i].donations.append(person['donations'])
                

    #Build Table
    
    #Headings
#    fout = open('tmp.csv', 'w', encoding='UTF-8')
    tmpStr = 'Name'
    for fDate in fDates:
        tmpStr += ',' + fDate.strftime("%d-%b-%Y")
    
#    fout.write(tmpStr + '\n')
    print(tmpStr)
    
    for member in members:
        tmpStr = member.name
        for donation in member.donations:
            tmpStr += ',' + str(donation)
        print(tmpStr)
#        fout.write(tmpStr + '\n')

#    for member in members:
#        print(member)

#    print(fDates)
            
#            print(json.dumps(data, indent = 4))
    myTimer.end()
    print('Completed in {}'.format(myTimer.elapsedTime()))


# Start of main
if __name__ == '__main__':
    
    
    #Timezones
    UTC_TZ = pytz.timezone('UTC')
    EASTERN_TZ = pytz.timezone("US/Eastern")
    
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6
    


    output_folder = 'output'
    if platform.system() == 'Windows':
        output_folder += '\\'
    elif platform.system() == 'Linux':
        output_folder == '/'

    
    
    processHistory('QQG200V')

    
    
    