#!/usr/bin/env python
import ROOT
import os
import numpy
import sys
import fnmatch
from copy import deepcopy as copy

from optparse import OptionParser
from optparse import OptionGroup


from Queue import Queue

from threading import Thread, Semaphore
from multiprocessing import cpu_count

end = ".txt"
class Wrap:
    def __init__(self, func, args, queue):
        self.queue = queue
        self.func = func
        self.args = args
        
    def __call__(self):
        ret = self.func( *self.args )
        self.queue.put( ret  )

    
class Parallel:
    def __init__(self,ncpu):
        self.running = Queue(ncpu)
        self.returned = Queue()
	self.njobs = 0
	
    def run(self,cmd,args):
        wrap = Wrap( self, (cmd,args), self.returned )
	self.njobs += 1
        thread = Thread(None,wrap)
        thread.start()
        
    def __call__(self,cmd,args):
        if type(cmd) == str:
            print cmd
            for a in args:
                cmd += " %s " % a
            args = (cmd,)
            cmd = commands.getstatusoutput
        self.running.put((cmd,args))
        ret = cmd( *args ) 
        self.running.get()
        self.running.task_done()
        return ret

def getFilesFromDatacard(datacard):
    if not os.path.isfile(datacard): return ""
    card = open(datacard,"r")
    files = set()
    for l in card.read().split("\n"):
        if l.startswith("shape"):
            toks = [t for t in l.split(" ") if t != "" ]
            files.add(toks[3])
    files = list(files)
    ret = files[0]
    for f in files[1:]:
        ret += ",%s" % f
    return ret

parser = OptionParser()
parser.add_option("-d","--datfile",help="Pick up running options from datfile")
parser.add_option("-q","--queue",help="Which batch queue")
parser.add_option("--dryRun",default=False,action="store_true",help="Dont submit")
parser.add_option("--parallel",default=False,action="store_true",help="Run local fits in multithreading")
parser.add_option("--runLocal",default=False,action="store_true",help="Run locally")
parser.add_option("--skipWorkspace",default=False,action="store_true",help="Dont remake MultiDim workspace")
parser.add_option("--hadd",help="Trawl passed directory and hadd files. To be used when jobs are complete.")
parser.add_option("-v","--verbose",default=False,action="store_true")
parser.add_option("--poix",default="r")
parser.add_option("--catsMap",default="")
parser.add_option("--catRanges",default="")
parser.add_option("--prefix",default="./")
parser.add_option("--postFitAll",default=False,action="store_true",help="Use post-fit nuisances for all methods")
parser.add_option("--monitor",default='',help="Monitor mode - sub/resub/check/resub-missing directory of jobs (from --outDir) ")
#parser.add_option("--blindStd",default=False,action="store_true",help="Run standard suite of blind plots")
#parser.add_option("--unblindSimple",default=False,action="store_true",help="Run simple set of unblind plots (limit, pval, best fit mu)")
#parser.add_option("--unblindFull",default=False,action="store_true",help="Run full suite of unblind plots")
specOpts = OptionGroup(parser,"Specific options")
specOpts.add_option("--datacard",default=None)
specOpts.add_option("--files",default=None)
specOpts.add_option("-o","--outDir",default=None)
specOpts.add_option("--method",default=None)
specOpts.add_option("--expected",type="int",default=None)
specOpts.add_option("--mhLow",type="float",default=None)
specOpts.add_option("--mhHigh",type="float",default=None)
specOpts.add_option("--mhStep",type="float",default=None)
specOpts.add_option("--muLow",type="float",default=None)
specOpts.add_option("--muHigh",type="float",default=None)
specOpts.add_option("--rvLow",type="float",default=None)
specOpts.add_option("--rvHigh",type="float",default=None)
specOpts.add_option("--rfLow",type="float",default=None)
specOpts.add_option("--rfHigh",type="float",default=None)
specOpts.add_option("--cvLow",type="float",default=None)
specOpts.add_option("--cvHigh",type="float",default=None)
specOpts.add_option("--cfLow",type="float",default=None)
specOpts.add_option("--cfHigh",type="float",default=None)
specOpts.add_option("--kgamLow",type="float",default=None)
specOpts.add_option("--kgamHigh",type="float",default=None)
specOpts.add_option("--kgluLow",type="float",default=None)
specOpts.add_option("--kgluHigh",type="float",default=None)
specOpts.add_option("--wspace",type="str",default=None)
specOpts.add_option("--jobs",type="int",default=None)
specOpts.add_option("--pointsperjob",type="int",default=1)
specOpts.add_option("--expectSignal",type="float",default=None)
specOpts.add_option("--expectSignalMass",type="float",default=None)
specOpts.add_option("--splitChannels",default=None)
specOpts.add_option("--toysFile",default=None)
specOpts.add_option("--additionalOptions",default="",type="string")
specOpts.add_option("--postFit",default=False,action="store_true",help="Use post-fit nuisances")
parser.add_option_group(specOpts)
(opts,args) = parser.parse_args()
if not os.path.exists(os.path.expandvars('$CMSSW_BASE/bin/$SCRAM_ARCH/combine')):
	sys.exit('ERROR - CombinedLimit package must be installed')
if not os.path.exists(os.path.expandvars('$CMSSW_BASE/bin/$SCRAM_ARCH/text2workspace.py')):
	sys.exit('ERROR - CombinedLimit package must be installed')
