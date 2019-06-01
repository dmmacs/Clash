# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 11:31:42 2019

@author: dmmacs
"""
import time 

global myStart

def start():
    global myStart
    myStart = time.time()

def end():
    global myEnd
    myEnd = time.time()

def formatFloat(fmt, val):
  ret = fmt % val
  if ret.startswith("0."):
    return ret[1:]
  if ret.startswith("-0."):
    return "-" + ret[2:]
  return ret

def elapsedTime():
    elapsed = myEnd - myStart
    retVal = time.strftime("%H:%M:%S", time.gmtime(elapsed))
    retVal += formatFloat('%.3f',elapsed - int(elapsed))
    
    return(retVal)

def printTime():
    #elapsed = myEnd - myStart
    #print(time.strftime("%H:%M:%S", time.gmtime(elapsed)), end="")
    #print(formatFloat('%.3f',elapsed - int(elapsed)))
    print(elapsedTime())
    
    
    