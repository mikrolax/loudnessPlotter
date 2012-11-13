#/usr/bin/python
# -*- coding: utf-8 -*-
__author__='seb@mikrolax.me'

import os
import unittest
import time
import datetime
from string import Template
  
import test.test_generate
import test.test_conformance
import test.test_build
import test.test_doc
#import test.test_setup

#import test.test_download   

import loudness


class Test(unittest.TestCase):
  def setUp(self):
    unittest.TestCase.setUp(self)
    self.testresults=[]
    self.infos={}
    self.infos['version']=loudness.__version__
    self.infos['module']='loudness.py'
    self.infos['package']=None
    self.infos['application name']=None
    self.infos['duration']=None
    self.infos['date']=str(datetime.datetime.now()) 
    self.infos['testnames']=[]
    self.infos['elapsed']=[]
    #result=test('test.test_build')
    loader = unittest.TestLoader()
    runner = unittest.TextTestRunner(verbosity=2)
    begintime=datetime.datetime.now()
    
    self.infos['testnames'].append('test_build')
    suite = loader.loadTestsFromModule(test.test_build)
    t0=datetime.datetime.now()
    result = runner.run(suite)
    elapsed=datetime.datetime.now()-t0
    self.testresults.append(result)
    self.infos['elapsed'].append(str(elapsed))

    self.infos['testnames'].append('test_generate')    
    suite = loader.loadTestsFromModule(test.test_generate)
    t0=datetime.datetime.now()
    result = runner.run(suite)
    elapsed=datetime.datetime.now()-t0
    self.testresults.append(result)
    self.infos['elapsed'].append(str(elapsed))
  
    self.infos['testnames'].append('test_conformance')    
    suite = loader.loadTestsFromModule(test.test_conformance)
    t0=datetime.datetime.now()
    result = runner.run(suite)
    elapsed=datetime.datetime.now()-t0
    self.testresults.append(result)
    self.infos['elapsed'].append(str(elapsed))
    
    self.infos['testnames'].append('test_doc')    
    suite = loader.loadTestsFromModule(test.test_doc)
    t0=datetime.datetime.now()
    result = runner.run(suite)
    elapsed=datetime.datetime.now()-t0
    self.testresults.append(result)
    self.infos['elapsed'].append(str(elapsed))
    
    self.infos['duration']=str(datetime.datetime.now()-begintime)
                      
  def test(self):
    #output JSON result
    import json
    s=json.dumps(self.infos)
    f=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'test','tst_result','infos.json'),'w')
    f.write(str(s))
    idx=0
    for result in self.testresults:
      stringerror=''
      stringfailure=''
      for id,fail in result.failures:
        stringfailure='%s  : %s' %(id,fail)
      for id,fail in result.failures:
        stringerror='%s  : %s' %(id,fail)
      s=json.dumps(dict(tstNb=result.testsRun,failures=stringfailure,errors=stringerror))
      f=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'test','tst_result',self.infos['testnames'][idx]+'.json'),'w')
      f.write(str(s))
      idx=idx+1

  def tearDown(self):
    unittest.TestCase.tearDown(self) 
    writeHTML(self.testresults,self.infos) #from JSON?

        
