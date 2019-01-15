#!/usr/bin/env python3
import configparser
import os
import subprocess
import tempfile
import sys
import ntpath
import glob
FNULL = open(os.devnull, 'w')
# Config initialisation and reading functions
config = configparser.ConfigParser()
configpath = os.getcwd()+'/config.ini'


def createconfig():
    if os.path.isfile(configpath):  # Check if config exists and create it if it doesn't
        pass
    else:
        # Insert config generation here
        config['lbchd'] = {'tempdir': '',  # Folder to store unpacked files in, defaults to OS Temp if blank
                           'preservetemp': 0}  # Keep files after run, 0 = delete, 1 = keep
        with open(configpath, 'w') as configfile:
            config.write(configfile)
            configfile.close()


def readconfig(section, field):
    config.read(configpath)
    try:
        return config[section][field]  # Return desired value from the config, -1 otherwise
    except KeyError:
        return -1


def unpackchd(emulator, romfile):
    # If the temp folder value in the config is not empty, set its value for use.
    # Otherwise, use the tempfile module to find the OS's temp directory and use it.
    if readconfig('lbchd', 'tempdir') != '':
        templocation = str(readconfig('lbchd', 'tempdir'))+'/lbchd/'
    else:
        templocation = tempfile.gettempdir()+'/lbchd/'
    os.makedirs(templocation, exist_ok=True)
    # Check config for details on the desired emulator. If the values don't exist, terminate the script.
    if readconfig(emulator, 'fullname') == -1:
        print('ERROR: Config file is missing the fullname for', emulator)
        sys.exit(1)
    if readconfig(emulator, 'exec') == -1:
        print('ERROR: Config file is missing the exec for', emulator)
        sys.exit(1)
    # Check if the given CHD exists.
    if not os.path.exists(romfile):
        print('ERROR: Rom CHD does not exist.')
        sys.exit(1)
    rombase = os.path.splitext(ntpath.basename(romfile))[0]  # Extract the name of the CHD without the extension.
    romtemp = templocation+'/'+rombase+'.cue'  # The full path the CUE Sheet for the rom will be extracted to.
    makechd = os.getcwd()+'/chdman.exe'  # Path to the chdman executable.
    if not os.path.exists(romtemp):  # Check if the extracted file already exists and skip extraction if it does.
        print('CHD found, extracting to temp location.')
        # Use subprocess to run makechd and unpack the CHD to the temp directory.
        subprocess.run([makechd, 'extractcd', '-i', romfile, '-o', romtemp], stdin=FNULL, stderr=FNULL, stdout=FNULL)
        print('ROM Extracted.')
    else:
        print('ROM already found in temp location.')
    print('Starting', readconfig(emulator, 'fullname'))
    # Run the emulator specified by the user with the arguments from the config file.
    subprocess.run([readconfig(emulator, 'exec'), romtemp], stdin=FNULL, stderr=FNULL, stdout=FNULL)
    if readconfig('lbchd', 'preservetemp') == '0':  # If the user set it, delete the extracted rom files.
        print('Deleting temp location.')
        chdunpacklist = glob.glob(templocation+'/'+rombase+'**')
        for rbin in chdunpacklist:
            os.remove(rbin)


if __name__ == '__main__':
    createconfig()  # Initialise config
    if not os.path.exists(os.getcwd()+'/chdman.exe'):
        print('ERROR: chdman.exe is missing.')
        print('This can be obtained from the latest MAME release.')
        sys.exit(1)
    if len(sys.argv) != 3:  # Check if two arguments were passed to the script
        print('ERROR: Unexpected or missing arguments.')
        print('Format: launchbox-chd-interceptor.exe [emulator] [ROM fullpath]')
        sys.exit(1)
    else:
        unpackchd(sys.argv[1], sys.argv[2])  # Grab arguments and pass them to the main function.
