#! /home/dmmacs/anaconda3/bin/python3
# -*- coding: utf-8 -*-

import ClanCommon
import glob
import json
import datetime
import myTimer
import prop

playerTag = '#8YGUPVPR'
clan_tag = 'QQG200V'
record_folder = 'record' + ClanCommon.DirSlash()
record_folder = clan_tag + ClanCommon.DirSlash() + 'record' + ClanCommon.DirSlash()

seasonStart = datetime.datetime.now()



def genhtml(outData):
    global seasonStart
    

    min_value = 20000
    newData = []
    for i, data in enumerate(reversed(outData)):
#        print(i, data)
        newData.append(data)
#        print(data[1])
        if data[2] < min_value:
            min_value = data[2]
        if data[1] == seasonStart:
        #if data[3] == 0:
        #    if i > 3:
            break
    #print(outData)
    print(min_value)
    min_value /= 100
    min_value = round(min_value,0) * 100
    print(int(min_value))

    htmlout = '<!DOCTYPE HTML>\n'
    htmlout += '<html>\n'
    htmlout += '<head>\n'
    htmlout += '<script>\n'
    htmlout += 'window.onload = function () {\n'
    htmlout += 'var chart = new CanvasJS.Chart("chartContainer", {\n'
    htmlout += '\tanimationEnabled: true,\n'
    htmlout += '\ttheme: "light3",\n'
    htmlout += '\ttitle:{text: "Trophies for ' + outData[0][0] + ' (' + playerTag + ')' + '"},\n'
    htmlout += '\taxisX:{valueFormatString: "DDD MM/DD/YYYY",crosshair: {enabled: true,snapToDataPoint: true}},\n'
    htmlout += '\taxisY: {title: "Trophies",minimum: ' + str(min_value) + ',crosshair: {enabled: true, snapToDataPoint: true}},\n'
    htmlout += '\ttoolTip:{shared:true,animationEnabled: true},\n'
    htmlout += '\tlegend:{cursor:"pointer",verticalAlign: "bottom",horizontalAlign: "left",dockInsidePlotArea: true,itemclick: toogleDataSeries},\n'
    htmlout += '\tdata: [{\n'
    htmlout += '\t\ttype: "line",showInLegend: true,name: "Trophies",markerType: "cross",xValueFormatString: "DDD MM/DD/YYYY",color: "blue",\n'
    htmlout += '\t\tdataPoints: [\n'

    for i, data in enumerate(reversed(newData)):
#        print(data[1].year, data[1].month - 1, data[1].day)
        tmpStr = '\t\t\t{x: new Date(' + str(data[1].year) + ',' + str(data[1].month - 1) + ',' + str(data[1].day) + ')' + ',y: ' + str(data[2]) + '}'
        #print(i, len(newData)) #  + '},'
        if i < len(newData) - 1:
            tmpStr += ','
        tmpStr += '\n'
        htmlout += tmpStr
#        print(tmpStr)
#        print(data)
    htmlout += '\t\t]\n'
    htmlout += '\t},\t]\n'

    htmlout += '});\n'
    htmlout += 'chart.render();\n'
    htmlout += '\n'

    htmlout += 'function toogleDataSeries(e){\n'
    htmlout += '\tif (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {\n'
    htmlout += '\t\te.dataSeries.visible = false;\n'
    htmlout += '\t} else{\n'
    htmlout += '\t\te.dataSeries.visible = true;\n'
    htmlout += '\t}\n'
    htmlout += '\tchart.render();\n'
    htmlout += '\n'
    htmlout += '}\n'
    htmlout += '}\n'

    htmlout += '</script>\n'
    htmlout += '</head>\n'
    htmlout += '<body>\n'
    htmlout += '<div id="chartContainer" style="height: 50%; width: 80%;"></div>\n'
    htmlout += '<script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>\n'
    htmlout += '</body>\n'
    htmlout += '</html>\n'
 
    #print(htmlout)

    print('Saving Data for  ' + outData[0][0])
    fname = clan_tag + ClanCommon.DirSlash() + outData[0][0] + '.html'
    out = open(fname, 'w', encoding='UTF-8')
    print(out.name)
    out.write(htmlout)
    out.close()

    print(record_folder + fname)

