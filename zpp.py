#!/usr/bin/python
import os, sys, getopt, subprocess, json, math

def simpleOptParse(opt,arg,opts,sel,name):
	for a in arg.split(","):
		if a in opts:
			sel.append(a)
		else:
			sys.exit("Unkown " + name + " arg: " + a)

def main(argv):

	#disk layouts
	layout = []

	#possible raid modes
	raidOpts = ["raidz","raidz1","raidz2","raidz3","mirror"]

	#possible options
	atimeOpts = ["on","off"]
	syncOpts = ["standard","disabled","always"]
	recordsizeOpts = ["1k","2k","4k","8k","16k","32k","64k","128k"]
	ashiftOpts = ["9","10","11","12","13","14","15","16","17"]

	#selected options
	atimeSel = []
	syncSel = []
	recordsizeSel = []
	ashiftSel = []
	fio = ""
	name = ""
	path = ""

	#retreive the args
	opts, args = getopt.getopt(argv,"",[
		"layout=",

		"atime=",
		"sync=",
		"recordsize=",
		"ashift=",
		"path=",
		"fio=",
		"name="
	])

	#processing arguments
	for opt, arg in opts:
		if opt == "--layout":
			for o in arg.split(","):
				if o in raidOpts:
					layout.append(o)
				else:
					if os.path.exists(o) == True:
						layout.append(o)
					else:
						sys.exit("Device or mode not found: " + o)
		elif opt == "--atime":
			simpleOptParse(opt, arg, atimeOpts, atimeSel, "atime")
		elif opt == "--sync":
			simpleOptParse(opt, arg, syncOpts, syncSel, "sync")
		elif opt == "--recordsize":
			simpleOptParse(opt, arg, recordsizeOpts, recordsizeSel, "recordsize")
		elif opt == "--ashift":
			simpleOptParse(opt, arg, ashiftOpts, ashiftSel, "ashift")
		elif opt == "--name":
			for a in arg.split(","):
				name = a
		elif opt == "--path":
			for a in arg.split(","):
				path = a
		elif opt == "--fio":
			for a in arg.split(","):
				if os.path.isfile(a) == True:
					fio = a 
				else:
					sys.exit("No fio template found! " + a)

	#building blocks
	#create = "zpool create " + name + " -f "
	destroy = "zpool destroy " + name
	bench = "fio " + fio + " | grep 'read='" #confirm this

	#for l in layout:
	#	create += l + " "

	totalRuns = 0

	for a in atimeSel:
		for s in syncSel:
			for r in recordsizeSel:
				for f in ashiftSel:
					totalRuns += 1
	
	run = 1

	modes = ['iop','thruput']
	lengths = ['rand','seq']

	for a in atimeSel:
		for s in syncSel:
			for r in recordsizeSel:
				for f in ashiftSel:
					create = "zpool create " + name + " "
					for z in layout:
						create += z + " "
					if a in atimeSel:
						create += "-O atime=" + a + " "
					if s in syncSel:
						create += "-O sync=" + s + " "
					if r in recordsizeSel:
						create += "-O recordsize=" + r + " "
					if f in ashiftSel:
						create += "-o ashift=" + f + " "
					
					#print("Run: " + str(run) + " of " + str(totalRuns))
					#run += 1
					
					#create the pool
					os.system(create)

					#read tests
					result = []
					for m in modes:
						for l in lengths:
							test_cmd = "fio " + 'fio-profs/' + m + '/' + l + '-read' + " --output-format=json --filename=" + path
							ret = subprocess.run([test_cmd],stdout=subprocess.PIPE,shell=True)
							j = json.loads(ret.stdout.decode('utf-8'))
							result.append([m,l,str(math. trunc(j['jobs'][0]['read']['iops'])),str(math. trunc(j['jobs'][0]['read']['io_bytes']/1000000))+"MBps"])

					options = " atime=" + a + ", sync=" + s + ", recordsize=" + r + ", ashift=" + f
					print(str(result) + options)	

					#destroy the pool
					os.system(destroy)


if __name__ == "__main__":
	main(sys.argv[1:])