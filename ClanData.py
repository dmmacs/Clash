#! /home/dmmacs/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""ClanData"""

from _version import __version__
import json
#import openpyxl
import datetime
#import dateutil
#import pytz
import sys
import os
import platform
#import glob
import argparse
import ClanCommon
import myTimer
import ClanHistory
import ClanWar
import buildIndex
import Highland
import logging
import record_cleanup

#def processClashDate(tmpStr):
#    year = int(tmpStr[0:4])
#    month = int(tmpStr[4:6])
#    day = int(tmpStr[6:8])
#    hour = int(tmpStr[9:11])
#    minute = int(tmpStr[11:13])
#    seconds = int(tmpStr[13:15])
#    
#    retVal = datetime.datetime(year, month, day, hour, minute, seconds, tzinfo=ClanCommon.UTC_TZ)
#    return retVal
#

    
# Start of main
if __name__ == '__main__':

    myTimer.start()
    print('Python Version is: ' + platform.python_version())
    print('Script Version is: ' + __version__)
    
    logFname = os.path.dirname(os.path.abspath(__file__)) + ClanCommon.DirSlash() + 'ClanData.log'
    LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(filename=logFname, level=logging.DEBUG, format=LOG_FORMAT,filemode='w')
    logger = logging.getLogger()
    logging.info('Python Version is: ' + platform.python_version() + '\n')
    logging.info('Script Version is: ' + __version__ + '\n')
    
    
    # ***** Constants *****

    ClanCommon.init()
    
    SECONDS_PER_HOUR = 3600
    THREE_QUARTERS = (SECONDS_PER_HOUR / 4 * 3)
    HALF = (SECONDS_PER_HOUR / 4 * 2)
    ONE_QUARTER = (SECONDS_PER_HOUR / 4 * 1)

    hash_sign = '%23'
    clan_tag = 'QQG200V'
    record_folder = 'record'
    history_folder = 'history'
    apiFname = 'api_key.txt'
    
    #Create Lock File
    lockFname = os.path.dirname(os.path.abspath(__file__))
    lockFname += ClanCommon.DirSlash()
    lockFname += 'ClanData.lck'
    #if os.path.exists(lockFname):
    #    print('Lock File already exists')
    #    sys.exit(-1)
#    out = open(lockFname, 'w+')
#    out.write('Running')
#    out.close()
    

