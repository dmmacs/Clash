#! /home/dmmacs/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 09:45:50 2019

@author: dmmacs
"""

from _version import __version__
import requests
import json
#import openpyxl
import datetime
import pytz
import sys
import os
import platform
import glob
import argparse

def createTD(text, css='', align=''):
    retVal = '<td '
    if css != '':
        retVal += 'class=' + css 
    
    if align!= '':
        retVal += ' style=text-align:' + align + ';'
    retVal += '>'
    retVal +=  text + '</td>'
    return (retVal)

def createTH(text, css=''):
    return ('<th>' + text + '</tj>')

def processClashDate(tmpStr):
    year = int(tmpStr[0:4])
    month = int(tmpStr[4:6])
    day = int(tmpStr[6:8])
    hour = int(tmpStr[9:11])
    minute = int(tmpStr[11:13])
    seconds = int(tmpStr[13:15])
    
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
        print(file)
        idx = file.find(base_fname) + len(base_fname)
        print(str(idx), file)#file[idx:len(base_fname)])
        
    
    
    



# Start of main
if __name__ == '__main__':

    # ***** Constants *****
    #Timezones
    UTC_TZ = pytz.timezone('UTC')
    Eastern_TZ = pytz.timezone("US/Eastern")

    
    SECONDS_PER_HOUR = 3600
    THREE_QUARTERS = (SECONDS_PER_HOUR / 4 * 3)
    HALF = (SECONDS_PER_HOUR / 4 * 2)
    ONE_QUARTER = (SECONDS_PER_HOUR / 4 * 1)

    hash_sign = '%23'
    clan_tag = 'QQG200V'
    output_folder = 'output'
    history_folder = 'history'
    apiFname = 'api_key.txt'

#    parser.add_argument('-o', '--output', default='.', required=True, help='Output Folder for HTML and excel files')
#    parser.add_argument('-e', '--excel', action='store_true', default=False, required=False, help='Enables Excel File output')
#    parser.add_argument('-s', '--silent', action='store_true', default=False, required=False, help='Turns on silent mode which will only output error messages to stdout')
#    parser.add_argument('--verbose', default=0, type=int,required=False, help='Enables LoggingLevel Mode')

    parser = argparse.ArgumentParser(description='Arguments for ClanData.py')
    parser.add_argument('-k','--key', default='')#, required=False)
    parser.add_argument('-c','--clantag', default='')
    parser.add_argument('-o','--output', default='')
    parser.add_argument('-v', '--version', action='version', version='Version: ' + __version__)
    
    args = parser.parse_args()
    
    
    if args.key:
        apiFname = args.key
    if args.clantag:
        clan_tag = args.clantag
    if args.output:
        output_folder = args.output
        
#    print(args)
    

#    print(apiFname)
    #Read Key from File
    try:
        fname = os.path.dirname(__file__)
        fname = os.path.dirname(os.path.abspath(__file__))
        if platform.system() == 'Windows':
            fname += '\\'
            output_folder += '\\'
            history_folder += '\\'
        elif platform.system() == 'Linux':
            fname += '/'
            output_folder += '/'
            history_folder += '/'
        fname += apiFname
        fin = open(fname, 'r')
        key = fin.readline().strip()
        fin.close()
    except FileNotFoundError:
        print("Unable to find api key file, " + os.path.realpath(__file__) + apiFname)
        sys.exit(-1)

    print('Output Folder = ' + output_folder)
    _authorization = 'authorization' + ':' + key
    
    link = 'https://api.clashroyale.com/v1/clans/QQG200V/members'
    link_clan = 'https://api.clashroyale.com/v1/clans/%23' + clan_tag #QQG200V'
    link_members = 'https://api.clashroyale.com/v1/clans/%' + clan_tag + '/members' #23QQG200V/members'
    link_warlog = 'https://api.clashroyale.com/v1/clans/%' + clan_tag + '/warlog'
    link_current_war = 'https://api.clashroyale.com/v1/clans/%' + clan_tag + '/currentwar'
    link_tourn_global = 'https://api.clashroyale.com/v1/globaltournaments'

    
    # Get Clan Data
    print('Getting Clan Data')
    r = requests.get(link_clan, headers={"Accept":"application/json", "authorization":"Bearer " + key})
    clan_data = r.json();
    r.close()
    print('\tClan Data for ' + clan_data['name'])
    
    # Get Clan member Data
    print('Getting Clan Member Data')
    r = requests.get(link_members, headers={"Accept":"application/json", "authorization":"Bearer " + key})
    clan_member_data = r.json()
    r.close()
    print('\ttotal Clan Members = ' + str(clan_data['members']))
    
    # Get Clan warlog Data
    print('Getting WarLog Data')
    r = requests.get(link_warlog, headers={"Accept":"application/json", "authorization":"Bearer " + key})
    clan_warlog = r.json()
    r.close()
    print('\ttotal Clan Members = ' + str(clan_data['members']))
    
    # Get Clan Current War Data
    print('Getting Current War Data')
    r = requests.get(link_current_war, headers={"Accept":"application/json", "authorization":"Bearer " + key})
    clan_current_war = r.json()
    r.close()
    print(json.dumps(clan_current_war, indent = 4))
    print('\tClan War State = ' + str(clan_current_war['state']))# + ' until ' + processClashDate(clan_current_war['warEndTime']).strftime('%d-%b-%Y %I:%M:%S %p %Z'))
    
    
    # Get Global Tournament Data
    print('Getting Global Tournament Data')
    r = requests.get(link_tourn_global, headers={"Accept":"application/json", "authorization":"Bearer " + key})
    tourn_global_data = r.json()
    r.close()
    print('\tGlobal Tournament Title: ' + tourn_global_data['items'][0]['title'])# + ' until ' + processClashDate(tourn_global_data['items'][0]['endTime']).astimezone(tz=Eastern_TZ).strftime('%d-%b-%Y %I:%M:%S %p %Z'))
#    print(json.dumps(tourn_global_data, indent = 4))
#    print(processClashDate(tourn_global_data['items'][0]['endTime']).astimezone(tz=Eastern_TZ).strftime('%d-%b-%Y %I:%M:%S %p %Z'))
    
    
    
    
    htmlout = ''
    htmlout += '<!DOCTYPE HTML>\n'
    htmlout += '<html>\n<head>\n'
    htmlout += '<title>' + 'Clash Royale - ' + clan_data['name'] + 'Clan' + '</title>\n'
    htmlout += '<link rel="icon" type="image/png" href="https://developer.clashroyale.com/favicon-16x16.16d92b.png" sizes=16x16/>\n'
    htmlout += '<link rel="icon" type="image/png" href="https://developer.clashroyale.com/favicon-16x16.16d92b.png" sizes=16x16>\n'
    htmlout += '<link rel="icon" type="image/png" href="https://developer.clashroyale.com/favicon-32x32.09ad6d.png" sizes=32x32>\n'
    htmlout += '<link rel="icon" type="image/png" href="https://developer.clashroyale.com/favicon-96x96.0fce98.png" sizes=96x96>\n'
    htmlout += '<link rel="icon" type="image/png" href="https://developer.clashroyale.com/favicon-192x192.6f82ec.png" sizes=192x192>\n'
    htmlout += '<link rel="shortcut icon" href=https://developer.clashroyale.com/favicon.673a60.ico>\n'
    
#    htmlout += '<link href=\"css/defaultTheme.css\" rel=\"stylesheet\" media=\"screen\" />\n'
#    htmlout += '<link href=\"css/myTheme.css\" rel=\"stylesheet\" media=\"screen\" />\n'
    htmlout += '<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js\"></script>\n'
    htmlout += '<script src="js/sortable.js"></script>\n'

#    htmlout += "<script src=\"js/jquery.fixedheadertable.js\"></script>\n"
#    htmlout += "<script>$(document).ready(function() {\n$('.myTable01').fixedHeaderTable({ height: '600', footer: false, cloneHeadToFoot: false, themeClass: 'fancyTable', autoShow: true })\n});\n</script>\n"

    htmlout +="<link href=\"css/dashboard.css\" rel=\"stylesheet\" media=\"screen\" />\n"
    htmlout +="<link href=\"css/sortable_table.css\" rel=\"stylesheet\" media=\"screen\" />\n"

    htmlout += "</head>\n"

    htmlout += "<body>\n"
    
    #Clan Name Section
    htmlout += '<div style="width:100%;">\n' 
    
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
    htmlout += createTH('Clan Rank')
    htmlout += createTH('Name')
    htmlout += createTH('Role')
    htmlout += createTH('Level')
    htmlout += createTH('Last Seen')
    htmlout += createTH('Trophies')
    htmlout += createTH('Arena')
    htmlout += createTH('Donations')
    htmlout += '</thead>\n'
    
    
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
        htmlout += createTD(str(item['clanRank']), css, 'center')
        htmlout += createTD(item['name'], css)
        htmlout += createTD(item['role'], css)
        htmlout += createTD(str(item['expLevel']), css, 'center')

        last_seen = processClashDate(item['lastSeen'])
        
        timeNow = datetime.datetime.now().replace(microsecond=0)
        timeNow = timeNow.astimezone(tz=UTC_TZ)
        timediff = timeNow -  last_seen
        
        hours,rest = divmod(timediff.total_seconds(), SECONDS_PER_HOUR)
        rest = rest % SECONDS_PER_HOUR

        if rest >= HALF:
            hours += 1
        htmlout += createTD('{} hours ago'.format(hours), css)
        htmlout += createTD(str(item['trophies']), css, 'center')
        htmlout += createTD(item['arena']['name'], css)
        htmlout += createTD(str(item['donations']), css, 'center')
        htmlout += '</tr>\n'
        
    htmlout += '</tbody>\n'

    htmlout += '</table>\n'
    htmlout += '</body\n'
    htmlout += '</html>\n'
    
    # add last update date
    htmlout += '<div align=\"right\">\n'
    htmlout += '<p style=\"font-size:10px;right:auto\"> Last Updated: '

    htmlout += timeNow.astimezone(tz=Eastern_TZ).strftime('%d-%b-%Y %I:%M:%S %p %Z')
    htmlout += ' with Version: ' + __version__
    htmlout += '</p>\n'

    htmlout += '</div>\n'
    
    # Write HTML File    
    out = open('index.html', 'w', encoding='UTF-8')
    out.write(htmlout)
    out.close()
    
    #Capture weekly data if its time, between 23:55 and 11:59:59
    midnight = timeNow.replace(hour=23, minute=59, second=59, microsecond=0)
    eleven_fifty_five = timeNow.replace(hour=23, minute=55, second=0, microsecond=0)
    
    
    file_time_stamp = timeNow.astimezone(tz=Eastern_TZ).strftime('%Y%m%d')
    #Save Clan Data
    fname = output_folder
    fname += clan_data['name'] 
    fname += '-'
    fname += 'clan_data'
    fname += '-'
    fname += file_time_stamp
    fname += '.txt'
    print('Saving Clan Data' + fname)
    out = open(fname, 'w', encoding='UTF-8')
    out.write(json.dumps(clan_data, indent = 4))
    out.close()

    if timeNow > eleven_fifty_five and timeNow < midnight:
        fname = fname.replace(output_folder, history_folder)
        out = open(fname, 'w', encoding='UTF-8')
        out.write(json.dumps(clan_data, indent = 4))
        out.close()
    
    #Save Clan Member Data
    fname = output_folder
    fname += clan_data['name'] 
    fname += '-'
    fname += 'clan_member_data'
    fname += '-'
    fname += file_time_stamp
    fname += '.txt'
    print('Saving Clan Member Data' + fname)
    out = open(fname, 'w', encoding='UTF-8')
    out.write(json.dumps(clan_member_data, indent = 4))
    out.close()
    if timeNow > eleven_fifty_five and timeNow < midnight:
        fname = fname.replace(output_folder, history_folder)
        out = open(fname, 'w', encoding='UTF-8')
        out.write(json.dumps(clan_data, indent = 4))
        out.close()
    
    
    #Save Warlog Data
    fname = output_folder
    fname += clan_data['name'] 
    fname += '-'
    fname += 'warlog'
    fname += '-'
    fname += file_time_stamp
    fname += '.txt'
    print('Saving Warlog Data' + fname)
    out = open(fname, 'w', encoding='UTF-8')
    out.write(json.dumps(clan_warlog, indent = 4))
    out.close()
    if timeNow > eleven_fifty_five and timeNow < midnight:
        fname = fname.replace(output_folder, history_folder)
        out = open(fname, 'w', encoding='UTF-8')
        out.write(json.dumps(clan_data, indent = 4))
        out.close()

    #Save Current War Data
    fname = output_folder
    fname += clan_data['name'] 
    fname += '-'
    fname += 'currentwar'
    fname += '-'
    fname += file_time_stamp
    fname += '.txt'
    print('Saving Current War Data' + fname)
    out = open(fname, 'w', encoding='UTF-8')
    out.write(json.dumps(clan_current_war, indent = 4))
    out.close()
    if timeNow > eleven_fifty_five and timeNow < midnight:
        fname = fname.replace(output_folder, history_folder)
        out = open(fname, 'w', encoding='UTF-8')
        out.write(json.dumps(clan_data, indent = 4))
        out.close()

    #Save Global Tournament Data
    fname = output_folder
    fname += clan_data['name'] 
    fname += '-'
    fname += 'tourn_global_data'
    fname += '-'
    fname += file_time_stamp
    fname += '.txt'
    print('Saving Global Tournament Data' + fname)
    out = open(fname, 'w', encoding='UTF-8')
    out.write(json.dumps(tourn_global_data, indent = 4))
    out.close()
    if timeNow > eleven_fifty_five and timeNow < midnight:
        fname = fname.replace(output_folder, history_folder)
        out = open(fname, 'w', encoding='UTF-8')
        out.write(json.dumps(clan_data, indent = 4))
        out.close()
    
