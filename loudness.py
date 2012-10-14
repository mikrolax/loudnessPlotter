#/usr/bin/python
# -*- coding: utf-8 -*-

from string import Template
import os
import subprocess
import glob

__version__='0.1.0'
__author__='seb@mikrolax.me'


tpl_CDN='''<!DOCTYPE html>
<html lang="en"><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <title>loudnessPlotter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="plot loudness mesurement">
    <meta name="author" content="seb 'mikrolax'">
    <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.1.1/css/bootstrap-combined.min.css" rel="stylesheet">

    <style>
      body {
        padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
      }
    </style>
    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
  <!--[if lte IE 8]><script language="javascript" type="text/javascript" src="excanvas.min.js"></script><![endif]-->
    <link rel="shortcut icon" href="favicon.ico">
  </head>
  <body>

    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <a class="brand" href="#">loudnessPlotter</a>
          <div class="nav-collapse collapse">
            <ul class="nav">
              <!-- <li class="active"><a href="https://github.com/mikrolax/loudnessPlotter/issues">Bugs</a></li> -->
            </ul>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>
    
  <div class="container">
    <h3> $filename </h3><hr>
      $htmlstats
      <div id="placeholder" style="width:900px;height:450px"></div>
      
      <h4>Legend</h4> 
      <dl class="dl-horizontal">
        <dt> Y axis value : </dt><dd> LUFS </dd>
        <dt> X axis value :</dt><dd> seconds </dd>
      </dl>
      </div>
            
    <footer>
      <hr>
      <p>report bugs!</p>
      <p class="pull-right"> <a href="https://github.com/mikrolax/loudnessPlotter">loudnessPlotter</a> - 2012 </p>
    </footer>
  </div>
  
  <script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
  <script src="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.1.1/js/bootstrap.min.js"></script>
  <script src="http://cdnjs.cloudflare.com/ajax/libs/flot/0.7/jquery.flot.min.js"></script>  
  <script language="javascript" type="text/javascript">
  $(document).ready(function() {
  $.plot($("#placeholder"), $datas,$options);
  });
  </script>

  </body></html>
'''

tpl_multi_fromCDN='''<!DOCTYPE html>
<html lang="en"><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <title>loudnessPlotter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="plot loudness mesurement">
    <meta name="author" content="seb 'mikrolax'">
    <!-- Le styles -->
    <style>
      body {
        padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
      }
    </style>
    <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.1.1/css/bootstrap-combined.min.css" rel="stylesheet">
    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
  <!--[if lte IE 8]><script language="javascript" type="text/javascript" src="excanvas.min.js"></script><![endif]-->
    <link rel="shortcut icon" href="favicon.ico">

  </head>
  <body>

    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <a class="brand" href="#">loudnessPlotter</a>
          <div class="nav-collapse collapse">
            <ul class="nav">
              <!-- <li class="active"><a href="#">Home</a></li> -->
            </ul>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>
    
  <div class="container">
  
  $tabbedplaceholder
  
  <footer>
  <hr>
  <p class="pull-right"> <a href="https://github.com/mikrolax/loudnessPlotter">loudnessPlotter</a> - 2012 </p>
  </footer>
  </div>
  <script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
  <script src="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.1.1/js/bootstrap.min.js"></script>
  <script src="http://cdnjs.cloudflare.com/ajax/libs/flot/0.7/jquery.flot.min.js"></script>
<script language="javascript" type="text/javascript">
$(document).ready(function() {
$plots
});
</script>

  </body></html>
'''

def writeHTML(loudnessdata,htmlout):
  """    Write a single self-contained HTML page with graph. """
  print 'writeHTML %s' %os.getcwd()
  fout=open(htmlout+'.html','w')
  s = Template(tpl_CDN)
  htmlstats=HTMLstats(stats(loudnessdata))

  datas=[] # getData(self.loudnessdata)
  M=[]
  S=[]
  I=[]
  idx_m=0
  idx_s=0
  idx_i=0  
  for val in loudnessdata['M']:
    M.append([idx_m*2*0.1,loudnessdata['M'][idx_m]])
    idx_m+=1
  for val in loudnessdata['S']:
    S.append([idx_s*0.1,loudnessdata['S'][idx_s]])
    idx_s+=1
  for val in loudnessdata['M']:
    I.append([idx_i*2*0.1,loudnessdata['I'][0]]) 
    idx_i+=1  
  Mdict={}
  Mdict['label']='Momentary'
  Mdict['data']=M
  Sdict={}
  Sdict['label']='Short-Term'
  Sdict['data']=S  
  Idict={}
  Idict['label']='Integrated'
  Idict['data']=I  
  datas.append(Mdict)
  datas.append(Sdict)
  datas.append(Idict)
  options='''{}'''
  page=s.safe_substitute(filename=os.path.basename(htmlout),htmlstats=htmlstats,datas=datas,options=options) #,options=options
  print 'write %s' %htmlout+'.html'
  fout.write(str(page))
  
