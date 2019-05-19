# -*- coding: utf-8 -*-
"""
Created on Sat May 18 09:45:50 2019

@author: dmmacs
"""

import requests
import json
#import openpyxl
import time
import datetime
import pytz


def createTD(text):
    return ('<td>' + text + '</td>')

def createTH(text):
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
    
    key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjY1ODMyYzNlLTQ1YzctNGMwNC1iNTkwLTgyYTI0YzQyMDhiMiIsImlhdCI6MTU1ODIwNTQ5MCwic3ViIjoiZGV2ZWxvcGVyLzE4YzkyMzA4LTE2YzYtZjhmYy0yMjMzLTY0YTM2ZjliZjMyNyIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI3MC4xNzcuMTY3LjcwIl0sInR5cGUiOiJjbGllbnQifV19.ah33L09g2vdZ0qZYU8gkby60R4x2QhPZefeES9qXkuH4D-t8sqYw1M5p-xzeboSWHune8rKQw2A277QnWlLR-w'
    
    _authorization = 'authorization' + ':' + key
    
    link = 'https://api.clashroyale.com/v1/clans/QQG200V/members'
    link_clan = 'https://api.clashroyale.com/v1/clans/%23QQG200V'
    link_members = 'https://api.clashroyale.com/v1/clans/%23QQG200V/members'
    
    
    
    
    
    #headers={"Accept":"application/json", "authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjAwNzdlMDJjLTVlZGMtNDA1Ni1hZWNhLTZjZWMwMzRiYjQ4NiIsImlhdCI6MTUzNDM0NjYyMCwic3ViIjoiZGV2ZWxvcGVyL2JlYjQ5NzYzLWNhMzMtNTllYy02MTBjLTAzZmM2MzVmN2Y1OCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxOTAuMjI4LjIyMy4xMzMiXSwidHlwZSI6ImNsaWVudCJ9XX0.YAag5hP2ic3-uURi0eqUwHedL9vLaBgVa19BSbEWHdvi2hn4s1QROwqZRQOsKJMTph_G6kHgBUX2vrEmmmQ3vw"    
    #r = requests.get(link_clan, headers={"Accept":"application/json", "authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjY1ODMyYzNlLTQ1YzctNGMwNC1iNTkwLTgyYTI0YzQyMDhiMiIsImlhdCI6MTU1ODIwNTQ5MCwic3ViIjoiZGV2ZWxvcGVyLzE4YzkyMzA4LTE2YzYtZjhmYy0yMjMzLTY0YTM2ZjliZjMyNyIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI3MC4xNzcuMTY3LjcwIl0sInR5cGUiOiJjbGllbnQifV19.ah33L09g2vdZ0qZYU8gkby60R4x2QhPZefeES9qXkuH4D-t8sqYw1M5p-xzeboSWHune8rKQw2A277QnWlLR-w"})
    r = requests.get(link_members, headers={"Accept":"application/json", "authorization":"Bearer " + key})
    #print(json.dumps(r.json(), indent = 2))
    
    json_string = json.dumps(r.json(), indent = 4)
    #print(json_string)
    
    data_store = r.json()
    
    
    htmlout = ''
    htmlout += '<!DOCTYPE HTML>\n'
    htmlout += '<html>\n<head>\n'
    htmlout += '<title>' + 'Clash Royale - BeaverCleavers Clan' + '</title>\n'
    htmlout += '<link href=\"defaultTheme.css\" rel=\"stylesheet\" media=\"screen\" />\n'
    htmlout += '<link href=\"myTheme.css\" rel=\"stylesheet\" media=\"screen\" />\n'
    htmlout += '<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js\"></script>\n'
    htmlout += '<script src="sortable.js"></script>'

    htmlout += "<script src=\"jquery.fixedheadertable.js\"></script>\n"
    htmlout += "<script>$(document).ready(function() {\n$('.myTable01').fixedHeaderTable({ height: '600', footer: false, cloneHeadToFoot: false, themeClass: 'fancyTable', autoShow: true })\n});\n</script>\n"

    htmlout +="<link href=\"dashboard.css\" rel=\"stylesheet\" media=\"screen\" />\n"
    htmlout +="<link href=\"sortable_table.css\" rel=\"stylesheet\" media=\"screen\" />\n"

    htmlout += "</head>\n"

    htmlout += "<body>\n"

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
    
    #print(json_string["items"][3])
    #print(datastore["office"].get("law"))
    #print(data_store["items"][3])
    
    htmlout += '<tbody>\n'
    for item in data_store["items"]:
        #print(item['lastSeen'])
        
        htmlout += '<tr>'
        htmlout += createTD(item['name'])
        htmlout += createTD(item['role'])
        htmlout += createTD(str(item['expLevel']))
        #2019 05 18 T 23 49 06.000Z
        last_seen_str = item['lastSeen']
        year = int(last_seen_str[0:4])
        month = int(last_seen_str[4:6])
        day = int(last_seen_str[6:8])
        hour = int(last_seen_str[9:11])
        minute = int(last_seen_str[11:13])
        seconds = int(last_seen_str[13:15])
        timezone = pytz.timezone('UTC')
        
        last_seen= datetime.datetime(year, month, day, hour, minute, seconds, tzinfo=pytz.utc)
#            print(last_seen)
#        timezone = pytz.timezone(tz=pytz.UTC)
#            print(last_seen.astimezone(tz=eastern))
#            print(last_seen.astimezone(tz=eastern).strftime('%d-%b-%Y %I:%M:%S %p'))
        timeNow = datetime.datetime.now().replace(microsecond=0)
        timeNow = timeNow.astimezone(tz=timezone)
        timediff = timeNow -  last_seen
            
        hours,rest = divmod(timediff.total_seconds(), SECONDS_PER_HOUR)
        rest = rest % SECONDS_PER_HOUR

        if rest >= HALF:
            hours += 1
#                        
#            print(timeNow.astimezone(tz=eastern).strftime('%d-%b-%Y %I:%M:%S %p'))
#            print('{} hours ago'.format(hours))
            
            #hours,rest = divmod(timediff, 3600)
            #print(hours)
        htmlout += createTD('{} hours ago'.format(hours))
            
            
#        last_seen = datetime.datetime()
        #time.time(item['lastSeen'])
        htmlout += createTD(str(item['trophies']))
        htmlout += createTD(item['arena']['name'])
        htmlout += createTD(str(item['clanRank']))
        htmlout += createTD(str(item['donations']))
        htmlout += '</tr>\n'
        
        #print(item['name'])
    htmlout += '</tbody>\n'

    htmlout += '</table>\n'
    htmlout += '</body\n'
    htmlout += '</html>\n'
    
    
#    f = open('tmp.txt', 'w')
#    f.write(json.dumps(r.json(), indent = 2))
#    f.close()

    out = open('index.html', 'w', encoding='UTF-8')
    out.write(htmlout)
    out.close()
    
    