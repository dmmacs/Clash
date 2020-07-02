#! /home/dmmacs/anaconda3/bin/python3
# -*- coding: utf-8 -*-

import os
import datetime
import pytz

props = {}
def update_property(id, value):
    props[id] = value

def load_properties(filepath, sep='=', comment_char='#'):
    """
    Read the file passed as parameter as a properties file.
    """
    global props
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"')
                props[key] = value
    return props

def updateProp(prop, data):
    print()

def save_properties(filepath,sep='=', comment_char='#'):
    print('#Updated by: ' + os.environ['USERNAME'])
    now = datetime.datetime.now(tz=pytz.timezone("US/Arizona"))
    print('#' + now.strftime('%d-%b-%Y %I:%M:%S %p %Z'))

    global props

    with open(filepath, 'wt') as f:
        # Add Comments
        f.write('#Updated by: ' + os.environ['USERNAME'] + '\n')
        f.write('#' + now.strftime('%d-%b-%Y %I:%M:%S %p %Z') + '\n')

        for key in props.keys():
            tmpStr = key + sep + str(props[key])
            f.write(tmpStr + '\n')
            print(tmpStr)