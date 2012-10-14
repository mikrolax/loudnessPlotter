loudnessPlotter
===============

Analyse wav file loudness and plot graph in html 

`loudnessPlotter` is based on ebu_r128 lib writen in C by [radionova labs](http://labs.radionova.no/2011/01/07/ebu-r128-library/). Original source code is provided in ebu_r128 folder.


Installation
==============
## Download
Using git:

    cd /home/user/mypath
    git clone https://github.com/mikrolax/loudnessPlotter.git

## Compil
### For unix-like platform (linux, MAC OS):

    cd ebu_r128
    make wave_analyze
    cp wave_analyze ../

### Windows
`wave_analyze.exe` binarie is provided. If you need you can compil it with minGW, take a look at Codeblocks IDE as it can be bundle with it.


Usage
=======

### Windows
Binaries are provided, simply open the command line and type:

    loudnesspplotter.exe [file.wav or folder] [oupoutfolder]

### from python (All platform)
Make sure you have the compiled the `wave_analyse` programm for your platform! If not, see above.

As a script:

    python loudness.py /path/to/folder/or/wavefile
  
As a module:

    import loudness
    loudness.LoudnessPlotter(wavfilelist,outpath).process()


License
==========
[GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.txt)


Credits
==========
[radionova labs](http://labs.radionova.no/2011/01/07/ebu-r128-library/) for providing this lib and wave_analyze example under GNU GPL.


####Links
https://en.wikipedia.org/wiki/Loudness
https://en.wikipedia.org/wiki/Loudness_monitoring

