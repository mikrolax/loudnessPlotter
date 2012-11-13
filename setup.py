#/usr/bin/python
# -*- coding: utf-8 -*-

#import distribute_setup
#distribute_setup.use_setuptools()

import os
from distutils.core import setup,Extension,Command

import sys
if sys.platform=='win32':
  try:
    import py2exe
  except:
    print 'Cannot import py2exe'

  
__version__     =__import__('loudness').__version__
__author__      =__import__('loudness').__author__
__author_email__=__import__('loudness').__author_email__
__url__         =__import__('loudness').__url__
__download_url__=__import__('loudness').__download_url__


class Clean(Command):
    description = "custom clean command that forcefully removes dist & build directories"
    user_options = []
    def initialize_options(self):
        self.cwd = None
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        import shutil
        shutil.rmtree(os.path.join(os.getcwd(),'dist'))
        shutil.rmtree(os.path.join(os.getcwd(),'build'))
        #shutil.rmtree(os.path.join(os.getcwd(),'MANIFEST'))
        
class Test(Command):
    description = "pass loudnessPlotter testsuite"
    user_options = []
    def initialize_options(self):
        self.cwd = None
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        #os.system('rm -rf ./build ./dist') #use subprocess
        import subprocess
        cmd='python test.py'
        returnCode=subprocess.call(cmd,shell=True)
        self.assertEqual(returnCode,0)


class TstBuild(Command):
    description = "pass build test"
    user_options = []
    def initialize_options(self):
        self.cwd = None
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        #os.system('rm -rf ./build ./dist') #use subprocess
        import subprocess
        cmd='python %s' %os.path.join('test','test_build.py')
        returnCode=subprocess.call(cmd,shell=True)
        assert returnCode==0, 'test_build return error: %s' % returnCode

class TstSetup(Command):
    description = "pass build test"
    user_options = []
    def initialize_options(self):
        self.cwd = None
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        #os.system('rm -rf ./build ./dist') #use subprocess
        import subprocess
        cmd='python %s' %os.path.join('test','test_setup.py')
        returnCode=subprocess.call(cmd,shell=True)
        #assert returnCode==0, 'test_build return error: %s' % returnCode
        

class SphinxDoc(Command):
    description = "pass build test"
    user_options = []
    def initialize_options(self):
        self.cwd = None
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        import subprocess
        cmd='python %s' %os.path.join('test','test_doc.py')
        returnCode=subprocess.call(cmd,shell=True)
        assert returnCode==0


'''wave_analyze=Extension('wave_analyze',
                   include_dirs = [os.path.join('ebu_r128','includes')],
                   sources = [os.path.join('ebu_r128','src','itu-1770-filter.c'),
                              os.path.join('ebu_r128','src','ebu_r128.c'),
                              os.path.join('ebu_r128','examples','wave','wave.c'),
                              os.path.join('ebu_r128','examples','wave','main.c')])'''


setup(
    cmdclass={'clean_all': Clean,'test':Test,'tst_setup':TstSetup,'test_build':TstBuild,'sphinx_doc':SphinxDoc}, #'test':Test,
    name        ='loudnessplotter',
    version     =__version__,
    author      =__author__,
    author_email=__author_email__,
    url         =__url__,
    download_url=__download_url__,
    license='GNU GPLv3',
    long_description=open('README.md').read(),
    classifiers=[
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent',
    'Programming Language :: C',
    'Programming Language :: Python',
    'Topic :: Multimedia :: Sound/Audio',
    'Topic :: Multimedia :: Sound/Audio :: Analysis',
    'Topic :: Scientific/Engineering :: Visualization'],   

    #ext_package='ebu_r128',    
    #ext_modules=[wave_analyze], 
        
    py_modules=['loudness','test'], 

    package_data = {
        '': ['template_example.html'],
        'doc': ['*.md'],
        'ebu_r128': ['LICENSE','README','API' ]
    },
    #test_suite='tests'
    #package_data={'ebu_r128': ['LICENSE','README','API' ]},    
    data_files=[('', ['template_example.html']),
                ('', ['wave_analyze.exe']), #not really....??
                ('ebu_r128', ['example/*.c']),
                ('ebu_r128', ['src/*.c']),
                ('ebu_r128', ['include/*.h'])],
    
    #for py2exe
    options ={'py2exe': {'bundle_files': 1,'dist_dir':'portable/'}},
    zipfile = None,
    console=[{'script':'loudness.py'}]               
 )