#    parser.add_argument('-o', '--output', default='.', required=True, help='Output Folder for HTML and excel files')
#    parser.add_argument('-e', '--excel', action='store_true', default=False, required=False, help='Enables Excel File output')
#    parser.add_argument('-s', '--silent', action='store_true', default=False, required=False, help='Turns on silent mode which will only output error messages to stdout')
#    parser.add_argument('--verbose', default=0, type=int,required=False, help='Enables LoggingLevel Mode')

    parser = argparse.ArgumentParser(description='Arguments for ClanData.py')
    parser.add_argument('-k','--key', default='api_key.txt', required=False, help='File that contains the api key')
    parser.add_argument('-c','--clantag', default='QQG200V', required=False, help='Clan Tag to get data for')
    parser.add_argument('-o','--output', default='record', required=False, help='Folder to store raw data')
    parser.add_argument('-v', '--version', action='version', version='Version: ' + __version__)
    parser.add_argument('-H', '--history', action='store_true', default=False, required=False,help='Build History Tables for Donations and War')
    parser.add_argument('-T', '--tag', default='', required=False, help='Gamer Tag to capture Trophy History')
    
    args = parser.parse_args()
    print(args)
    logging.info('API Argument: ' + args.key + '\n')    
    
    if args.key:
        apiFname = args.key
    if args.clantag:
        clan_tag = args.clantag
    if args.output:
        record_folder = args.output
        
    #Read Key from File
    try:
        fname = os.path.dirname(__file__)
        fname = os.path.dirname(os.path.abspath(__file__))
        fname += ClanCommon.DirSlash()

        fname += apiFname
        fin = open(fname, 'r')
        key = fin.readline().strip()
        fin.close()
    except FileNotFoundError:
        print("Unable to find api key file, " + os.path.realpath(__file__) + apiFname)
        sys.exit(-1)

    htmlFname = clan_tag + ClanCommon.DirSlash() + 'clan_data.html'

    # Check to see if the clan_tag folder exists:
    if os.path.isdir(clan_tag) is False:
        # Directory does not exist, create it
        try:
            os.makedirs(clan_tag)
        except OSError as exc:
            print(exc.errno)

    record_folder = clan_tag + ClanCommon.DirSlash() + record_folder + ClanCommon.DirSlash()
    history_folder = clan_tag + ClanCommon.DirSlash() + history_folder + ClanCommon.DirSlash()

    #Check to see if record_folder exists:
    if os.path.isdir(record_folder) is False:
        # Directory does not exist, create it
        try:
            os.makedirs(record_folder)
        except OSError as exc:
            print(exc.errno)

    #Check to see if record_folder exists:
    if os.path.isdir(history_folder) is False:
        # Directory does not exist, create it
        try:
            os.makedirs(history_folder)
        except OSError as exc:
            print(exc.errno)
        

    print('Record Folder = ' + record_folder)
    _authorization = 'authorization' + ':' + key
    
    link = 'https://api.clashroyale.com/v1/clans/QQG200V/members'
    link_clan = 'https://api.clashroyale.com/v1/clans/%23' + clan_tag #QQG200V'
    link_members = 'https://api.clashroyale.com/v1/clans/%' + clan_tag + '/members' #23QQG200V/members'
    link_warlog = 'https://api.clashroyale.com/v1/clans/%' + clan_tag + '/warlog'
    link_current_war = 'https://api.clashroyale.com/v1/clans/%' + clan_tag + '/currentwar'
    link_tourn_global = 'https://api.clashroyale.com/v1/globaltournaments'

    reqHeaders = {"Accept":"application/json", "authorization":"Bearer " + key}
    # Get Clan Data
    print('Getting Clan Data')
    req = ClanCommon.getAPIData(clan_tag, 'ClanData')
    if (req.status_code != 200):
        print('Could not read Clan Data Api, Response Code {}'.format(req.status_code))
        sys.exit(-1)
    clan_data = req.json()
    print('\tClan Data for ' + clan_data['name'])
    
    # Get Clan member Data
    print('Getting Clan Member Data')
    req = ClanCommon.getAPIData(clan_tag, 'ClanMembers')
    if (req.status_code != 200):
        print('Could not read Clan Member Data Api, Response Code {}'.format(req.status_code))
        sys.exit(-1)
    clan_member_data = req.json()
    print('\ttotal Clan Members = ' + str(clan_data['members']))
    
    # Get Clan warlog Data
    print('Getting WarLog Data')
    req = ClanCommon.getAPIData(clan_tag, 'WarLog')
    if (req.status_code != 200):
        print('Could not read War Log Api, Response Code {}'.format(req.status_code))
        sys.exit(-1)
    clan_warlog = req.json()        
    print('\ttotal Clan Members = ' + str(clan_data['members']))
    
    # Get Clan Current War Data
    print('Getting Current War Data')
    req = ClanCommon.getAPIData(clan_tag, 'CurrentWar')
    if (req.status_code != 200):
        print('Could not read Current War Api, Response Code {}'.format(req.status_code))
        sys.exit(-1)
    clan_current_war = req.json()
    print('\tClan War State = ' + str(clan_current_war['state']))# + ' until ' + ClanCommon.processClashDate(clan_current_war['warEndTime']).strftime('%d-%b-%Y %I:%M:%S %p %Z'))
    
    
    # Get Global Tournament Data
    print('Getting Global Tournament Data')
    req = ClanCommon.getAPIData(clan_tag, 'GlobalTournament')
    if (req.status_code != 200):
        print('Could not read Global Tournament Data Api, Response Code {}'.format(req.status_code))
        sys.exit(-1)
    tourn_global_data = req.json()
    if len(tourn_global_data['items']) > 0:
        print('\tGlobal Tournament Title: ' + tourn_global_data['items'][0]['title'])# + ' until ' + processClashDate(tourn_global_data['items'][0]['endTime']).astimezone(tz=Eastern_TZ).strftime('%d-%b-%Y %I:%M:%S %p %Z'))
    
    
    #Generate HTML Output
    
    htmlout = ''
    htmlout = ClanCommon.buildhtmlHeader(clan_data['name'])
    htmlout += '<div style="width:100%;text-align:center;font-weight: bold;font-size:150%">' + 'Clan Data for ' + clan_data['name'] + '</div><br/>\n'
    
    
    #Clan Name Section
    htmlout += '<div style="width:100%;">\n' 
    htmlout += '<div style="float: left; width:50%;">'
    
    clan_badge = 'https://statsroyale.com/images/clanwars/'
    clan_badge += str(clan_data['badgeId'])
    
    clan_war_level = ClanCommon.getWarLeague(clan_data['clanWarTrophies'])
    if clan_war_level.find('Bronze') > -1:
#    if clan_data['clanWarTrophies'] < 600:
        clan_badge += '_bronze3'
    elif clan_war_level.find('Silver') > -1:
#    elif clan_data['clanWarTrophies'] < 1500:
        clan_badge += '_silver3'
        clan_war_level = 'Bronze'
    elif clan_war_level.find('Gold') > -1:
