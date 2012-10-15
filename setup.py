#/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup
import zipfile
import sys
import os
import glob

def zip_folder(folder_path, output_path):
    """Zip the contents of an entire folder (with that folder included
    in the archive). Empty subfolders will be included in the archive
    as well.
    """
    #ZipFile.setpassword(pwd)
    parent_folder = os.path.dirname(folder_path)                                      
    contents = os.walk(folder_path)
    try:
        zip_file = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)
        for root, folders, files in contents:
            for folder_name in folders:
                absolute_path = os.path.join(root, folder_name)
                relative_path = absolute_path.replace(parent_folder,'')
                zip_file.write(absolute_path, relative_path)
            for file_name in files:
                absolute_path = os.path.join(root, file_name)
                relative_path = absolute_path.replace(parent_folder,'')
                zip_file.write(absolute_path, relative_path)
    except IOError, message:
        print message
    except OSError, message:
        print message
    except zipfile.BadZipfile, message:
        print message
    finally:
        zip_file.close()

def find_data_files(source,target,patterns):
    """Locates the specified data-files and returns the matches
    in a data_files compatible format.

    source is the root of the source data tree.
        Use '' or '.' for current directory.
    target is the root of the target data tree.
        Use '' or '.' for the distribution directory.
    patterns is a sequence of glob-patterns for the
        files you want to copy.
    """
    if glob.has_magic(source) or glob.has_magic(target):
        raise ValueError("Magic not allowed in src, target")
    ret = {}
    for pattern in patterns:
        pattern = os.path.join(source,pattern)
        for filename in glob.glob(pattern):
            if os.path.isfile(filename):
                targetpath = os.path.join(target,os.path.relpath(filename,source))
                path = os.path.dirname(targetpath)
                ret.setdefault(path,[]).append(filename)

    return sorted(ret.items())

    
if sys.platform == 'win32':
  import py2exe
  import loudness
  #sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),'Microsoft.VC90.CRT'))
  setup(
      name='loudnessPlotter',
      version=loudness.__version__,
      author=loudness.__author__,
      options = {'py2exe': {'bundle_files': 1,'dist_dir':'bin/'}}, #, 'optimize': 2,
      zipfile = None,
      console=[{'script':'loudness.py'}], #,'icon_resources': [(0, "static/icon.ico")],
      data_files = find_data_files('','',[
                  'wave_analyze.exe'
                  ]),      
   )
  if os.path.isfile(os.path.join('bin','loudnessPlotter.exe')):
    os.remove(os.path.join('bin','loudnessPlotter.exe'))
  os.rename(os.path.join('bin','loudness.exe'),os.path.join('bin','loudnessPlotter.exe'))  
  zipname=u'loudnessPlotter-%s-win32.zip' %loudness.__version__ 
  zip_folder(os.path.join(os.path.dirname(__file__),'bin'),os.path.join(os.path.abspath(os.path.dirname(__file__)),zipname)) 
