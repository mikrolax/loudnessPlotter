#/usr/bin/python
# -*- coding: utf-8 -*-
__author__='seb@mikrolax.me'

import os
import subprocess
import glob
import sys
import unittest

import loudness #need init.py ?


testfilelist3341=['seq-3341-1-16bit.wav',
    'seq-3341-2-16bit.wav',
    'seq-3341-3-16bit-v02.wav',
    'seq-3341-4-16bit-v02.wav',
    'seq-3341-5-16bit-v02.wav',
    'seq-3341-6-5channels-16bit.wav',
    'seq-3341-6-6channels-WAVEEX-16bit.wav',
    'seq-3341-7_seq-3342-5-24bit.wav',
    'seq-3341-2011-8_seq-3342-6-24bit-v02.wav']


testfilelist3342=['seq-3342-1-16bit.wav',
    'seq-3342-2-16bit.wav',
    'seq-3342-3-16bit.wav',
    'seq-3342-4-16bit.wav',
    'seq-3341-7_seq-3342-5-24bit.wav',
    'seq-3341-2011-8_seq-3342-6-24bit-v02.wav']


testfilelistITU=['1770-2_Comp_23LKFS_1000Hz_2ch.wav',
  '1770-2_Comp_23LKFS_2000Hz_2ch.wav', 
  '1770-2_Comp_23LKFS_10000Hz_2ch.wav',
  '1770-2_Comp_23LKFS_ChannelCheckCentre.wav',
  '1770-2_Comp_23LKFS_500Hz_2ch.wav', 
  '1770-2_Comp_24LKFS_ChannelCheckLeft.wav',
  '1770-2_Comp_24LKFS_ChannelCheckLFEs.wav',
  '1770-2_Comp_24LKFS_ChannelCheckLs.wav', 
  '1770-2_Comp_24LKFS_ChannelCheckRight.wav',
  '1770-2_Comp_24LKFS_ChannelCheckRs.wav',
  '1770-2_Comp_24LKFS_SummingTest.wav', 
  '1770-2_Comp_AbsGateTest.wav', 
  '1770-2_Comp_RelGateTest.wav', 
  '1770-2_Comp_18LKFS_FrequencySweep.wav', 
  '1770-2_Comp_23LKFS_25Hz_2ch.wav', 
  '1770-2_Comp_23LKFS_100Hz_2ch.wav',
  '1770-2_Comp_23LKFS_ChannelCheckLeft.wav',
  '1770-2_Comp_23LKFS_ChannelCheckLFEs.wav',
  '1770-2_Comp_23LKFS_ChannelCheckLs.wav', 
  '1770-2_Comp_23LKFS_ChannelCheckRight.wav',
  '1770-2_Comp_23LKFS_ChannelCheckRs.wav', 
  '1770-2_Comp_23LKFS_SummingTest.wav',
  '1770-2_Comp_24LKFS_25Hz_2ch.wav', 
  '1770-2_Comp_24LKFS_100Hz_2ch.wav',
  '1770-2_Comp_24LKFS_500Hz_2ch.wav',
  '1770-2_Comp_24LKFS_1000Hz_2ch.wav',
  '1770-2_Comp_24LKFS_2000Hz_2ch.wav',
  '1770-2_Comp_24LKFS_10000Hz_2ch.wav', 
  '1770-2_Comp_24LKFS_ChannelCheckCentre.wav']

ITU_awaited=[-23.0,
  -23, 
  -23.0,
  -23.0,
  -23.0, 
  -24.0,
  -24.0,
  -24.0, 
  -24.0,
  -24.0,
  -24.0, 
  -24.0, #'1770-2_Comp_AbsGateTest.wav', 
  -24.0, #'1770-2_Comp_RelGateTest.wav', 
  -18.0, 
  -23.0, 
  -23.0,
  -23.0,
  -23.0,
  -23.0, 
  -23.0,
  -23.0, 
  -23.0,
  -24.0, 
  -24.0,
  -24.0,
  -24.0,
  -24.0,
  -24.0, 
  -24.0]