if not os.path.exists(os.path.expandvars('$CMSSW_BASE/bin/$SCRAM_ARCH/combineCards.py')):
	sys.exit('ERROR - CombinedLimit package must be installed')

cwd = os.getcwd()
allowedMethods = ['Scan','Asymptotic','AsymptoticGrid','ProfileLikelihood','ChannelCompatibilityCheck','MultiPdfChannelCompatibility','MHScan','MHScanStat','MHScanNoGlob','MuScan','MuScanMHProf','RVScan','RFScan','RVRFScan','MuMHScan','GenerateOnly', 'RProcScan', 'RTopoScan', 'MuVsMHScan','CVCFScan','KGluKGamScan']

def system(exec_line):
	if opts.verbose: print '\t', exec_line
	os.system(exec_line)

if opts.monitor: 
  if opts.monitor not in ['sub','check','resub','resub-missing','resub-no-run','show-fail','show-done','show-run']: sys.exit('Error -- Unknown monitor mode %s'%opts.monitor)
  dir = opts.outDir

  if opts.monitor == 'sub' or 'resub' in opts.monitor : 
    # pick up job scripts in output directory (ends in .sh)
    lofjobs = []
    for root,dirs,files in os.walk(dir):
     for file in fnmatch.filter(files,'*.sh'):
       if opts.monitor == 'resub' and not os.path.isfile('%s/%s.fail'%(root,file)): continue
       elif opts.monitor == 'resub-missing' :
         job_number=int( file[file.find('job'):file.find('.sh')].strip('job') )
	 if 'Job%d.'%job_number in ' '.join(filter(lambda x: '.root' in x, files)): continue
       elif opts.monitor == 'resub-no-run' :
	 if os.path.isfile('%s/%s.run'%(root,file)): continue 
       #lofjobs.append('%s/%s'%(os.path.abspath(root),file))
       fpath = os.path.abspath("%s/%s"%(root,file))
       do_it_system = 'bsub -q %s -o %s.log  < %s'%(opts.queue,fpath,fpath)
       if not opts.dryRun:
         system('rm -f %s/%s.done'%(root,file))
         system('rm -f %s/%s.fail'%(root,file))
         system('rm -f %s/%s.log'%(root,file))
         system(do_it_system)
       elif opts.verbose: print "\t -> ", do_it_system
   # print 'Submitting %d jobs from directory %s'%(len(lofjobs),dir)
   # submit_jobs(lofjobs) 

  if opts.monitor == 'check' or 'show' in opts.monitor: 
    failjobs = []
    runjobs  = []
    donejobs = []
    number_of_jobs = 0
    for root,dirs,files in os.walk(dir):
     for file in fnmatch.filter(files,'*.sh'):
       if os.path.isfile('%s/%s.fail'%(root,file)): failjobs.append('%s/%s'%(root,file))
       if os.path.isfile('%s/%s.done'%(root,file)):
       		if not '%s.sh'%file in failjobs : donejobs.append('%s/%s'%(root,file))
       if os.path.isfile('%s/%s.run'%(root,file)): runjobs.append('%s/%s'%(root,file))
       number_of_jobs+=1
    print 'Status of jobs directory ', dir
    print '  Total of %d jobs'%number_of_jobs 
    if opts.monitor=='show-fail' or 'show' not in opts.monitor:
      print '  %d in status Fail -> (resub them with --monitor resub)'%len(failjobs)
      for job in failjobs : print '\t FAIL %s'%job
    if opts.monitor=='show-run' or 'show' not in opts.monitor:
      print '  %d in status Running -> '%len(runjobs)
      for job in runjobs : print '\t RUN %s'%job
    if opts.monitor=='show-done' or 'show' not in opts.monitor:
      print '  %d in status Done -> '%len(donejobs)
      for job in donejobs : print '\t DONE %s'%job
    print "\n  %d/%d Running, %d/%d Done, %d/%d Failed (resub with --monitor resub)"\
    	%(len(runjobs),number_of_jobs,len(donejobs),number_of_jobs,len(failjobs),number_of_jobs)
		
  sys.exit('Finished Monitor -- %s'%opts.monitor)

if opts.parallel:
    parallel = Parallel(cpu_count())

if not opts.files and opts.datacard:
    opts.files = getFilesFromDatacard(opts.datacard)

defaults = copy(opts)


def checkValidMethod():
	if opts.method not in allowedMethods: sys.exit('%s is not a valid method'%opts.method)

def configureMassFromNJobs():
	if opts.mhLow and opts.mhHigh and opts.mhStep:
		masses = numpy.arange(opts.mhLow,opts.mhHigh+opts.mhStep,opts.mhStep)
		if len(masses)<opts.jobs: sys.exit("Can't have more masses than number of jobs")
		else:
			opts.masses_per_job = [[] for x in range(opts.jobs)]
			while len(masses)!=0:
				for j in range(opts.jobs):
					if len(masses)==0: break
					opts.masses_per_job[j].append(masses[0])
					masses = numpy.delete(masses,0)
		if len(opts.masses_per_job)!=opts.jobs: sys.exit('ERROR - len job config (%d) not equal to njobs (%d)'%(len(opts.masses_per_job),opts.jobs))

def strtodict(lstr):
	retdict = {}
	if not len(lstr): return retdict
	objects = lstr.split(':')
	for o in objects:
	  k,vs = o.split('[')
	  vs = vs.rstrip(']')
	  vs = vs.split(',')
	  retdict[k] = [float(vs[0]),float(vs[1])]
	return retdict