def writeHTML(testresults,processing):#add details/template/snippet and outfilename
  html=''' <h2> Unit Test Results </h3> <hr>'''
  well_infos=''
  for item in processing.keys():
    if processing[item] != None and isinstance(processing[item],str):
      well_infos+=''' %s : %s <br>''' %(str(item),processing[item])
  if well_infos!='':
    html+='''<div class="well">'''+well_infos+'''</div>'''

  #sumarry table
  idx=0
  html+= '''<table class="table">
            <thead>
              <tr>
                <th>Test name</th>'''
  if 'elapsed' in processing.keys():              
    html+='''<th>duration</th>'''                
  html+='''<th>Test Nb</th>
                <th>Errors</th>
                <th>Failures</th>
              </tr>
            </thead>
            <tbody>'''
  for result in testresults:                       
    if len(result.errors)>0:
      html+='''<tr class="error">  '''
      if 'testnames' in processing.keys():
        html+='''<td> %s </td>''' %processing['testnames'][idx]  
      else:
        html+='''<td> #%s </td>''' %idx
      if 'elapsed' in processing.keys():
        html+='''<td> %s </td>''' %processing['elapsed'][idx]  
      else:
        html+='''<td>  </td>'''  
        
      html+='''<td> %s </td>''' %result.testsRun        
      html+='''<td> %s </td>''' %len(result.errors)  
      html+='''<td> %s </td>''' %len(result.failures)  
      html+='''</tr>'''
    elif len(result.failures)>0:
      html+='''<tr class="warning">  '''
      if 'testnames' in processing.keys():
        html+='''<td> %s </td>''' %processing['testnames'][idx]  
      else:
        html+='''<td> #%s </td>''' %idx
      if 'elapsed' in processing.keys():
        html+='''<td> %s </td>''' %processing['elapsed'][idx]  
      else:
        html+='''<td>  </td>'''  
      html+='''<td> %s </td>''' %result.testsRun        
      html+='''<td> %s </td>''' %len(result.errors)  
      html+='''<td> %s </td>''' %len(result.failures)  
      html+='''</tr>'''
    else:
      html+='''<tr class="success">  '''
      if 'testnames' in processing.keys():
        html+='''<td> %s </td>''' %processing['testnames'][idx]  
      else:
        html+='''<td> #%s </td>''' %idx
      if 'elapsed' in processing.keys():
        html+='''<td> %s </td>''' %processing['elapsed'][idx]  
      else:
        html+='''<td>  </td>''' 
      html+='''<td> %s </td>''' %result.testsRun        
      html+='''<td> %s </td>''' %len(result.errors)  
      html+='''<td> %s </td>''' %len(result.failures)  
      html+='''</tr>'''
    idx=idx+1 
  html+='''</tbody></table>'''
  
  idx=0
  for result in testresults: 
    #html+='''<br> <h3>  %s </h3><hr>''' %processing['testnames'][idx]
    #html+='''Nb Tests : %s ''' %result.testsRun
    #html+='''<br> duration : %s ''' %processing['elapsed'][idx] #or None...
    #html+='''<br> Errors : '''
    #if len(result.errors)==0:
    #  html+=''' <span class="label label-success"> 0 </span>  '''
    #else:
    #  html+=''' <span class="label label-important"> %s </span> ''' %len(result.errors)   
    #html+='''<br> Failures : '''
    #if len(result.failures)==0:
    #  html+=''' <span class="label label-success"> 0 </span>  '''
    #else:
    #  html+=''' <span class="label label-warning"> %s </span> ''' %len(result.failures)  
    #html+=''' <br><br>'''
    if len(result.errors)>0:
      for id,error  in result.errors: 
        html+='''<div class="error"> <strong> %s </strong> <hr>  %s <br></div>''' %(id,error)    
    if len(result.failures)>0:
      for id,error  in result.failures: 
        html+='''<div class="alert"><button type="button" class="close" data-dismiss="alert">×</button> <strong> %s </strong><hr>  %s <br></div>''' %(id,error)  
    idx=idx+1


    

  s = Template(tpl)
  page=s.safe_substitute(content=html)
  f=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'test','tst_result','test.html'),'w')
  f.write(str(page))
  
  s = Template(snippet)
  page=s.safe_substitute(content=html)
  f=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'test','tst_result','test.snippet'),'w')
  f.write(str(page))

snippet='''
  <div class="container">
  $content
  </div>
'''

tpl='''
<!DOCTYPE html>
<html lang="en"><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <title>test</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.1.1/css/bootstrap-combined.min.css" rel="stylesheet">
    <!--UNCOMMENT FOR LOCAL STATIC FILE <link href="bootstrap-combined.min.css" rel="stylesheet">  -->
    
    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements. You (may) have to provide excanvas.min.js... -->
      <!--[if lt IE 9]>
        <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
      <![endif]-->
      <!--[if lte IE 8]><script language="javascript" type="text/javascript" src="excanvas.min.js"></script><![endif]-->
  
  <link rel="shortcut icon" href="favicon.ico">
  </head>
  <body>
  <div class="container">
  $content
  </div>

  <div class="container">
  <footer>
  <hr>
  <p class="pull-right"> <a href="https://github.com/mikrolax/loudnessPlotter">loudnessPlotter</a> - 2012 </p>
  </footer>
  </div>
     
  <script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
  <script src="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.1.1/js/bootstrap.min.js"></script>
  <script src="http://cdnjs.cloudflare.com/ajax/libs/flot/0.7/jquery.flot.min.js"></script>
    <!--UNCOMMENT FOR LOCAL STATIC FILE 
    <script src="jquery.min.js"></script>
    <script src="bootstrap.min.js"></script>
    <script src="jquery.flot.min.js"></script>
    -->   
</body></html>

'''  

def main():
  unittest.main()   
  
if __name__ == '__main__':
  main()
  

