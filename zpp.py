#!/usr/bin/python
import os, sys, getopt

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
	ashiftOpts = ["9","10","11","12","13"]

	#selected options
	atimeSel = []
	syncSel = []
	recordsizeSel = []
	ashiftSel = []
	fio = ""
	name = ""

	#retreive the args
	opts, args = getopt.getopt(argv,"",[
		"layout="

		"atime=",
		"sync=",
		"recordsize=",
		"ashift=",

		"fio=",
		"name="
	])

	#processing arguments
	for opt, arg in opts:
		if opt == "--layout":
			for a in arg.split(","):
				if a in raidOpts:
					layout.append(a)
				else:
					if os.path.exists(a) == True:
						layout.append(a)
					else:
						sys.exit("Device or mode not found: " + o)
		elif opt == "--atime":
			simpleOptParse(opt, arg, atimeOpts, atimeSel, "atime")
		elif opt == "--sync":
			simpleOptParse(opt, arg, atimeOpts, atimeSel, "sync")
		elif opt == "--recordsize":
			simpleOptParse(opt, arg, recordsizeOpts, recordsizeSel, "recordsize")
		elif opt == "--ashift":
			simpleOptParse(opt, arg, ashiftOpts, ashiftSel, "ashift")
		elif opt == "--name":
			for a in arg.split(","):
				name = a
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

	for a in atimeOpts:
		for s in syncOpts:
			for r in recordsizeOpts:
				for f in ashiftOpts:
					create = "zpool create " + name + " -f "
					if a in atimeSel:
						create += "-O atime=" + a + " "
					if s in syncSel:
						create += "-O sync=" + s + " "
					if r in recordsizeSel:
						create += "-O recordsize=" + r + " "
					if f in ashiftSel:
						create += "-o ashift=" + f + " "
					
					print(create)

	

if __name__ == "__main__":
	print("test")
	main(sys.argv[1:])