catRanges = strtodict(opts.catRanges)

def getSortedCats():
	cats = set()
	f = open(opts.datacard)
	for l in f.readlines():
		if l.startswith('bin'):
			els = l.split()[1:]
			for el in els: 
				cats.add(el)
			break
	
	myarr = sorted(cats, key=lambda x: (x[:3],int(x.split('cat')[1].split('_')[0])), reverse=True)
	if opts.verbose: print myarr
	return myarr

def removeRelevantDiscreteNuisances():
	newCard = open('tempcard.txt','w')
	card = open(opts.datacard)
	for line in card.readlines():
		if 'discrete' in line:
			for cat in opts.splitChannels:
				catString = '_'+cat.split('cat')[1]
				if catString in line: newCard.write(line)
		else: newCard.write(line)
	card.close()
	newCard.close()
	system('mv %s %s'%(newCard.name,card.name))

def splitCard():
	if not opts.splitChannels: sys.exit('Channel splitting options not specified')
	f = open(opts.datacard)
	allCats = set()
	for line in f.readlines():
		if line.startswith('bin'):
			for el in line.split()[1:]:
				allCats.add(el)
	f.close()
	if opts.verbose: print 'Found these categories in card: ', allCats
	veto = ""
	for cat in allCats:
		if cat in opts.splitChannels: continue
		else: veto += "|ch1_"+cat
	veto=veto[1:]
	splitCardName = opts.datacard.replace('.txt','')
	for cat in opts.splitChannels: splitCardName += '_'+cat
	splitCardName += '.txt'
	system('combineCards.py --xc="%s" %s > %s'%(veto,opts.datacard,splitCardName))
	opts.datacard = splitCardName
	removeRelevantDiscreteNuisances()

def makeStatOnlyCard():
	
	assert(opts.datacard.endswith('.txt'))
	newcardname = opts.datacard.replace('.txt','_statonly.txt') 
	outf = open(newcardname,'w')
	inf = open(opts.datacard)
	for line in inf.readlines():
		line_els = line.split()
		if line.startswith('kmax'): line = line.replace(line_els[1],'*')
		if len(line_els)>1 and (line_els[1]=='lnN' or line_els[1]=='param'): continue
		else: outf.write(line)
	inf.close()
	outf.close()
	opts.datacard = newcardname 

def makeNoGlobCard():
	
	assert(opts.datacard.endswith('.txt'))
	newcardname = opts.datacard.replace('.txt','_noglob.txt') 
	outf = open(newcardname,'w')
	inf = open(opts.datacard)
	for line in inf.readlines():
		line_els = line.split()
		if line.startswith('kmax'): line = line.replace(line_els[1],'*')
		if line.startswith('CMS_hgg_globalscale'): continue
		else: outf.write(line)
	inf.close()
	outf.close()
	opts.datacard = newcardname 

def writePreamble(sub_file):
	sub_file.write('#!/bin/bash\n')
	sub_file.write('touch %s.run\n'%os.path.abspath(sub_file.name))
	sub_file.write('cd %s\n'%os.getcwd())
	sub_file.write('eval `scramv1 runtime -sh`\n')
	sub_file.write('cd -\n')
	sub_file.write('mkdir -p scratch\n')
	sub_file.write('cd scratch\n')
	sub_file.write('cp -p $CMSSW_BASE/bin/$SCRAM_ARCH/combine .\n')
	#sub_file.write('cp -p %s .\n'%os.path.abspath(opts.datacard))
	sub_file.write('cp -f %s ./DATACARD.root\n'%(os.path.abspath(opts.datacard)))
	#opts.datacard = "DATACARD"
	if opts.toysFile: 
		for f in opts.toysFile.split(','):
			sub_file.write('cp -p %s .\n'%os.path.abspath(f))
	if opts.files:
	  for file in opts.files.split(','):
	  	if file: sub_file.write('cp -p %s .\n'%os.path.abspath(file))

def writePostamble(sub_file, exec_line):

	sub_file.write('if ( %s ) then\n'%exec_line)
	sub_file.write('\t mv higgsCombine*.root %s\n'%os.path.abspath(opts.outDir))
	sub_file.write('\t touch %s.done\n'%os.path.abspath(sub_file.name))
	sub_file.write('else\n')
	sub_file.write('\t touch %s.fail\n'%os.path.abspath(sub_file.name))
	sub_file.write('fi\n')
	sub_file.write('rm -f %s.run\n'%os.path.abspath(sub_file.name))
	sub_file.close()
	system('chmod +x %s'%os.path.abspath(sub_file.name))
	if not opts.dryRun and opts.queue:
		system('rm -f %s.done'%os.path.abspath(sub_file.name))
		system('rm -f %s.fail'%os.path.abspath(sub_file.name))
		system('rm -f %s.log'%os.path.abspath(sub_file.name))
		system('bsub -q %s -o %s.log %s'%(opts.queue,os.path.abspath(sub_file.name),os.path.abspath(sub_file.name)))
	if opts.runLocal:
		if opts.parallel:
			parallel.run(system,['bash %s'%os.path.abspath(sub_file.name)])
		else:
			system('bash %s'%os.path.abspath(sub_file.name))

