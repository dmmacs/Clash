#! /home/dmmacs/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 09:45:50 2019

@author: dmmacs
"""

import requests
import json
#import openpyxl
import datetime
import pytz
import sys
import os
import platform

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

if __name__ == '__main__':

    SECONDS_PER_HOUR = 3600
    THREE_QUARTERS = (SECONDS_PER_HOUR / 4 * 3)
    HALF = (SECONDS_PER_HOUR / 4 * 2)
    ONE_QUARTER = (SECONDS_PER_HOUR / 4 * 1)

    hash_sign = '%23'
    clan_tag = 'QQG200V'
    #https://api.clashroyale.com/v1/clans/%23QQG200V
    #https://api.clashroyale.com/v1/clans/%23QQG200V/members

    apiFname = 'api_key.txt'
    #Read Key from File
    try:
        fname = os.path.dirname(__file__)
        fname = os.path.dirname(os.path.abspath(__file__))
        if platform.system() == 'Windows':
            fname += '\\'
        elif platform.system() == 'Linux':
            fname += '/'
        fname += apiFname
        fin = open(fname, 'r')
        key = fin.readline().strip()
        fin.close()
    except FileNotFoundError:
        print("Unable to find api key file, " + os.path.realpath(__file__) + apiFname)
        sys.exit(-1)
        
    _authorization = 'authorization' + ':' + key
    
    link = 'https://api.clashroyale.com/v1/clans/QQG200V/members'
    link_clan = 'https://api.clashroyale.com/v1/clans/%23QQG200V'
    link_members = 'https://api.clashroyale.com/v1/clans/%' + clan_tag + '/members' #23QQG200V/members'
    
    r = requests.get(link_clan, headers={"Accept":"application/json", "authorization":"Bearer " + key})
    clan_data = r.json();
    r.close()
    
    #print(json.dumps(clan_data, indent = 4))
    
    r = requests.get(link_members, headers={"Accept":"application/json", "authorization":"Bearer " + key})
    
    data_store = r.json()
    r.close()
    
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
    htmlout += '<img style="float:left;margin-bottom:20px;" src="https://statsroyale.com/images/clanwars/16000164_silver3.png" height="100px" width="72px">\n'
    
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
#    htmlout += '<div style="width:100%;"">\n'
#    htmlout += '<div align="center" style="text-align:left;">\n'
#    htmlout += '<img style="float:left;margin-bottom:20px;text-align:center;" src="https://cdn.statsroyale.com/images/trophy.png" height="51px" width="51px">\n'
#    htmlout += '<div style="line-height:25px;font-size:23px;font-weight:bold">'
#    htmlout += str(clan_data['clanScore'])
#    htmlout += '</div>\n'
#    htmlout += '<div style="line-height:20px;font-size:15px">Trophies</div>\n'
#    
#    # Clan War Information
#    htmlout += '<div class="clan_info">\n'
#    htmlout += '<div style="text-align:center;">\n'
#    htmlout += '<img style="float:left;margin-bottom:20px" src="https://cdn.statsroyale.com/images/clan-trophies.png" height="51px" width="51px">\n'
#    htmlout += '<div style="line-height:25px;font-size:23px;font-weight:bold">'
#    htmlout += str(clan_data['clanWarTrophies'])
#    htmlout += '</div>\n'
#    htmlout += '<div style="line-height:20px;font-size:15px">Trophies</div>\n'
#    
    
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
    for item in data_store["items"]:
        
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

        last_seen_str = item['lastSeen']
        year = int(last_seen_str[0:4])
        month = int(last_seen_str[4:6])
        day = int(last_seen_str[6:8])
        hour = int(last_seen_str[9:11])
        minute = int(last_seen_str[11:13])
        seconds = int(last_seen_str[13:15])
        timezone = pytz.timezone('UTC')
        
        last_seen= datetime.datetime(year, month, day, hour, minute, seconds, tzinfo=pytz.utc)

        timeNow = datetime.datetime.now().replace(microsecond=0)
        timeNow = timeNow.astimezone(tz=timezone)
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
    eastern = pytz.timezone("US/Eastern")
#    print(timeNow.astimezone(tz=eastern).strftime('%d-%b-%Y %I:%M:%S %p %Z'))
    htmlout += timeNow.astimezone(tz=eastern).strftime('%d-%b-%Y %I:%M:%S %p %Z')
    htmlout += '</p>\n'
#        htmlBuilder.append("<p style=\"font-size:10px;right:auto\"> Dashboard Version: ").append("v").append(jarVer).append("</p>\n");
    htmlout += '</div>\n'
    
    
    out = open('index.html', 'w', encoding='UTF-8')
    out.write(htmlout)
    out.close()
    
    
    out = open('tmp.txt', 'w', encoding='UTF-8')
    out.write(json.dumps(clan_data, indent = 4))
    out.close()
    
    #Capture weekly data if its time, between 23:55 and 11:59:59
    midnight = timeNow.replace(hour=23, minute=59, second=59, microsecond=0)
    eleven_fifty_five = timeNow.replace(hour=23, minute=55, second=0, microsecond=0)
#    timeNow = timeNow.replace(hour=23, minute=57, second=33, microsecond=0)
#    print(timeNow)
#    print(midnight)
#    print(eleven_fifty_five)
    if timeNow > eleven_fifty_five and timeNow < midnight:
        fname = clan_data['name'] 
        fname += '-'
        fname += timeNow.strftime('%Y%m%d')
        fname += '.txt'
        print('Writing Daily Cland Data to: ' + fname)
        out = open(fname, 'w', encoding='UTF-8')
        out.write(json.dumps(clan_data, indent = 4))
        out.close()
        #print('Time to save the weekly data', fname)
    
    