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

def getFileNameDate(fname_date):
    year = int(fname_date[0:4])
    month = int(fname_date[4:6])
    day = int(fname_date[6:8])
    hour = 0
    minute = 0
    seconds = 0
    
    retVal = datetime.datetime(year, month, day, hour, minute, seconds, tzinfo=UTC_TZ)
    return retVal
    


def processHistory():
    print('\nProcessHistory\n')
    
    base_fname = '-clan_data-'
    file_filter = output_folder + '*' + base_fname + '*.txt'
    files = glob.glob(file_filter)
    print(files)

    # Determine day of files
    for file in files:
        idx1 = file.find(base_fname) + len(base_fname)
        idx2 = file.find('.', idx1)
        fTime = getFileNameDate(file[idx1:idx2])
        
        if fTime.weekday() == SUN:
            print(file)
            fin = open(file, 'r')
            
            clan_data = json.load(fin);
            fin.close()
            print(json.dumps(clan_data, indent = 4))



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

    
    
    processHistory()
    
    
    