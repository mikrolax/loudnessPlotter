#/usr/bin/python
# -*- coding: utf-8 -*-
__author__='seb@mikrolax.me'

import subprocess
import os

import unittest

class SourceDocTest(unittest.TestCase):
  def setUp(self):
    unittest.TestCase.setUp(self)
    unittest.TestCase.verbose=2
    testpath=os.path.dirname(os.path.abspath(__file__))
    self.options='-f -F -H loudnessPlotter -A seb@mikrolax.me -V 0.1 ' #-R -f 
    basedir=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    self.packagedir=basedir
    self.outputdir=os.path.join(self.packagedir,'doc','sphinx')
    self.pathnames=[] #to be excluded
    self.sourcedir= self.outputdir    

  def test_step1_generate_sphinx(self):
    cmd='sphinx-apidoc %s -o %s %s %s' %(self.options,self.outputdir,self.packagedir,self.pathnames)
    returnCode=subprocess.call(cmd,shell=True)
    self.assertEqual(returnCode,0)     
    import fileinput
    for line in fileinput.FileInput(os.path.join(self.outputdir,'conf.py'), inplace = 1): 
      line=line.replace("#sys.path.insert(0, os.path.abspath('.'))", "sys.path.insert(0,'"+os.path.dirname(self.packagedir)+"')")
      print line,
  
  def test_step2_build_sphinx_html(self):
    options='-q -a '# warning as error, quiet mode
    builddir= os.path.join(self.packagedir,'doc','source_doc')
    #filenames=[]
    cmd='sphinx-build %s %s %s ' %(options,self.sourcedir,builddir)
    returnCode=subprocess.call(cmd,shell=True)
    self.assertEqual(returnCode,0)
  
  def test_step3_build_sphinx_json(self): #also try singlehtml?
    options='-a -q '# -q -W 
    builddir= os.path.join(self.packagedir,'test','tst_result','sphinx-json')
    #filenames=[]
    cmd='sphinx-build -b json %s %s %s ' %(options,self.sourcedir,builddir)
    returnCode=subprocess.call(cmd,shell=True)
    self.assertEqual(returnCode,0)
    #now generate your own with toc/body from index/modules ?
       
  def tearDown(self):
     unittest.TestCase.tearDown(self)     

if __name__ == '__main__':
  unittest.main()        
