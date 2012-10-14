loudnessPlotter
===============

Analyse wav file loudness and plot graph in html 

loudnessPlotter is based on wave_analyze program, writen in C by [radionova labs](http://labs.radionova.no/2011/01/07/ebu-r128-library/). Original source code is provided in ebu_r128 folder.

 Usage
=======

## Windows
Binaries are provided, simply open the command line and type:
	loudnesspplotter.exe [file.wav or folder] [oupoutfolder]


#### from python (All platform)
Make sure you have the compiled the wave_analyse programm for your platform! If not, see later.

As a script:
  python loudness.py /path/to/folder/or/wavefile
  
As a module:
	import loudness
	loudness.LoudnessPlotter(wavfilelist,outpath).process()


Compilation
============
For unix-like platform (linux, MAC OS)

	cd ebu_r128
	make wave_analyze
	

