#loudnessPlotter
*****************

Analyse wave file loudness and plot graph in html.`loudnessPlotter` is based on ebu_r128 lib writen in C by [radionova labs](http://labs.radionova.no/2011/01/07/ebu-r128-library/). 
Original source code is provided. Application is portable, i.e. can run off a USB key for instance.

see [website](http://mikrolax.github.com/loudnessPlotter/) for more information.

           

### Download
#####Using git

    cd /home/user/mypath
    git clone https://github.com/mikrolax/loudnessPlotter.git

#####Manual Download   
Zip downlod on [Github](https://github.com/mikrolax/loudnessPlotter/zipball/master)      
           
<br>
     
## Basic Usage
********
>Make sure you have the `wave_analyze` programm for your platform! See [documentation](http://mikrolax.github.com/loudnessPlotter/doc) for more information about usage, option, template etc...

### Windows  
Binaries are provided, simply open the command line and type:

    loudnessPlotter.exe [file.wav or folder] [ouputfolder]

### From python (all platform)

As a script:

    python loudness.py /path/to/folder/or/wavefile
  
As a module:

    import loudness
    loudness.LoudnessPlotter(wavfilelist,outpath).process() #analyse and write HTML with plot


###What it does

Generate a single HTML page (which itself load some javascript from the web): launches wav_analyze executable, get its output, and convert it into an HTML plot.

If you specifie a folder, all .wav under this folder will be analysed, output HTML file name will be : `loudness.html`   
If you specifie a wav file i.e. `wavfilename.wav`, output HTML file name will be : `wavfilename.html`      
        
<br>              
<br>        




##Credits
**********
[radionova labs](http://labs.radionova.no/2011/01/07/ebu-r128-library/) for providing this lib and wave_analyze example under GNU GPL.
[JQuery](http://jquery.com/), the well-known javascript library   
[flot](http://www.flotcharts.org/) an attactive javascript plotting for JQuery      
[Bootstrap](http://twitter.github.com/bootstrap/) the famous CSS/JS framework from Twitter.        


##License
**********
[GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.txt) 
     

## Contibuting  
**********
Fork on github, develop, and send me patch. Or contact me via e-mail.     


<hr>   
###### Normatives, references   
[[1](https://en.wikipedia.org/wiki/Loudness)] Wikipedia page for loudness   
[[2](https://en.wikipedia.org/wiki/Loudness_monitoring)] Wikipedia page for loudness monitoring     
[[3](http://tech.ebu.ch/loudness)] EBU R128 website     
[[4](http://www.itu.int/rec/R-REC-BS.1770/en)] ITU R-REC-BS.1770 on ITU website      
[[5](http://labs.radionova.no/2011/01/07/ebu-r128-library/)] radionovas original ebu_r128 lib links   