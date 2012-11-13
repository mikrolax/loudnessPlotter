#/usr/bin/python
# -*- coding: utf-8 -*-
__author__='seb@mikrolax.me'

import os
import subprocess
import glob
import sys
import unittest

import loudness

class HtmlGenerationTest(unittest.TestCase):
  def setUp(self):
    unittest.TestCase.setUp(self)
    tst_file=os.path.join(os.path.dirname(os.path.abspath(__file__)),'testfiles','seq-3341-1-16bit.wav')
    tst_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)),'testfiles')

    ebu_tst_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'testfiles','ebu-loudness-test-setv03')
    itu_tst_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'testfiles','ITUBS1770_Compliance')

    #make it if it does not exist
    self.folderout=os.path.join(os.path.dirname(os.path.abspath(__file__)),'tst_result')
     
    self.tst_file=[tst_file]
    self.tst_folder=glob.glob(os.path.join(tst_folder,'*.wav'))
    self.ebur128lst=glob.glob(os.path.join(ebu_tst_path,'*.wav'))
    self.itu1770lst=glob.glob(os.path.join(itu_tst_path,'*.wav'))
             
  def test_generate_default_onefile(self):
    """ generate_default_onefile """  
    plotter=loudness.LoudnessPlotter(self.tst_file,self.folderout)
    plotter.process()
    
  def test_generate_default_multifile(self):
    """ generate_default_multifile """      
    plotter=loudness.LoudnessPlotter(self.tst_folder,self.folderout)
    plotter.process()

  '''def test_generate_with_options(self):
    plotter=loudness.LoudnessPlotter(self.tst_folder,self.folderout)
    plotter.autoscale=False
    plotter.template=os.path.join(os.path.dirname(os.path.abspath(__file__)),'loudnessPlotter','template_doc.html')
    plotter.outfilename='generate_with_options.html'
    plotter.process()    
    #rewrite with another template?  
    #plotter.process()'''

  def test_generate_ebur128(self):
    plotter=loudness.LoudnessPlotter(self.ebur128lst,self.folderout)
    plotter.autoscale=False
    plotter.template=os.path.join(os.path.dirname(os.path.abspath(__file__)),'loudnessPlotter','template_doc.html')
    plotter.outfilename='tst_ebu.html'
    plotter.process()    
    #rewrite with another template?  
    plotter.template=os.path.join(os.path.dirname(os.path.abspath(__file__)),'loudnessPlotter','template.snippet')
    plotter.outfilename='tst_ebu.snippet'
    plotter.write()

  def test_generate_itu1770(self):
    plotter=loudness.LoudnessPlotter(self.itu1770lst,self.folderout)
    plotter.autoscale=False
    plotter.template=os.path.join(os.path.dirname(os.path.abspath(__file__)),'loudnessPlotter','template_doc.html')
    plotter.outfilename='tst_itu.html'
    plotter.process()    
    #rewrite with another template?  
    plotter.template=os.path.join(os.path.dirname(os.path.abspath(__file__)),'loudnessPlotter','template.snippet')
    plotter.outfilename='tst_itu.snippet'
    plotter.write()
          
  def tearDown(self):
     unittest.TestCase.tearDown(self) 
      
if __name__ == '__main__':
  unittest.main()   
  
  
