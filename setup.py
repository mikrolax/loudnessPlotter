#/usr/bin/python
# -*- coding: utf-8 -*-
import os
from distutils.core import setup,Extension

__version__     =__import__('loudness').__version__
__author__      =__import__('loudness').__author__
__author_email__=__import__('loudness').__author_email__
__url__         =__import__('loudness').__url__
__download_url__=__import__('loudness').__download_url__

wave_analyze=Extension('wave_analyze',
                   include_dirs = [os.path.join('ebu_r128','includes')],
                   sources = [os.path.join('ebu_r128','examples','wave','main.c'),
                              os.path.join('ebu_r128','src','ebu_r128.c'),
                              os.path.join('ebu_r128','src','itu-1770-filter.c')])

setup(
    name        ='loudnessplotter',
    version     =__version__,
    author      =__author__,
    author_email=__author_email__,
    url         =__url__,
    download_url=__download_url__,
    long_description=open('README.md').read(),
    classifiers=[
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent',
    'Programming Language :: C',
    'Programming Language :: Python',
    'Topic :: Multimedia :: Sound/Audio',
    'Topic :: Multimedia :: Sound/Audio :: Analysis',
    'Topic :: Scientific/Engineering :: Visualization'],   

    ext_package='ebu_r128',    
    ext_modules=[wave_analyze], 
        
    py_modules=['loudness','test'], 
    #packages=['test'],

    package_data={'ebu_r128': ['LICENSE','README','API' ]},    
    #data_files=[('ebu_r128', ['src/*.c']),
    #            ('ebu_r128', ['includes/*.h']),
    #            ('ebu_r128', ['examples/wave/main.c'])]    
 )