def writeAsymptotic():
	print 'Writing Asymptotic'
	try:
		assert(opts.masses_per_job)
	except AssertionError:
		sys.exit('No masses have been defined')

	dname = "DATACARD.root" #opts.datacard.split("/")[-1]
	for j, mass_set in enumerate(opts.masses_per_job):
		file = open('%s/sub_job%d.sh'%(opts.outDir,j),'w')
		writePreamble(file)
		exec_line = ''
		for mass in mass_set:
			exec_line +=	'combine %s -M Asymptotic -m %6.2f '%(dname,mass)
			if opts.additionalOptions: exec_line += ' %s'%opts.additionalOptions
			if opts.expected: exec_line += ' --run=expected'
			if mass!=mass_set[-1]: exec_line += ' && '
		writePostamble(file,exec_line)

def writeAsymptoticGrid():
	print 'Writing AsymptoticGrid'
	dname = "DATACARD"#opts.datacard.split("/")[-1]
	
	if not os.path.exists(os.path.expandvars('$CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/makeAsymptoticGrid.py')):
		sys.exit('ERROR - CombinedLimit package must be installed')
	
	try:
		assert(opts.masses_per_job)
	except AssertionError:
		sys.exit('No masses have been defined')
	
	# create specialised limit grid workspace
	if not opts.skipWorkspace:
		print 'Creating workspace for %s...'%opts.method
		ws_exec_line = 'text2workspace.py %s -o %s -m %g'%(os.path.abspath(opts.datacard),os.path.abspath(opts.datacard).replace('.txt','.root'),opts.mh) 
		system(ws_exec_line)
	opts.datacard = opts.datacard.replace('.txt','.root')

	# sub jobs through combine
	for j, mass_set in enumerate(opts.masses_per_job):
		for mass in mass_set:
			system('python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/makeAsymptoticGrid.py -w %s -m %6.2f -n 10 -r %3.1f %3.1f --runLimit --nCPU=3 -d %s'%(opts.datacard,mass,opts.muLow,opts.muHigh,os.path.abspath(opts.outDir)))
			sub_file_name = os.path.abspath(opts.outDir+'/limitgrid_%5.1f.sh'%(mass))
			if opts.verbose:
				print 'bsub -q %s -n 3 -R "span[hosts=1]" -o %s.log %s'%(opts.queue,os.path.abspath(sub_file_name),os.path.abspath(sub_file_name))
			if not opts.dryRun and opts.queue:
				system('rm -f %s.log'%os.path.abspath(sub_file_name))
				system('bsub -q %s -n 3 -R "span[hosts=1]" -o %s.log %s'%(opts.queue,os.path.abspath(sub_file_name),os.path.abspath(sub_file_name)))
			if opts.runLocal:
				system('bash %s'%os.path.abspath(sub_file_name))

	# switch back
	opts.datacard = opts.datacard.replace('.root','.txt')

def writeProfileLikelhood():

	print 'Writing ProfileLikelihood'
	try:
		assert(opts.masses_per_job)
	except AssertionError:
		sys.exit('No masses have been defined')

	tempcardstore = opts.datacard
	if opts.splitChannels: splitCard()
	toysfilestore = opts.toysFile

	dname = "DATACARD.root"#opts.datacard.split("/")[-1]
	# write
	for j, mass_set in enumerate(opts.masses_per_job):
		file = open('%s/sub_job%d.sh'%(opts.outDir,j),'w')
		if opts.toysFile:
			opts.toysFile = ''
			for mass in mass_set:
				opts.toysFile += toysfilestore.replace('${m}',str(mass)).replace('.0','')
		writePreamble(file)
		exec_line = ''
		for mass in mass_set:
			exec_line +=	'combine %s -M ProfileLikelihood -m %6.2f --signif --pval '%(dname,mass)
			if opts.additionalOptions: exec_line += ' %s'%opts.additionalOptions
			if opts.expected: exec_line += ' -t -1'
			if opts.expectSignal: exec_line += ' --expectSignal=%3.1f'%opts.expectSignal
			if opts.expectSignalMass: exec_line += ' --expectSignalMass=%6.2f'%opts.expectSignalMass
			if opts.toysFile: exec_line += ' --toysFile %s'%toysfilestore.replace('${m}',str(mass)).replace('.0','')
			if mass!=mass_set[-1]: exec_line += ' && '
		
		writePostamble(file,exec_line)
	# change back
	opts.datacard = tempcardstore
	opts.toysFile = toysfilestore

def writeChannelCompatibility():

	dname = "DATACARD.root"#opts.datacard.split("/"[-1]
	print 'Writing ChannelCompatibility'
	try:
		assert(opts.mh)
	except AssertionError:
		sys.exit('mh is not defined')

	file = open('%s/sub_m%6.2f.sh'%(opts.outDir,opts.mh),'w')
	writePreamble(file)
	exec_line = 'combine %s -M ChannelCompatibilityCheck -m %6.2f --rMin=-25. --saveFitResult '%(dname,opts.mh)
	writePostamble(file,exec_line)

def writeSingleGenerateOnly():
	
	dname = opts.datacard.split("/")[-1]
	dname = "DATACARD.root"#opts.datacard.split("/")[-1]
	file = open('%s/sub.sh'%(opts.outDir),'w')
	writePreamble(file)
	exec_line = 'combine %s -M GenerateOnly -m %6.2f --saveToys '%(dname,opts.mh)
	if opts.expected: exec_line += ' -t -1'
	if opts.expectSignal: exec_line += ' --expectSignal=%3.1f'%opts.expectSignal
	if opts.expectSignalMass: exec_line += ' --expectSignalMass=%6.2f'%opts.expectSignalMass
	writePostamble(file,exec_line)