#    elif clan_data['clanWarTrophies'] < 3000:
        clan_badge += '_gold3'
    else:
        clan_badge += '_magical'
    clan_badge += '.png'
    
    
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
    htmlout += clan_current_war['state']
    htmlout += '<br/>' + clan_war_level + '</div>'
    htmlout += '<div style="line-height:20px;font-size:15px">'
    if clan_current_war['state'] == 'warDay':
        warEndTime = ClanCommon.processClashDate(clan_current_war['warEndTime'])
        htmlout += 'War Ends:'
        htmlout += warEndTime.astimezone(tz=ClanCommon.Eastern_TZ).strftime('%I:%M:%S %p %Z %d-%b-%Y')
        htmlout += ' </div></div>'
    elif clan_current_war['state'] == 'collectionDay':
        warEndTime = ClanCommon.processClashDate(clan_current_war['collectionEndTime'])
        htmlout += 'Collection Ends:'
        htmlout += warEndTime.astimezone(tz=ClanCommon.Eastern_TZ).strftime('%I:%M:%S %p %Z %d-%b-%Y')
        htmlout += ' </div></div>'
    
    
    htmlout += '</div>\n'
    htmlout += '</div>\n'
    
    
    
    
    htmlout += '<div style="clear:both"></div>\n'
    
    #Clan Information Section
    htmlout += '<div style="width:100%;">\n' #Full clan Information Section Div
    
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
    
    htmlout += '<div class="container_12">\n'

    htmlout += '<table class="sortable" cellpadding="0" cellspacing="0"  width=90%>\n'
    htmlout += "<thead>\n"
    htmlout += ClanCommon.createTH('Clan Rank')
    htmlout += ClanCommon.createTH('Name')
    htmlout += ClanCommon.createTH('Role')
    htmlout += ClanCommon.createTH('Level')
    htmlout += ClanCommon.createTH('Last Seen (Hours)')
    htmlout += ClanCommon.createTH('Trophies')
    htmlout += ClanCommon.createTH('Arena')
    htmlout += ClanCommon.createTH('Donations')
    htmlout += '\n</thead>\n'
    
    
    htmlout += '<tbody>\n'
    for item in clan_member_data["items"]:
        
        htmlout += '<tr>'

        if item['clanRank'] == 1:
            css = 'goldbkd'
        elif item['clanRank'] == 2:
            css = 'silverbkd'
        elif item['clanRank'] == 3:
            css = 'bronzebkd'
        else:
            css = ''
        htmlout += ClanCommon.createTD(str(item['clanRank']), css, 'center')
        htmlout += ClanCommon.createTD(item['name'], css)
        htmlout += ClanCommon.createTD(item['role'], css)
        htmlout += ClanCommon.createTD(str(item['expLevel']), css, 'center')

        last_seen = ClanCommon.processClashDate(item['lastSeen'])
        
        timeNow = datetime.datetime.now().replace(microsecond=0)
        timeNow = timeNow.astimezone(tz=ClanCommon.UTC_TZ)
        timediff = timeNow -  last_seen
        
        hours,rest = divmod(timediff.total_seconds(), SECONDS_PER_HOUR)
        rest = rest % SECONDS_PER_HOUR
        
        if rest >= HALF:
            hours += 1
        

        htmlout += ClanCommon.createTD('{}'.format(hours), css)        
        htmlout += ClanCommon.createTD(str(item['trophies']), css, 'center')
        htmlout += ClanCommon.createTD(item['arena']['name'], css)
        htmlout += ClanCommon.createTD(str(item['donations']), css, 'center')
        htmlout += '</tr>\n'
        
    htmlout += '</tbody>\n'

    htmlout += '</table>\n'
    htmlout += '</div>\n'
    
    # add last update date
    htmlout += '<div align=\"right\">\n'
    htmlout += '<p style=\"font-size:10px;right:auto\"> Last Updated: '

    htmlout += timeNow.astimezone(tz=ClanCommon.Eastern_TZ).strftime('%d-%b-%Y %I:%M:%S %p %Z')
    htmlout += ' with Version: ' + __version__
    htmlout += '</p>\n'

    htmlout += '</div>\n'
    htmlout += ClanCommon.buildhtmlFooter()
    
    # Write HTML File

    with open(htmlFname, 'w', encoding='UTF-8') as out:    
        out.write(htmlout)
    
    #Capture weekly data if its time, between 23:55 and 11:59:59
    midnight = timeNow.replace(hour=23, minute=59, second=59, microsecond=0)
    eleven_fifty_five = timeNow.replace(hour=23, minute=55, second=0, microsecond=0)
    
    
    file_time_stamp = timeNow.astimezone(tz=ClanCommon.Eastern_TZ).strftime('%Y%m%d')
    #Save Clan Data
    fname = record_folder
    fname += clan_data['name'] 
    fname += '-'
    fname += 'clan_data'
    fname += '-'
    fname += file_time_stamp
    fname += '.txt'
    print('Saving Clan Data ' + fname)
    with open(fname, 'w', encoding='UTF-8') as out:
        out.write(json.dumps(clan_data, indent = 4))
    
    
    if timeNow > eleven_fifty_five and timeNow < midnight:
        fname = fname.replace(record_folder, history_folder)
        out = open(fname, 'w', encoding='UTF-8')
        out.write(json.dumps(clan_data, indent = 4))
        out.close()
        
        # If it Sunday, put a copy of the data in the history folder
        if timeNow.weekday() == 2:#ClanCommon.SUN
            fname = fname.replace('.txt', '_weekly.txt')
            out = open(fname, 'w', encoding='UTF-8')
            out.write(json.dumps(clan_data, indent = 4))
            out.close()
    
        
    
    #Save Clan Member Data
    fname = record_folder
    fname += clan_data['name'] 
    fname += '-'
    fname += 'clan_member_data'
    fname += '-'
    fname += file_time_stamp
    fname += '.txt'
    print('Saving Clan Member Data ' + fname)
    
    with open(fname, 'w', encoding='UTF-8') as out:
        out.write(json.dumps(clan_member_data, indent = 4))
    if timeNow > eleven_fifty_five and timeNow < midnight:
        fname = fname.replace(record_folder, history_folder)
        out = open(fname, 'w', encoding='UTF-8')
        out.write(json.dumps(clan_data, indent = 4))
        out.close()
        
    #Save Warlog Data
    fname = record_folder
    fname += clan_data['name'] 
    fname += '-'
    fname += 'warlog'
    fname += '-'
    fname += file_time_stamp
    fname += '.txt'
    print('Saving Warlog Data ' + fname)
    with open(fname, 'w', encoding='UTF-8') as out:
        out.write(json.dumps(clan_warlog, indent = 4))
    if timeNow > eleven_fifty_five and timeNow < midnight:
        fname = fname.replace(record_folder, history_folder)
        out = open(fname, 'w', encoding='UTF-8')
        out.write(json.dumps(clan_data, indent = 4))
        out.close()

    #Save Current War Data
    fname = record_folder
    fname += clan_data['name'] 
    fname += '-'
    fname += 'currentwar'
    fname += '-'
    fname += file_time_stamp
    fname += '.txt'
    print('Saving Current War Data ' + fname)
    with open(fname, 'w', encoding='UTF-8') as out:
        out.write(json.dumps(clan_current_war, indent = 4))
    if timeNow > eleven_fifty_five and timeNow < midnight:
        fname = fname.replace(record_folder, history_folder)
        out = open(fname, 'w', encoding='UTF-8')
        out.write(json.dumps(clan_data, indent = 4))
        out.close()

    #Save Global Tournament Data
    fname = record_folder
    fname += clan_data['name'] 
    fname += '-'
    fname += 'tourn_global_data'
    fname += '-'
    fname += file_time_stamp
    fname += '.txt'
    print('Saving Global Tournament Data ' + fname)
    with open(fname, 'w', encoding='UTF-8') as out:
        out.write(json.dumps(tourn_global_data, indent = 4))
    if timeNow > eleven_fifty_five and timeNow < midnight:
        fname = fname.replace(record_folder, history_folder)
        out = open(fname, 'w', encoding='UTF-8')
        out.write(json.dumps(clan_data, indent = 4))
        out.close()
    
    if args.history:
        ClanHistory.processWeeklyHistory(clan_tag, clan_data)
        ClanHistory.processDailyHistory(clan_tag, clan_data)

    if args.tag:
        Highland.getTrophyData('#8YGUPVPR',clan_tag)

    ClanWar.processClanWar(clan_tag, clan_data)
    ClanWar.processNonParticipant(clan_tag, clan_data)
    buildIndex.processHtmlFiles(clan_tag, clan_data['name'])

    record_cleanup.clean_up_files(clan_tag, 'beavercleavers', '-clan_member_data')
    record_cleanup.clean_up_files(clan_tag, 'beavercleavers', '-clan_data-')
    record_cleanup.clean_up_files(clan_tag, 'beavercleavers', '-currentwar-')
    record_cleanup.clean_up_files(clan_tag, 'beavercleavers', '-tourn_global_data-')
    record_cleanup.clean_up_files(clan_tag, 'beavercleavers', '-warlog-')
    

#    if os.path.exists(lockFname):
#        os.remove(lockFname)


    myTimer.end()
    print()
    print('Completed ClanData in {}'.format(myTimer.elapsedTime()))
    
    
    
    