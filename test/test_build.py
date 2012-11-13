#/usr/bin/python
# -*- coding: utf-8 -*-
__author__='seb@mikrolax.me'

import os
import subprocess
import sys
import unittest


class ManualBuildTest(unittest.TestCase):
  def setUp(self):
    unittest.TestCase.setUp(self)
    #clean/remove file...
    try:
      #remove .o file...
      if sys.platform == 'win32' :    
        print 'remove %s' %os.path.abspath(os.path.join('ebu_r128','wave_analyze.exe'))
        os.remove( os.path.abspath(os.path.join('ebu_r128','wave_analyze.exe')) ) #relative from package root folder
      else:
        print 'remove %s' %os.path.abspath(os.path.join('ebu_r128','wave_analyze'))
        os.remove(os.path.join('ebu_r128','wave_analyze')) #relative from package root folder
    except:
      print 'cannot find/delete wave_analyze binarie'
      
  def test_build_manual(self):
    """ test manually build of wave_analyze bin and copy (update) it. """
    #os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'loudnessPlotter'))
    if sys.platform == 'win32' :
      cmd='cd ebu_r128 & mingw32-make clean & mingw32-make wave_analyze & copy wave_analyze.exe ..\ & cd ..'
    else:
      cmd='cd ebu_r128/; make clean; make wave_analyze; cp wave_analyze ../.; cd ..'
      #also try mingw?
    returnCode=subprocess.call(cmd,shell=True)
    self.assertEqual(returnCode,0)


  #also add test_setup module??
  #def test_build_setup(self):
  
  def tearDown(self):
     unittest.TestCase.tearDown(self) 
     
     
if __name__ == '__main__':
  unittest.main() 
