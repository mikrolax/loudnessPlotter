loudnessPlotter
===============

Analyse wav file loudness and plot graph in html 

`loudnessPlotter` is based on ebu_r128 lib writen in C by [radionova labs](http://labs.radionova.no/2011/01/07/ebu-r128-library/). Original source code is provided.


Installation
==============
## Download
Using git:

    cd /home/user/mypath
    git clone https://github.com/mikrolax/loudnessPlotter.git


## Compilation
### For unix-like platform (linux, MAC OS):
 
    cd ebu_r128
    make wave_analyze
    cp wave_analyze ../


### Windows
`wave_analyze.exe` binarie is provided.  

If you need you can compil it with minGW, take a look at Codeblocks IDE as it can be bundle with it.
So assuming you have mingw installed:

    cd ebu_r128
    mingw32-make wave_analyze
    copy wave_analyze ..\
   
   

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


What it does
=============
Generate a single HTML page (which itself load some javascript from the web): launches wav_analyze executable, get its output, and convert it into an HTML plot.

If you specifie a folder, all .wav under this folder will be analysed, output HTML file name will be : `loudness.html`
If you specifie a wav file i.e. `wavfilename.wav`, output HTML file name will be : `wavfilename.html`


License
==========
[GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.txt)


Credits
==========

[radionova labs](http://labs.radionova.no/2011/01/07/ebu-r128-library/) for providing this lib and wave_analyze example under GNU GPL.

[JQuery](http://jquery.com/), the well-known javascript library 
[flot](http://www.flotcharts.org/) an attactive javascript plotting for JQuery
[Bootstrap](http://twitter.github.com/bootstrap/) the famous CSS/JS framework from Twitter. 


####Links

https://en.wikipedia.org/wiki/Loudness   
https://en.wikipedia.org/wiki/Loudness_monitoring   

[EBU Website](http://tech.ebu.ch/loudness)   
[ITU Rec BS1770](http://www.itu.int/rec/R-REC-BS.1770/en)   