class ConformanceTest(unittest.TestCase):
  def setUp(self):
    unittest.TestCase.setUp(self)
    self.ebu_tst_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'testfiles','ebu-loudness-test-setv03')
    self.itu_tst_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'testfiles','ITUBS1770_Compliance')
    self.folderout=os.path.join(os.path.dirname(os.path.abspath(__file__)),'tst_result')
    
    #self.testfilelist3341    
       
  '''def test_ebu(self):
    self.ebu_plotter.analyse()
    self.assertAlmostEqual(float(self.ebu_plotter.loudnessdata['seq-3341-1-16bit.wav']['I'][0]),-23.0,1)   
    self.assertAlmostEqual(float(self.ebu_plotter.loudnessdata['seq-3341-2-16bit.wav']['I'][0]),-33.0,1)
    self.assertAlmostEqual(float(self.ebu_plotter.loudnessdata['seq-3341-3-16bit-v02.wav']['I'][0]),-23.0,1)
    self.assertAlmostEqual(float(self.ebu_plotter.loudnessdata['seq-3341-4-16bit-v02.wav']['I'][0]),-23.0,1)
    self.assertAlmostEqual(float(self.ebu_plotter.loudnessdata['seq-3341-5-16bit-v02.wav']['I'][0]),-23.0,1)
    self.assertAlmostEqual(float(self.ebu_plotter.loudnessdata['seq-3341-6-5channels-16bit.wav']['I'][0]),-23.0,1)
    self.assertAlmostEqual(float(self.ebu_plotter.loudnessdata['seq-3341-7_seq-3342-5-24bit.wav']['I'][0]),-23.0,1)
    self.assertAlmostEqual(float(self.ebu_plotter.loudnessdata['seq-3341-2011-8_seq-3342-6-24bit-v02.wav']['I'][0]),-23.0,1)
    self.assertAlmostEqual(float(self.ebu_plotter.loudnessdata['seq-3341-6-6channels-WAVEEX-16bit.wav']['I'][0]),-23.0,1)
  '''
  
  def test_tech3341_1(self):
    testfile=testfilelist3341[0]
    plotter=loudness.LoudnessPlotter([os.path.join(self.ebu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    #outpout=    write(yield?+'.html')
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),-23.0,1)   

  def test_tech3341_2(self):
    testfile=testfilelist3341[1]
    plotter=loudness.LoudnessPlotter([os.path.join(self.ebu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),-33.0,1)   

  def test_tech3341_3(self):
    testfile=testfilelist3341[2]
    plotter=loudness.LoudnessPlotter([os.path.join(self.ebu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),-23.0,1)   

  def test_tech3341_4(self):
    testfile=testfilelist3341[3]
    plotter=loudness.LoudnessPlotter([os.path.join(self.ebu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),-23.0,1)   

  def test_tech3341_5(self):
    testfile=testfilelist3341[4]
    plotter=loudness.LoudnessPlotter([os.path.join(self.ebu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),-23.0,1)   

  def test_tech3341_6(self):
    testfile=testfilelist3341[5]
    plotter=loudness.LoudnessPlotter([os.path.join(self.ebu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),-23.0,1)   

  def test_tech3341_6_bis(self):
    testfile=testfilelist3341[6]
    plotter=loudness.LoudnessPlotter([os.path.join(self.ebu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),-23.0,1)   

  def test_tech3341_7(self):
    testfile=testfilelist3341[7]
    plotter=loudness.LoudnessPlotter([os.path.join(self.ebu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),-23.0,1)   

  def test_tech3341_8(self):
    testfile=testfilelist3341[8]
    plotter=loudness.LoudnessPlotter([os.path.join(self.ebu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),-23.0,1)   





  def test_tech3342_1(self):
    testfile=testfilelist3342[0]
    plotter=loudness.LoudnessPlotter([os.path.join(self.ebu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['LRA']),10.0,1)   


  def test_tech3342_2(self):
    testfile=testfilelist3342[1]
    plotter=loudness.LoudnessPlotter([os.path.join(self.ebu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['LRA']),5.0,1)   

  def test_tech3342_3(self):
    testfile=testfilelist3342[2]
    plotter=loudness.LoudnessPlotter([os.path.join(self.ebu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['LRA']),20.0,1)   
  
  def test_tech3342_4(self):
    testfile=testfilelist3342[3]
    plotter=loudness.LoudnessPlotter([os.path.join(self.ebu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['LRA']),15.0,1)   

  def test_tech3342_5(self):
    testfile=testfilelist3342[4]
    plotter=loudness.LoudnessPlotter([os.path.join(self.ebu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['LRA']),5.0,1)   

  def test_tech3342_6(self):
    testfile=testfilelist3342[5]
    plotter=loudness.LoudnessPlotter([os.path.join(self.ebu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['LRA']),15.0,1)   




  def test_itu_1(self):
    testfile=testfilelistITU[0]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[0],1)   
  def test_itu_2(self):
    testfile=testfilelistITU[1]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[1],1)   
  def test_itu_3(self):
    testfile=testfilelistITU[2]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[2],1)   
  def test_itu_4(self):
    testfile=testfilelistITU[3]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[3],1)   
  def test_itu_5(self):
    testfile=testfilelistITU[4]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[4],1)   
  def test_itu_6(self):
    testfile=testfilelistITU[5]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[5],1)   
  def test_itu_7(self):
    testfile=testfilelistITU[6]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[6],1)   
  def test_itu_8(self):
    testfile=testfilelistITU[7]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[7],1)   
  def test_itu_9(self):
    testfile=testfilelistITU[8]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[8],1)   
  def test_itu_10(self):
    testfile=testfilelistITU[9]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[9],1)   
  def test_itu_11(self):
    testfile=testfilelistITU[10]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[10],1)   
  def test_itu_12(self):
    testfile=testfilelistITU[11]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[11],1)   
  def test_itu_13(self):
    testfile=testfilelistITU[12]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[12],1)   
  def test_itu_14(self):
    testfile=testfilelistITU[13]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[13],1)   
  def test_itu_15(self):
    testfile=testfilelistITU[14]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[14],1)   
  def test_itu_16(self):
    testfile=testfilelistITU[15]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[15],1)   
  def test_itu_17(self):
    testfile=testfilelistITU[17]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[17],1)   
  def test_itu_18(self):
    testfile=testfilelistITU[0]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[0],1)   
  def test_itu_19(self):
    testfile=testfilelistITU[18]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[18],1)   
  def test_itu_20(self):
    testfile=testfilelistITU[19]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[19],1)   
  def test_itu_21(self):
    testfile=testfilelistITU[20]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[20],1)   
  def test_itu_22(self):
    testfile=testfilelistITU[21]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[21],1)   
  def test_itu_23(self):
    testfile=testfilelistITU[22]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[22],1)   
  def test_itu_24(self):
    testfile=testfilelistITU[23]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[23],1)   
  def test_itu_25(self):
    testfile=testfilelistITU[24]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[24],1)   
  def test_itu_26(self):
    testfile=testfilelistITU[25]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[25],1)   
  def test_itu_27(self):
    testfile=testfilelistITU[26]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[26],1)   
  def test_itu_28(self):
    testfile=testfilelistITU[27]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[27],1)   
  def test_itu_29(self):
    testfile=testfilelistITU[28]
    plotter=loudness.LoudnessPlotter([os.path.join(self.itu_tst_path,testfile)],self.folderout)
    plotter.analyse()
    self.assertAlmostEqual(float(plotter.loudnessdata[testfile]['I'][0]),ITU_awaited[28],1)   


if __name__ == '__main__':
  unittest.main()

   