def stats(loudnessdata):
  """ get min/max/average value of M,S,(I) value. Return a dictionnary  """
  stats={}
  stats['M']={}
  stats['S']={}
  idx=0
  maxVal=-100
  minVal=0
  avgVal=0
  for item in loudnessdata['M']:
    data=float(loudnessdata['M'][idx])
    if data > maxVal:
      maxVal=data
    elif data < minVal:
      minVal=data
    avgVal+=data/len(loudnessdata['M'])     
    idx+=1  
  stats['M']['min']=minVal
  stats['M']['max']=maxVal
  stats['M']['avg']='{0:.2f}'.format(avgVal)    
  idx=0
  maxVal=-100
  minVal=0
  avgVal=0
  for item in loudnessdata['S']:
    data=float(loudnessdata['S'][idx])
    if data > maxVal:
      maxVal=data
    elif data < minVal:
      minVal=data
    avgVal+=data/len(loudnessdata['S'])     
    idx+=1  
  stats['S']['min']=minVal
  stats['S']['max']=maxVal
  stats['S']['avg']='{0:.2f}'.format(avgVal)   
  stats['I']=float(loudnessdata['I'][0])
  #import pprint
  #pprint.pprint(stats)
  return stats

def parseLoudnessLog(filepath):
  """ return dict : { 'M' : [val,val2],
                      'S' : [value,value],
                      'I' : [integratedvalue]}
      value are string reprensenting LUFS value                
  """
  loudnessdata={}
  loudnessdata['M']=[]
  loudnessdata['S']=[]
  loudnessdata['I']=[]
  key=''
  lines = open(filepath,'r').readlines()
  for line in lines:
    if 'ebu_mode=s' in line:  
      print 'getting S value'
      key='S'
    if 'ebu_mode=m' in line:  
      print 'getting M value'    
      key='M'
    if 'ebu_mode=i' in line:  
      print 'getting I value'    
      key='I'      
    if 'Lk=' in line:
      data=line.rsplit()[1]
      loudnessdata[key].append(data.rsplit('Lk=')[1])  
  return loudnessdata   
  
def HTMLstats(stats):
  """ return html from M,S,I stats dictionnary (returned by stats())  """
  html='''<dl class="dl-horizontal">'''
  s=m=i=''   
  for key in stats.keys():
    if key=='M':
      m='''<dt>Momentary max</dt> <dd>'''+str(stats['M']['max'])+'''</dd>'''
      m+='''<dt>Momentary min</dt> <dd>'''+str(stats['M']['min'])+'''</dd>'''
      m+='''<dt>Momentary average</dt> <dd>'''+str(stats['M']['avg'])+'''</dd>'''
    elif key=='S':
      s='''<dt>Short-term max</dt> <dd>'''+str(stats['S']['max'])+'''</dd>'''
      s+='''<dt>Short-term min</dt> <dd>'''+str(stats['S']['min'])+'''</dd>'''
      s+='''<dt>Short-term average</dt> <dd>'''+str(stats['S']['avg'])+'''</dd>'''
    elif key=='I':
      i='''<dt>Integrated</dt> <dd>'''+str(stats['I'])+'''</dd>'''
    else:
      pass
  html+=m+s+i    
  html+='''</dl>'''
  return html  