def writeGenerateOnly():

	if opts.splitChannels:
		backupcard = opts.datacard
		backupdir = opts.outDir
		if 'all' in opts.splitChannels:
			cats = getSortedCats()
			for cat in cats:
				opts.splitChannels = [cat]
				splitCard()
				opts.outDir += '/'+cat
				system('mkdir -p %s'%opts.outDir)
				writeSingleGenerateOnly()
				opts.datacard = backupcard
				opts.outDir = backupdir
		else:
			splitCard()
			writeSingleGenerateOnly()
			opts.datacard = backupcard
			opts.outDir = backupdir
	else:
		writeSingleGenerateOnly()
def writeMultiPdfChannelCompatibility():
	
	print 'Writing MultiPdfChannelCompatibility'
	backupcard = opts.datacard
	backupdir = opts.outDir
	cats = getSortedCats()
	rmindefault = opts.muLow
	rmaxdefault = opts.muHigh
	catRanges = strtodict(opts.catRanges)
	for cat in cats:
		if cat in catRanges.keys():
		  if opts.verbose: print " set ranges for cat %s to"%cat, catRanges[cat]
		  opts.muLow  = catRanges[cat][0]
		  opts.muHigh = catRanges[cat][1]
		if opts.verbose: print cat
		opts.splitChannels = [cat]
		splitCard()
		opts.outDir += '/'+cat
		system('mkdir -p %s'%opts.outDir)
		opts.method = 'MuScan'
		writeMultiDimFit()
		opts.datacard = backupcard
		opts.outDir = backupdir
		opts.muLow  = rmindefault
		opts.muHigh = rmaxdefault
	
