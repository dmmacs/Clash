#! /home/dmmacs/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 09:45:50 2019

@author: dmmacs
"""

from _version import __version__
import pytz
import platform
import datetime

def init():
    global UTC_TZ
    global Eastern_TZ
    global MON
    global TUE
    global WED
    global THU
    global FRI
    global SAT
    global SUN
    
    UTC_TZ = pytz.timezone('UTC')
    Eastern_TZ = pytz.timezone("US/Eastern")
    
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6

def DirSlash():
    if platform.system() == 'Windows':
        return ('\\')
    elif platform.system() == 'Linux':
        return('/')

def getFileNameDate(fname_date):
#    init()
    year = int(fname_date[0:4])
    month = int(fname_date[4:6])
    day = int(fname_date[6:8])
    hour = 0
    minute = 0
    seconds = 0
    
    retVal = datetime.datetime(year, month, day, hour, minute, seconds, tzinfo=UTC_TZ)
    return retVal

class myFnames:
    def __init__(self,fName, fDate):
        self.fName = fName
        self.fDate = fDate
    
    def __str__(self):
        return ('FName:' + self.fName + ' FDate:' + self.fDate.strftime('%I:%M:%S %p %Z %d-%b-%Y'))


def buildhtmlHeader (title):
    retVal = ''
    retVal += '<!DOCTYPE HTML>\n'
    retVal += '<html>\n<head>\n'
    retVal += '<meta charset="UTF-8">\n'
    retVal += '<meta scriptVersion="' + __version__ + '">\n'
    retVal += '<title>' + 'Clash Royale - ' + title + ' Clan' + '</title>\n'
    retVal += '<link rel="icon" type="image/png" href="https://developer.clashroyale.com/favicon-16x16.16d92b.png" sizes=16x16>\n'
    retVal += '<link rel="icon" type="image/png" href="https://developer.clashroyale.com/favicon-16x16.16d92b.png" sizes=16x16>\n'
    retVal += '<link rel="icon" type="image/png" href="https://developer.clashroyale.com/favicon-32x32.09ad6d.png" sizes=32x32>\n'
    retVal += '<link rel="icon" type="image/png" href="https://developer.clashroyale.com/favicon-96x96.0fce98.png" sizes=96x96>\n'
    retVal += '<link rel="icon" type="image/png" href="https://developer.clashroyale.com/favicon-192x192.6f82ec.png" sizes=192x192>\n'
    retVal += '<link rel="shortcut icon" href=https://developer.clashroyale.com/favicon.673a60.ico>\n'
    
#    htmlout += '<link href=\"../css/defaultTheme.css\" rel=\"stylesheet\" media=\"screen\" />\n'
#    htmlout += '<link href=\"../css/myTheme.css\" rel=\"stylesheet\" media=\"screen\" />\n'
    retVal += '<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js\"></script>\n'
    retVal += '<script src="../js/sortable.js"></script>\n'

#    htmlout += "<script src=\"../js/jquery.fixedheadertable.js\"></script>\n"
#    htmlout += "<script>$(document).ready(function() {\n$('.myTable01').fixedHeaderTable({ height: '600', footer: false, cloneHeadToFoot: false, themeClass: 'fancyTable', autoShow: true })\n});\n</script>\n"

    retVal +="<link href=\"../css/dashboard.css\" rel=\"stylesheet\" media=\"screen\" />\n"
    retVal +="<link href=\"../css/sortable_table.css\" rel=\"stylesheet\" media=\"screen\" />\n"

    retVal += "</head>\n"

    retVal += "<body>\n"    
    
    
    return retVal


def buildhtmlFooter():
    retVal = '</body>\n'
    retVal += '</html>\n'

    return retVal

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
    return ('<th>' + text + '</th>')

