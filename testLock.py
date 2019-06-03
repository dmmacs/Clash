#! /home/dmmacs/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""testLock"""

import os
import ClanCommon
import myTimer
import datetime

if __name__ == '__main__':
    myTimer.start()


    lockFname = os.path.dirname(os.path.abspath(__file__))
    lockFname += ClanCommon.DirSlash()
    lockFname += 'ClanData.lck'

    if os.path.exists(lockFname):
        mod_timestamp = datetime.datetime.fromtimestamp(os.stat(lockFname).st_mtime)
        timeNow = datetime.datetime.now()
        
        timediff = (timeNow - mod_timestamp).total_seconds()
        if timediff > 20:
            os.remove(lockFname)


    myTimer.end()
    print('Completed in {}'.format(myTimer.elapsedTime()))


    