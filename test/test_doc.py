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
    self.options='-f -F -H loudnessPlotter -A seb@mikrolax.me ' #-R -V 0.1  
    basedir=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    self.packagedir=basedir
    self.outputdir=os.path.join(self.packagedir,'doc','sphinx')
    self.pathnames=[] #to be excluded
    self.sourcedir= self.outputdir    

  def test_step1_generate_sphinx(self):
    cmd='sphinx-apidoc %s -o %s %s %s' %(self.options,self.outputdir,self.packagedir,self.pathnames)
    print cmd
    returnCode=subprocess.call(cmd,shell=True)
    self.assertEqual(returnCode,0)     
    import fileinput
    for line in fileinput.FileInput(os.path.join(self.outputdir,'conf.py'), inplace = 1): 
      #line=line.replace("#sys.path.insert(0, os.path.abspath('.'))", "sys.path.insert(0,'"+os.path.dirname(self.packagedir)+"')")
      line=line.replace("#sys.path.insert(0, os.path.abspath('.'))", "sys.path.insert(0,'"+self.packagedir+"')")
      print line,
  
  '''def test_step2_build_sphinx_html(self): # or try a make...
    """ test html generation with sphinx calling sphinx-build """
    options='-a -W'# -q   warning as error, quiet mode
    builddir= os.path.join(self.packagedir,'doc','source_doc')
    #filenames=[]
    doctree=os.path.join(self.outputdir,'_build','doctrees')
    cmd='sphinx-build -b html -d %s %s %s %s ' %(doctree,options,self.sourcedir,builddir)
    print cmd
    returnCode=subprocess.call(cmd,shell=True)
    self.assertEqual(returnCode,0)'''

  def test_step3_build_sphinx_html(self): 
    """ test html generation with sphinx calling make/make.bat """
    options='-a -W'# -q   warning as error, quiet mode
    #builddir= os.path.join(self.packagedir,'doc','source_doc')
    import sys
    if sys.platform=='win32':
      cmd='cd %s & make.bat html ' %(self.sourcedir)      
    else:
      cmd='cd %s ;make html ' %(self.sourcedir)      
    print cmd
    returnCode=subprocess.call(cmd,shell=True)
    self.assertEqual(returnCode,0)

  def test_step4_build_sphinx_pdf(self): 
    """ test pdf generation with sphinx calling make/make.bat """
    options='-a -q -W'# -q   warning as error, quiet mode
    #builddir= os.path.join(self.packagedir,'doc','source_doc')
    import sys
    if sys.platform=='win32':
      cmd='cd %s & make.bat latexpdf ' %(self.sourcedir)      
    else:
      cmd='cd %s ;make html latexpdf ' %(self.sourcedir) #install texlive package for this      
    print cmd
    returnCode=subprocess.call(cmd,shell=True)
    self.assertEqual(returnCode,0)
         
  '''def test_step6_build_sphinx_json(self):
    """ test sphinx json generation (for future use) """
    options='-a -q -W'# -q -W 
    builddir= os.path.join(self.packagedir,'test','tst_result','sphinx-json')
    #filenames=[]
    cmd='sphinx-build -b json %s %s %s ' %(options,self.sourcedir,builddir)
    print cmd
    returnCode=subprocess.call(cmd,shell=True)
    self.assertEqual(returnCode,0)
    #now generate your own with toc/body from index/modules ?'''
       
  def tearDown(self):
     unittest.TestCase.tearDown(self)     

if __name__ == '__main__':
  unittest.main()        