def writeMultiDimFit(method=None,wsOnly=False):

	print 'Writing MultiDim Scan'
	ws_args = { 
		"Scan"		: " ", # Should actually make the workspace first!
		"RVRFScan" 	: "-P HiggsAnalysis.CombinedLimit.PhysicsModel:rVrFXSHiggs --PO higgsMassRange=120,130" ,
		"RVScan"	: "-P HiggsAnalysis.CombinedLimit.PhysicsModel:rVrFXSHiggs --PO higgsMassRange=120,130" ,
		"RVnpRFScan" 	: "-P HiggsAnalysis.CombinedLimit.PhysicsModel:rVrFXSHiggs --PO higgsMassRange=120,130" ,
		"RFScan"	: "-P HiggsAnalysis.CombinedLimit.PhysicsModel:rVrFXSHiggs --PO higgsMassRange=120,130" ,
		"RFnpRVScan" 	: "-P HiggsAnalysis.CombinedLimit.PhysicsModel:rVrFXSHiggs --PO higgsMassRange=120,130" ,
		"MuScan"	: "",
		"MuScanMHProf"	: "-P HiggsAnalysis.CombinedLimit.PhysicsModel:floatingHiggsMass",
		"CVCFScan"	: "-P HiggsAnalysis.CombinedLimit.HiggsCouplings:cVcF --PO higgsMassRange=122,128",
		"KGluKGamScan"	: "-P HiggsAnalysis.CombinedLimit.HiggsCouplings:higgsLoops --PO higgsMassRange=122,128",
		"MHScan"	: "-P HiggsAnalysis.CombinedLimit.PhysicsModel:rVrFXSHiggs --PO higgsMassRange=120,130",
		"MHScanStat" 	: "-P HiggsAnalysis.CombinedLimit.PhysicsModel:rVrFXSHiggs --PO higgsMassRange=120,130",
		"MHScanNoGlob"	: "-P HiggsAnalysis.CombinedLimit.PhysicsModel:rVrFXSHiggs --PO higgsMassRange=120,130",
		"MuMHScan"	: "-P HiggsAnalysis.CombinedLimit.PhysicsModel:floatingHiggsMass",
		"RTopoScan"	: "-P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel %s --PO higgsMassRange=120,130" % opts.catsMap,
		"RProcScan"	: "-P HiggsAnalysis.CombinedLimit.PhysicsModel:floatingXSHiggs --PO modes=ggH,qqH,VH,ttH --PO higgsMassRange=124,126 --PO ggHRange=-1:10 --PO qqHRange=-2:20 --PO VHRange=-2:20 --PO ttHRange=-2:20 "
	}

        setpois = {
            "RVRFScan" : [ "RV", "RF" ],
            "RVScan" : [ "RV", "RF" ],
            "RVnpRFScan": [ "RV", "RF" ],
            "RFScan": [ "RV", "RF" ],
            "RFnpRVScan": [ "RV", "RF" ],
            "MuScan": [ ],
            "MuScanMHProf": [ ],
            "CVCFScan": [ "CV", "CF" ],
            "KGluKGamScan": [ "kgluon", "kgamma" ],
            "MHScan": [ ],
            "MHScanStat": [ ],
            "MHScanNoGlob": [ ],
            "MuMHScan": [ ],
            "RProcScan": [ "r_ggH","r_qqH","r_VH","r_ttH" ],
            "RTopoScan": [ "r_untag","r_qqHtag","r_VHtag","r_ttHtag" ],
            }
	
	combine_args = {
		"Scan" 	: "-P %s"%(opts.poix) , 
		"RVRFScan" 	: "-P RV -P RF --floatOtherPOIs=1" , 
		"RVScan"	: "--floatOtherPOIs=1 -P RV" ,
		"RVnpRFScan"	: "--floatOtherPOIs=0 -P RV" ,
		"RFScan"	: "--floatOtherPOIs=1 -P RF" ,
		"RFnpRVScan"	: "--floatOtherPOIs=0 -P RF" ,
		"MuScan"	: "-P r",
		"MuScanMHProf"	: "-P r --floatOtherPOIs=1",
		"CVCFScan"	: "-P CV -P CF --floatOtherPOIs=1", 
		"KGluKGamScan"	: "-P kgluon -P kgamma --floatOtherPOIs=1", 
		"MHScan"	: "--floatOtherPOIs=1 -P MH",
		"MHScanStat"	: "--floatOtherPOIs=1 -P MH",
		"MHScanNoGlob"	: "--floatOtherPOIs=1 -P MH",
		"MuMHScan"	: "-P r -P MH",
		"RProcScan"	: "--floatOtherPOIs=1 -P %s"%(opts.poix), # need to add option to run specific process
		"RTopoScan"	: "--floatOtherPOIs=1 -P %s"%(opts.poix) # need to add option to run specific topologic categories
		}
	par_ranges = {}
	if opts.rvLow!=None and opts.rvHigh!=None and opts.rfLow!=None and opts.rfHigh!=None:
		par_ranges["RVRFScan"]	= "RV=%4.2f,%4.2f:RF=%4.2f,%4.2f"%(opts.rvLow,opts.rvHigh,opts.rfLow,opts.rfHigh)
	if opts.rvLow!=None and opts.rvHigh!=None:
		par_ranges["RVScan"]	= "RV=%4.2f,%4.2f"%(opts.rvLow,opts.rvHigh) 
	if opts.rvLow!=None and opts.rvHigh!=None:
		par_ranges["RVnpRFScan"]= "RV=%4.2f,%4.2f"%(opts.rvLow,opts.rvHigh)
	if opts.rfLow!=None and opts.rfHigh!=None:
		par_ranges["RFScan"]	= "RF=%4.2f,%4.2f"%(opts.rfLow,opts.rfHigh)
	if opts.rfLow!=None and opts.rfHigh!=None:
		par_ranges["RFnpRVScan"]= "RF=%4.2f,%4.2f"%(opts.rfLow,opts.rfHigh)
	if opts.muLow!=None and opts.muHigh!=None:
		par_ranges["MuScan"]	= "r=%4.2f,%4.2f"%(opts.muLow,opts.muHigh) 
		par_ranges["MuScanMHProf"]= "r=%4.2f,%4.2f"%(opts.muLow,opts.muHigh) 
		par_ranges["RProcScan"]	  = "%s=%4.2f,%4.2f"%(opts.poix,opts.muLow,opts.muHigh)
		par_ranges["RTopoScan"]	  = "%s=%4.2f,%4.2f"%(opts.poix,opts.muLow,opts.muHigh)
	if opts.cvLow!=None and opts.cvHigh!=None and opts.cfLow!=None and opts.cfHigh!=None:
		par_ranges["CVCFScan"]	  = "CV=%4.2f,%4.2f:CF=%4.2f,%4.2f"%(opts.cvLow,opts.cvHigh,opts.cfLow,opts.cfHigh)
	if opts.kgamLow!=None and opts.kgamHigh!=None and opts.kgluLow!=None and opts.kgluHigh!=None:
		par_ranges["KGluKGamScan"] = "kgamma=%4.2f,%4.2f:kgluon=%4.2f,%4.2f"%(opts.kgamLow,opts.kgamHigh,opts.kgluLow,opts.kgluHigh)
	if opts.mhLow!=None and opts.mhHigh!=None:
		par_ranges["MHScan"]	  = "MH=%6.2f,%6.2f"%(opts.mhLow,opts.mhHigh)
		par_ranges["MHScanStat"]  = "MH=%6.2f,%6.2f"%(opts.mhLow,opts.mhHigh)
		par_ranges["MHScanNoGlob"]= "MH=%6.2f,%6.2f"%(opts.mhLow,opts.mhHigh)
	if opts.muLow!=None and opts.muHigh!=None and opts.mhLow!=None and opts.mhHigh!=None:
		par_ranges["MuMHScan"]	  = "r=%4.2f,%4.2f:MH=%6.2f,%6.2f"%(opts.muLow,opts.muHigh,opts.mhLow,opts.mhHigh)
	# create specialised MultiDimFit workspace
	if not method:
		method = opts.method
	backupcard = opts.datacard
	if method=='MHScanStat':
		makeStatOnlyCard()
	if method=='MHScanNoGlob':
		makeNoGlobCard()
	if not opts.skipWorkspace:
		datacardname = os.path.basename(opts.datacard).replace('.txt','')
		print 'Creating workspace for %s...'%method
		exec_line = 'text2workspace.py %s -m %g -o %s %s'%(os.path.abspath(opts.datacard),opts.mh,os.path.abspath(opts.datacard).replace('.txt',method+'.root'),ws_args[method]) 
		print exec_line
		if opts.postFit:
                    exec_line += '&& combine -m 125 -M MultiDimFit --saveWorkspace -n %s_postFit %s' % ( datacardname+method, os.path.abspath(opts.datacard).replace('.txt',method+'.root') )
                    exec_line += '&& mv higgsCombine%s_postFit.MultiDimFit.mH125.root %s' % ( datacardname+method, os.path.abspath(opts.datacard).replace('.txt',method+'_postFit.root') )
                if opts.parallel and opts.dryRun:
                    parallel.run(system,(exec_line,))
                else:
                    system(exec_line)
        
	if wsOnly:
		return

	if opts.postFit:
            opts.datacard = opts.datacard.replace('.txt',method+'_postFit.root')
            if opts.expected and method in setpois and opts.expectSignal:
                pars = ""
                for poi in setpois[method]:
                    if pars != "": pars+=","
                    pars += "%s=%4.2f" % ( poi, opts.expectSignal )
                if pars != "":
                    if not "--setPhysicsModelParameters" in opts.additionalOptions:
		      opts.additionalOptions += " --setPhysicsModelParameters %s" %pars

	else:
		opts.datacard = opts.datacard.replace('.txt',method+'.root')
	# make job scripts
	dname = opts.datacard.split("/")[-1]
	dname = "DATACARD.root"#opts.datacard.split("/"[-1]
	for i in range(opts.jobs):
		file = open('%s/sub_m%1.5g_job%d.sh'%(opts.outDir,getattr(opts,"mh",0.),i),'w')
		writePreamble(file)
		exec_line = 'combine %s -M MultiDimFit --algo=grid  %s --points=%d --firstPoint=%d --lastPoint=%d -n %sJob%d'%(dname,combine_args[method],opts.pointsperjob*opts.jobs,i*opts.pointsperjob,(i+1)*opts.pointsperjob-1,method,i)
		if method in par_ranges.keys(): exec_line+=" --setPhysicsModelParameterRanges %s "%(par_ranges[method])
		if getattr(opts,"mh",None): exec_line += ' -m %6.2f'%opts.mh
		if opts.expected: exec_line += ' -t -1'
		if opts.expectSignal: exec_line += ' --expectSignal %4.2f'%opts.expectSignal
		if opts.expectSignalMass: exec_line += ' --expectSignalMass %6.2f'%opts.expectSignalMass
		if opts.additionalOptions: exec_line += ' %s'%opts.additionalOptions
		if opts.toysFile: exec_line += ' --toysFile %s'%opts.toysFile
		if opts.verbose: print '\t', exec_line
		writePostamble(file,exec_line)

	opts.datacard = backupcard 