def sortSecond(val):
    return(val[1])   

def getTrophyData(tag, clan_tag):
    global seasonStart

    ClanCommon.init()
    record_folder = 'record' + ClanCommon.DirSlash()
    record_folder = clan_tag + ClanCommon.DirSlash() + 'record' + ClanCommon.DirSlash()
    #print('\nProcess Trophy History for {} in {}'.format(clan_tag, record_folder))

    file_filter = record_folder + '*clan_data*' + '*.txt'
    files = glob.glob(file_filter)

    outData = []
    outstr = ''
    for file in files:
        idx1 = file.rfind('-') + 1
        idx2 = file.rfind('.')
        fTime = ClanCommon.getFileNameDate(file[idx1:idx2])
        #        print(file,fTime)
        fin = open(file, 'r')
        clan_data = json.load(fin)
        for person in clan_data['memberList']:
            if person['tag'] == '#8YGUPVPR':
                # print('{},{},{}'.format(fTime.strftime('%d-%b-%Y'),person['name'], person['trophies']))
                outstr += '{},{},{}\n'.format(person['name'], fTime.strftime('%d-%b-%Y'), person['trophies'])
                #outData.append('{},{},{}'.format(person['name'], fTime.strftime('%d-%b-%Y'), person['trophies']))
                outData.append([person['name'],fTime,person['trophies']])
                break


    req = ClanCommon.getAPIData('#8YGUPVPR', 'players')
    playerData = req.json()

    seasonEnd = datetime.datetime(2019,11,17,0,0,0,tzinfo=ClanCommon.UTC_TZ)

    print(seasonEnd)


    outData.sort(key=sortSecond)
    for data in reversed(outData):
        tmp = data[1]
        delta = tmp-seasonEnd
        #print('{}|||{}'.format(delta.days, delta.days % 14))
        data.append(delta.days % 14)

    if prop.props.get('id') == playerData['leagueStatistics']['previousSeason']['id']:
        prop.update_property('id', playerData['leagueStatistics']['previousSeason']['id'])
        yesterday = datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month, datetime.datetime.now().day, 0,0,0,0,tzinfo=ClanCommon.UTC_TZ)
        yesterday = yesterday - datetime.timedelta(days=1)
        prop.update_property('date', yesterday.strftime('%Y-%m-%d'))
        prop.save_properties('season.prop')

    splt = prop.props.get('date').split('-')
    seasonStart = datetime.datetime(int(splt[0]), int(splt[1]), int(splt[2]), 0, 0, 0, tzinfo=ClanCommon.UTC_TZ)
    print(seasonStart)
    #print(outData)
    genhtml(outData)

    fname = record_folder + 'highland' + '.csv'
    #    print(fname)
    out = open(fname, 'w', encoding='UTF-8')
    for data in outData:
        out.write(data[0] + ',' + data[1].strftime('%d-%b-%Y') + ',' + str(data[2]) + ',' + str(data[3]) + '\n')
        #pass
    #out.write(outstr)
    out.close()

    #print(playerData['leagueStatistics'])
#    print(json.dumps(playerData, indent=4))
#    print(playerData['leagueStatistics']['previousSeason']['id'])
    print(playerData['leagueStatistics']['previousSeason']['id'])
    print(prop.props.get('id'))
# Start of main
if __name__ == '__main__':

    prop.load_properties('season.prop')
    print(prop.props)
    myTimer.start()
    ClanCommon.init()


    getTrophyData(playerTag,clan_tag)

    myTimer.end()

    myTimer.printTime()
