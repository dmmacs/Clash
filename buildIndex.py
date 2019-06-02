#!! /usr/bin/python3
# -*- coding: utf-8 -*-
"""buildIndex"""
from _version import __version__
import glob
import ClanCommon
import myTimer
import datetime

def processHtmlFiles(clan_tag, clan_name):
    print('\nBuilding Index File for ' + clan_tag)

    ClanCommon.init()

    file_filter = clan_tag + ClanCommon.DirSlash() + '*.html'
    files = glob.glob(file_filter)
    
    
    htmlout = ClanCommon.buildhtmlHeader(clan_name)
    for file in files:
        if file.find('index.html') == -1:
            #<a href="QQG200V/index.html"><img src="https://statsroyale.com/images/clanwars/16000164_silver3.png" height="100px" width="86px">BeaverCleavers - QQG200V</a>
            idx1 = file.find(clan_tag)
            idx2 = file.find(ClanCommon.DirSlash(), idx1) + 1
#            print(file)
#            print(file[idx2:len(file)])
            tmpStr = '<a href="' + file[idx2:len(file)] + '">' + file[idx2:len(file)] + '</a><br/>\n'
            htmlout += tmpStr
            #print(tmpStr)


    htmlout += '<div align=\"right\">\n'
    htmlout += '<p style=\"font-size:10px;right:auto\"> Last Updated: '

    htmlout += datetime.datetime.now().astimezone(tz=ClanCommon.Eastern_TZ).strftime('%d-%b-%Y %I:%M:%S %p %Z')
    htmlout += ' with Version: ' + __version__
    htmlout += '</p>\n'

    htmlout += '</div>\n'

    htmlout += ClanCommon.buildhtmlFooter()
    
    htmlFname = clan_tag + ClanCommon.DirSlash() + 'index' + '.html'
    out = open(htmlFname, 'w', encoding='UTF-8')
    out.write(htmlout)
    out.close()


if __name__ == '__main__':

    myTimer.start()

    clan_tag = 'QQG200V'
    clan_name = 'beavercleavers'
    processHtmlFiles(clan_tag, clan_name)

    myTimer.end()
    print('Completed Build Indexin {}'.format(myTimer.elapsedTime()))
    
    