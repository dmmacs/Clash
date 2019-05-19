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

def createTD(text, css=''):
    retVal = '<td '
    if css != '':
        retVal += 'class=' + css 
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
        print(fname)
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
    
    print(json.dumps(clan_data, indent = 4))
    
    #headers={"Accept":"application/json", "authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjAwNzdlMDJjLTVlZGMtNDA1Ni1hZWNhLTZjZWMwMzRiYjQ4NiIsImlhdCI6MTUzNDM0NjYyMCwic3ViIjoiZGV2ZWxvcGVyL2JlYjQ5NzYzLWNhMzMtNTllYy02MTBjLTAzZmM2MzVmN2Y1OCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxOTAuMjI4LjIyMy4xMzMiXSwidHlwZSI6ImNsaWVudCJ9XX0.YAag5hP2ic3-uURi0eqUwHedL9vLaBgVa19BSbEWHdvi2hn4s1QROwqZRQOsKJMTph_G6kHgBUX2vrEmmmQ3vw"    
    #r = requests.get(link_clan, headers={"Accept":"application/json", "authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjY1ODMyYzNlLTQ1YzctNGMwNC1iNTkwLTgyYTI0YzQyMDhiMiIsImlhdCI6MTU1ODIwNTQ5MCwic3ViIjoiZGV2ZWxvcGVyLzE4YzkyMzA4LTE2YzYtZjhmYy0yMjMzLTY0YTM2ZjliZjMyNyIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI3MC4xNzcuMTY3LjcwIl0sInR5cGUiOiJjbGllbnQifV19.ah33L09g2vdZ0qZYU8gkby60R4x2QhPZefeES9qXkuH4D-t8sqYw1M5p-xzeboSWHune8rKQw2A277QnWlLR-w"})
    r = requests.get(link_members, headers={"Accept":"application/json", "authorization":"Bearer " + key})
    #print(json.dumps(r.json(), indent = 2))
    
    json_string = json.dumps(r.json(), indent = 4)
    #print(json_string)
    
    data_store = r.json()
    r.close()
    
    htmlout = ''
    htmlout += '<!DOCTYPE HTML>\n'
    htmlout += '<html>\n<head>\n'
    htmlout += '<title>' + 'Clash Royale - ' + clan_data['name'] + 'Clan' + '</title>\n'
    htmlout += '<link rel="icon" type="image/png" href="https://developer.clashroyale.com/favicon-16x16.16d92b.png" sizes=16x16/ >'
    htmlout += '<link rel="icon" type="image/png" href="https://developer.clashroyale.com/favicon-16x16.16d92b.png" sizes=16x16>'
    htmlout += '<link rel="icon" type="image/png" href="https://developer.clashroyale.com/favicon-32x32.09ad6d.png" sizes=32x32>'
    htmlout += '<link rel="icon" type="image/png" href="https://developer.clashroyale.com/favicon-96x96.0fce98.png" sizes=96x96>'
    htmlout += '<link rel="icon" type="image/png" href="https://developer.clashroyale.com/favicon-192x192.6f82ec.png" sizes=192x192>'
    htmlout += '<link rel="shortcut icon" href=https://developer.clashroyale.com/favicon.673a60.ico>'
    
    htmlout += '<link href=\"css/defaultTheme.css\" rel=\"stylesheet\" media=\"screen\" />\n'
    htmlout += '<link href=\"css/myTheme.css\" rel=\"stylesheet\" media=\"screen\" />\n'
    htmlout += '<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js\"></script>\n'
    htmlout += '<script src="js/sortable.js"></script>\n'

    htmlout += "<script src=\"js/jquery.fixedheadertable.js\"></script>\n"
    htmlout += "<script>$(document).ready(function() {\n$('.myTable01').fixedHeaderTable({ height: '600', footer: false, cloneHeadToFoot: false, themeClass: 'fancyTable', autoShow: true })\n});\n</script>\n"

    htmlout +="<link href=\"css/dashboard.css\" rel=\"stylesheet\" media=\"screen\" />\n"
    htmlout +="<link href=\"css/sortable_table.css\" rel=\"stylesheet\" media=\"screen\" />\n"

    htmlout += "</head>\n"

    htmlout += "<body>\n"
    
    #Clan Name Section
    htmlout += '<div class="clan_header">\n' 
    htmlout += '<h1 class="clan_name">'
    htmlout +=  clan_data['name']
    htmlout += '</h1>\n'
    htmlout += '<p class="clan_description">'
    htmlout += clan_data['description']
    htmlout += '</p>\n'
    htmlout += '</div>\n'
    
    #Clan Information Section
    htmlout += '<div class="clan_info">\n'
    htmlout += '<h1 class="clan_name">'
    htmlout +=  str(clan_data['clanScore'])
    htmlout += '</h1>\n'
#    htmlout += '<p class="clan_description">'
#    htmlout += clan_data['description']
#    htmlout += '</p>\n'
    htmlout += '</div>\n'

    htmlout += '<div class="container_12">\n'

    htmlout += '<table class="sortable" cellpadding="0" cellspacing="0">\n'
    htmlout += "<thead>\n"
    htmlout += createTH('Name')
    htmlout += createTH('Role')
    htmlout += createTH('Level')
    htmlout += createTH('Last Seen')
    htmlout += createTH('Trophies')
    htmlout += createTH('Arena')
    htmlout += createTH('Clan Rank')
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
        htmlout += createTD(item['name'], css)
        htmlout += createTD(item['role'], css)
        htmlout += createTD(str(item['expLevel']), css)

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
        htmlout += createTD(str(item['trophies']), css)
        htmlout += createTD(item['arena']['name'], css)
        
        htmlout += createTD(str(item['clanRank']), css)
        htmlout += createTD(str(item['donations']), css)
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
    
    
    print(os.path.realpath(__file__))
    