def run():
	# setup
	opts.outDir=os.path.join(opts.prefix,opts.outDir)
	system('mkdir -p %s'%opts.outDir)
	if opts.verbose: print 'Made directory', opts.outDir
	checkValidMethod()
	# submit
	storecard = opts.datacard
	if opts.postFit:
		opts.additionalOptions += " --snapshotName MultiDimFit"
		if opts.expected:
			opts.additionalOptions += " --toysFrequentist --bypassFrequentistFit" # Skip the actual fit but recentre constraints on fitted values from snapshot.
		if ( opts.method=='Asymptotic' or opts.method=='AsymptoticGrid' or opts.method=='ProfileLikelihood' or  opts.method=='ChannelCompatibilityCheck' or  opts.method=='MultiPdfChannelCompatibility' or  opts.method=='MultiPdfChannelCompatibility'):
			writeMultiDimFit("MuMHScan",True)
			opts.datacard = opts.datacard.replace('.txt','MuMHScan_postfit.root')
			if opts.expected:
				opts.additionalOptions += " ---overrideSnapshotMass --redefineSignalPOIs r --freezeNuisances MH"
	if opts.wspace: opts.datacard=opts.wspace	
	if opts.method=='Asymptotic' or opts.method=='AsymptoticGrid' or opts.method=='ProfileLikelihood':
		configureMassFromNJobs()
	if opts.method=='Asymptotic':
		writeAsymptotic()
	elif opts.method=='AsymptoticGrid':
		writeAsymptoticGrid()
	elif opts.method=='ProfileLikelihood':
		writeProfileLikelhood()
	elif opts.method=='ChannelCompatibilityCheck':
		writeChannelCompatibility()
	elif opts.method=='MultiPdfChannelCompatibility':
		writeMultiPdfChannelCompatibility()
	elif opts.method=='GenerateOnly':
		writeGenerateOnly()
	else:
		writeMultiDimFit()
	opts.datacard = storecard
def resetDefaultConfig():
    global opts
    opts = copy(defaults)
    ### for opt in specOpts.option_list:
    ###     opt_name = opt.dest.strip('--')
    ###     if opt_name=='datacard' or opt_name=='files': continue
    ###     else: setattr(opts,opt_name,None)

