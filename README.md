# Launchbox CHD Interceptor
## Description
A tool that sits between the Launchbox Frontend and your emulator to decompress and passthrough CHD-packed .bin/.cue games.
Designed for Launchbox but should work standalone and with other Frontends.

**Does not currently work with RetroArch.**
## Setup Guide
### Requirements
* Windows OS (may work on Linux/MacOS but untested)
* [Launchbox Frontend](https://www.launchbox-app.com/) (May work with others or as standalone)
* makechd.exe from the latest [MAME](https://www.mamedev.org/) release
* .bin/.cue games packed in CHD format
* An emulator with .cue support
### Video
Coming Soon
### Windows
1. Download the latest release and extract it to a folder.
2. Run the .exe once to generate a blank configuration file.
3. Copy makechd.exe into the root folder.
4. Open `config.ini` and edit the following:
    * Edit `tempdir` to change where CHD files are tempoarily unpacked when run (defaults to `C:\Users\(username)\Appdata\Local\Temp\lbchd\`).
    * Edit `preservetemp` to change whether the unpacked bin/cue files are kept after use. This makes starting games faster but uses more disk space.
5. To add a new emulator, open `config.ini` and:
    1. Add a new config section with the format `[name]` where name is the short name used to call the emulator from Launchbox.
    2. Within the new section, add `fullname=` with the full name of the emulator, this is used within the program to refer to the emulator.
    3. Add `exec=` with the full path to the emulator's executable.
6. Open Launchbox and add LBCHD's executable as a new emulator.
7. Add the platform for a specific emulator under the Supported Platforms menu and put the shortname of the emulator in the Default Command Line section (see Step 5.1 for this).
8. Add CHD files to Launchbox and run them.