#!/usr/bin/python2 
#-*- coding: utf-8 -*-

## ======================================================================
## Contains functions for logging and debugging.
##
## Copyright (C) 2013-2014 Jonas Møller
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## ======================================================================

import inspect, sys, traceback
from time import time, ctime, strftime, gmtime
from sys import stdout
from threading import currentThread

import GlobalVariables as GV

enable_color = False
color = {
        "DEFAULT": "\x1b[0;00m",
        "PANIC": "\x1b[1;31m",
        "FAIL": "\x1b[1;31m",
        "NOTICE": "",
        "DEBUG": "",
        "ERROR": "\x1b[1;33m",
        "SUCCESS": "\x1b[1;32m",
        "WARNING": "\x1b[1;31m",
        }

try:
    __logfile__ = open(GV.logfile_name, "a")
except (IOError, OSError):
    print("[WARNING]: Error while opening log file, continuing...")

def out(msg, end="\r\n", c="\x1b[0;33m"):
    stdout.write((c if c else "") + str(msg) + ("\x1b[0;00m" if c else "") + str(end))
    stdout.flush()

## XXX: Some functions still specify the function argument in log functions,
##      this is no longer needed and not recommended. No effort is being made
##      to replace all the occurenses of Log.xxx(function="yyy"), but this
##      could be accomplished with a not too complicated regex.

## TODO: I should define all these functions to take the arguments (comment, **kwargs)
##       the problem is that i would have to review all Log calls.

## All the log and error functions will pass all exceptions quietly, the last thing
## we want is the error message function crashing the server...

def fprint(fileobj, data):
    fileobj.write(data + GV.eol)
    fileobj.flush()

def genericLog(logtype, message, cr=False, **kwargs):
    if cr:
        ## Carriage return
        stdout.write("\r")
    if enable_color:
        stdout.write(color.get(logtype, ""))
    log = "[%s] %8s: %14s: %20s: %s" % (getTime(), logtype, currentThread().getName(), getCaller(), message)
    print(log)
    if enable_color:
        stdout.write(color["DEFAULT"])
    if kwargs.get("trace"):
        ## Print the traceback, indented with four spaces
        stdout.write("".join(["    "+x+GV.eol for x in traceback.format_exc(kwargs["trace"]).splitlines()]))
    fprint(__logfile__, log)

## Called by genericLog, which is called by panic/error/log etc, which is called by the [function we want]
def getCaller():
    curframe = inspect.currentframe()
    return inspect.getouterframes(curframe, 2)[3][3]

def getTime():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def panic(comment, **kwargs):
    genericLog("PANIC", comment, **kwargs)
    fail(255)

def fail(ret, **kwargs):
    genericLog("FAIL", "Failing due to previous errors", **kwargs)
    ## All threads are set as daemon, therefore this will halt the entire server
    sys.exit(ret)

def notice(comment, **kwargs):
    genericLog("NOTICE", comment, **kwargs)

def debug(comment, **kwargs):
    genericLog("DEBUG", comment, **kwargs)

## (comment, **kwargs) is used because of the deprecated function kwargument.
def error(comment, **kwargs):
    genericLog("ERROR", comment, **kwargs)

def log(comment, **kwargs):
    ## Legacy
    genericLog("NOTICE", comment, **kwargs)

def success(comment, **kwargs):
    genericLog("SUCCESS", comment, **kwargs)

def warning(comment, **kwargs):
    genericLog("WARNING", comment, **kwargs)

if __name__ == '__main__':
    pass
