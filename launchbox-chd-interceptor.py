#!/usr/bin/env python3
import configparser
import os
# Config initialisation and reading functions
config = configparser.ConfigParser()
configpath = os.getcwd()+'/config.ini'
def createconfig():
    if os.path.isfile(configpath):
        pass
    else:
        # Insert config generation here
        pass
def readconfig(section,field):
    config.read(configpath)
    try:
        return config[section][field]
    except KeyError:
        return 'ERROR: Section or Field does not exist'