class LoudnessPlotter(object):
  """ base class for launching executable, parse log and write output HTML file """
  def __init__(self,filelist,outpath): #add OneFile=True
    """ init some self used value """
    self.filelist=filelist
    self.outpath=outpath
    self.loudnessdata={}
    print self.filelist
    print self.outpath
    self.toolspath=os.path.abspath(os.path.dirname(__file__))   
    self.wavtoolpath=os.path.join(self.toolspath,'wave_analyze')

  def analyse(self):
    """ launch wave_analyze executable on each file of self.filelist putting stdout in a file """
    for item in self.filelist:
      logfile=item+'_loudness.txt'
      if os.path.isfile(logfile):
        print 'remove %s' %logfile
        os.remove(logfile)
      for ebu_mode in ['m','s','i']:
        print 'ebu mode %s' %ebu_mode
        log=open(logfile,'a')
        log.write('ebu_mode=%s\n' %ebu_mode)
        log.flush()
        cmd=self.wavtoolpath+' '+item+' '+ebu_mode
        subprocess.call(cmd,stdout=log,shell=True)
        log.close()

  def process(self):
    """ base function to parse and write HTML base on internal config """
    if len(self.filelist)==0:
      print 'No file to process. Abort'
      return 1
    self.analyse()
    for f in self.filelist:
      self.loudnessdata[os.path.basename(f)]=parseLoudnessLog(f+'_loudness.txt')
    if len(self.filelist)==1:
      self.writeIndividual()
    else :  
      self.write() 
        
  def writeIndividual(self):
    """ write single HTML file for an individual file"""
    for key in self.loudnessdata.keys():
      writeHTML(self.loudnessdata[key],os.path.join(self.outpath,key))

  def write(self):
    """ write single HTML file for a list of file"""  
    print 'loudnessplot::process'
  
    tabbedplaceholder='''<div class="tabbable"> 
                        <!-- <ul class="nav nav-tabs"> -->
                        <ul class="nav nav-pills">
                        '''    
    i=0                    
    for f in self.loudnessdata.keys(): 
      name=os.path.splitext(os.path.basename(f))[0]
      if i==0:
        tabbedplaceholder+='''<li class="active"><a href="#'''+name+'''" data-toggle="tab">'''+name+'''</a></li>
        '''      
      else:
        tabbedplaceholder+='''<li><a href="#'''+name+'''" data-toggle="tab">'''+name+'''</a></li>
        '''
      i+=1      
    tabbedplaceholder+='''</ul><hr>
    '''
    tabbedplaceholder+='''<div class="tab-content">
    '''  
    j=0
    for tab in self.loudnessdata.keys():
      name=os.path.splitext(os.path.basename(tab))[0]   
      if j==0:
        tabbedplaceholder+='''<div class="tab-pane active" id="'''+name+'''"> 
        ''' 
      else:
        tabbedplaceholder+='''<div class="tab-pane" id="'''+name+'''">
        ''' 
      tabbedplaceholder+=HTMLstats(stats(self.loudnessdata[tab]))+'''
      <div id="'''+'placeholder'+name+'''" style="width:850px;height:450px"></div>
      <h4>Legend</h4> 
      <dl class="dl-horizontal">
        <dt> Y axis value : </dt><dd> LUFS </dd>
        <dt> X axis value :</dt><dd> seconds </dd>
      </dl>
      </div>'''  
      j+=1
    tabbedplaceholder+='''</div>
    </div>
    '''    
    plots=''
    for item in self.loudnessdata.keys():
      datas=[] #getData(self.loudnessdata[item])
      M=[]
      S=[]
      I=[]
      idx_m=0
      idx_s=0
      idx_i=0
      for val in self.loudnessdata[item]['M']:
        M.append([idx_m*2*0.1,self.loudnessdata[item]['M'][idx_m]])
        idx_m+=1
      for val in self.loudnessdata[item]['S']:
        S.append([idx_s*0.1,self.loudnessdata[item]['S'][idx_s]])
        idx_s+=1  
      for val in self.loudnessdata[item]['M']:
        I.append([idx_i*2*0.1,self.loudnessdata[item]['I'][0]],) 
        idx_i+=1
      Mdict={}
      Mdict['label']='Momentary'
      Mdict['data']=M
      Sdict={}
      Sdict['label']='Short-Term'
      Sdict['data']=S  
      Idict={}
      Idict['label']='Integrated'
      Idict['data']=I  
      datas.append(Mdict)
      datas.append(Sdict)
      datas.append(Idict)
      options='''{}'''
      name=os.path.splitext(os.path.basename(item))[0]
      plots+='''$.plot($("#placeholder'''+name+'''"), '''+str(datas)+''','''+options+''');             
             '''
    s = Template(tpl_multi_fromCDN)
    page=s.safe_substitute(tabbedplaceholder=tabbedplaceholder,plots=plots) #,options=options
    print 'write %s' %os.path.join(self.outpath,'loudness.html')
    open(os.path.join(self.outpath,'loudness.html'),'w').write(page)  

def cli():
  """ Simple command line interface. Process file or path, based on input args """
  import sys
  msg=''' loudnessplotter : analyse and plot loudness in HTML\n usage: python loudnessplotter.py [inpath] [outpath]'''
  if len(sys.argv) > 1:
    pass
  else:
    print msg
    return 1      
  inpath=os.path.abspath(sys.argv[1])
  outpath=os.path.abspath(sys.argv[2])  
  wavfilelist=[]
  if os.path.isdir(inpath):
    wavfilelist=glob.glob(os.path.join(inpath,'*.wav'))    
  elif os.path.isfile(inpath) and os.path.splitext(inpath)[1]=='.wav' :
    wavfilelist.append(inpath)
  else:
    print msg
    return 1
  loud=LoudnessPlotter(wavfilelist,outpath)
  loud.process()  
  
if __name__ == "__main__":
  cli()