def configure(config_line):
	# could automate this but makes it easier to read and add options this way
	resetDefaultConfig()
	if opts.verbose: print config_line
	for option in config_line.split():
		if option.startswith('outDir='): opts.outDir = option.split('=')[1]
		if option.startswith('method='): opts.method = option.split('=')[1]
		if option.startswith('expected='): opts.expected = int(option.split('=')[1])
		if option.startswith('expectSignal='): opts.expectSignal = float(option.split('=')[1])
		if option.startswith('expectSignalMass='): opts.expectSignalMass = float(option.split('=')[1])
		if option.startswith('mhLow='): opts.mhLow = float(option.split('=')[1])
		if option.startswith('mhHigh='): opts.mhHigh = float(option.split('=')[1])
		if option.startswith('mhStep='): opts.mhStep = float(option.split('=')[1])
		if option.startswith('jobs='): opts.jobs = int(option.split('=')[1])
		if option.startswith('pointsperjob='): opts.pointsperjob = int(option.split('=')[1])
		if option.startswith('splitChannels='): opts.splitChannels = option.split('=')[1].split(',')
		if option.startswith('toysFile='): opts.toysFile = option.split('=')[1]
		if option.startswith('mh='): opts.mh = float(option.split('=')[1])
		if option.startswith('poix='): 
			poiopt = option.split('=')[1]
			if ',' in poiopt:
				opts.poix = " -P ".join(poiopt.split(','))
			else: opts.poix = option.split('=')[1]
		if option.startswith('muLow='): opts.muLow = float(option.split('=')[1])
		if option.startswith('muHigh='): opts.muHigh = float(option.split('=')[1])
		if option.startswith('rvLow='): opts.rvLow = float(option.split('=')[1])
		if option.startswith('rvHigh='): opts.rvHigh = float(option.split('=')[1])
		if option.startswith('rfLow='): opts.rfLow = float(option.split('=')[1])
		if option.startswith('rfHigh='): opts.rfHigh = float(option.split('=')[1])
		if option.startswith('cvLow='): opts.cvLow = float(option.split('=')[1])
		if option.startswith('cvHigh='): opts.cvHigh = float(option.split('=')[1])
		if option.startswith('cfLow='): opts.cfLow = float(option.split('=')[1])
		if option.startswith('cfHigh='): opts.cfHigh = float(option.split('=')[1])
		if option.startswith('kgamLow='): opts.kgamLow = float(option.split('=')[1])
		if option.startswith('kgamHigh='): opts.kgamHigh = float(option.split('=')[1])
		if option.startswith('kgluLow='): opts.kgluLow = float(option.split('=')[1])
		if option.startswith('kgluHigh='): opts.kgluHigh = float(option.split('=')[1])
		if option.startswith('wspace='): opts.wspace = str(option.split('=')[1])
		if option.startswith('catRanges='): opts.catRanges = str(option.split('=')[1])
		if option.startswith('opts='): 
			addoptstr = option.split("=")[1:]
			addoptstr = "=".join(addoptstr)
			opts.additionalOptions =  addoptstr.replace('+',' ')
			opts.additionalOptions = opts.additionalOptions.replace(">"," ")
			opts.additionalOptions = opts.additionalOptions.replace("<"," ")
		if option.startswith('catsMap='):
			print option
			for mp in option.split('=')[1].split(';'):
				if not "[" in mp.split(':')[-1]:
					mp += "[1,0,20]"
				opts.catsMap += " --PO map=%s" % mp
		if option.startswith('catRanges='):
			catRanges = strtodict(opts.catRanges)
		if option == "skipWorkspace": opts.skipWorkspace = True
		if option == "postFit":  opts.postFit = True
		if option == "expected": opts.expected = 1
        if opts.postFitAll: opts.postFit = True
	if opts.wspace : opts.skipWorkspace=True
	if "-P" in opts.poix and (opts.muLow!=None or opts.muHigh!=None): sys.exit("Cannot specify muLow/muHigh with >1 POI. Remove the muLow/muHigh option and add use --setPhysicsModelParameterRanges in opts keyword") 
	if opts.verbose: print opts
	run()

def trawlHadd():
	list_of_dirs=set()
	for root, dirs, files in os.walk(opts.hadd):
		for x in files:
			if 'higgsCombine' in x and '.root' in x: 
				list_of_dirs.add(root)

	for dir in list_of_dirs:
		for root, dirs, files in os.walk(dir):
			list_of_files=''
			for file in fnmatch.filter(files,'higgsCombine*Job*.root'):
				list_of_files += ' '+os.path.join(root,'%s'%file)
			print root, ' -- ', len(list_of_files.split())
			system('mkdir -p tmp_r')

			print list_of_files 
			for fi in list_of_files.split():
			  print fi
			  fif = ROOT.TFile.Open(fi)
			  fin = ROOT.TFile("tmp_r/tmp_%s"%(fi.split('/')[-1]),"RECREATE")
			  tr = fif.Get("limit")
			  fin.WriteTObject(tr)
			  fin.Close(); fif.Close();
			outname = dir.replace('/','_')
			exec_line = 'hadd -f %s/%s.root tmp_r/*'%(dir,outname)
			if opts.verbose: print exec_line
			system(exec_line)
			system('rm -rf tmp_r')

if opts.hadd:
	trawlHadd()
elif opts.datfile:
	datfile = open(opts.datfile)
	for line in datfile.readlines():
		line=line.strip('\n')
		if line.startswith('#') or len(line)==0: 
			continue
		if line.startswith('datacard'): 
			opts.datacard = line.split('=')[1]
                        defaults.datacard = opts.datacard
			#assert('.txt' in opts.datacard)
                        opts.files = getFilesFromDatacard(opts.datacard)
                        defaults.files += ","+opts.files
			continue
		if line.startswith('wspace'): 
			opts.wspace = line.split('=')[1]
                        defaults.datacard = opts.wspace
			#assert('.txt' in opts.datacard)
                        #opts.files = getFilesFromDatacard(opts.datacard)
                        defaults.files = opts.files
			continue
			
		if line.startswith('files'):
			opts.files = line.split('=')[1]
                        defaults.files = opts.files
			continue
		configure(line)

else:
	# default setup here
	print 'Not yet implemented'
        
if opts.parallel:
    for i in range(parallel.njobs):
	print parallel.returned.get()
        
