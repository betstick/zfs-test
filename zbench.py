#!/usr/bin/python

import os, sys, getopt

def main(argv):
	zpoolModes = []
	devices = []
	fio = ""

	opts, args = getopt.getopt(argv,"",["modes=","devices=","fio="])

	for opt, arg in opts:
		if opt == "--modes":
			for m in arg.split(","):
				if m == "raidz":
					zpoolModes.append(m)
				elif m == "raidz":
					zpoolModes.append(m)
				elif m == "raidz1":
					zpoolModes.append(m)
				elif m == "raidz2":
					zpoolModes.append(m)
				elif m == "raidz3":
					zpoolModes.append(m)
				elif m == "mirror":
					zpoolModes.append(m)
				else:
					sys.exit("Unkown pool mode: " + m)
		elif opt == "--devices": #this won't work if devices are zpools :/
			for d in arg.split(","):
				if os.path.exists(d):
					devices.append(d)
				else:
					sys.exit("Device not found: " + d)
		elif opt == "--fio":
			if os.path.isfile(arg):
				fio = arg
			else:
				sys.exit("FIO config not found: " + arg)

	if len(zpoolModes) < 1:
		sys.exit("No modes specified!")
	if len(devices) < 1:
		sys.exit("No devices specified!")
	if os.path.isfile(fio) != True:
		sys.exit("FIO config not specified! " + fio)

	print(zpoolModes)
	print(devices)
	print(fio)

	atime = "-O atime="
	atimeOpts = ["on ","off "]

	sync = "-O sync="
	syncOpts = ["standard ","disabled ","always "]

	recSize = "-O recordsize="
	recSizeOpts = ["4k ","8k ","16k ","64k ","128k "]

	ashift = "-o ashift="
	ashiftOpts = ["9 ","12 ","13 "]

	createCmd = "zpool create flash "
	destroyCmd = "zpool destroy flash"

	for m in zpoolModes:
		for a in atimeOpts:
			for s in syncOpts:
				for r in recSizeOpts:
					for a2 in ashiftOpts:
						os.system(destroyCmd)
						os.system("rm -rf /flash/")
						fullCreate = createCmd + m + " "
						for d in devices:
							fullCreate += d + " "
						fullCreate += atime + a
						fullCreate += sync + s
						fullCreate += recSize + r
						fullCreate += ashift + a2
						print(fullCreate)
						os.system(fullCreate + " -f")
						if os.path.exists("/flash/"):
							print("fio " + fio)
							fioOut = os.popen("fio " + fio)
							results = fioOut.read()
							print(results)
						#os.system(destroyCmd)

	os.system(destroyCmd)

if __name__ == "__main__":
	main(sys.argv[1:])