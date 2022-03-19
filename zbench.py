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
		elif opt == "--fio=":
			for f in arg:
				if os.path.isfile(f):
					fio = f
				else:
					sys.exit("FIO config not found: " + f)

	if len(zpoolModes) < 1:
		sys.exit("No modes specified!")
	if len(devices) < 1:
		sys.exit("No devices specified!")
	if fio == "":
		sys.exit("FIO config not specified!")

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
						fullCreate = createCmd
						fullCreate += m + devices[0] + devices[1] + devices[2] + devices[3]
						fullCreate += atime + a
						fullCreate += sync + s
						fullCreate += recSize + r
						fullCreate += ashift + a2
						print(fullCreate)
						os.system(fullCreate)
						results = os.popen("fio " + fio)

if __name__ == "__main__":
	main(sys.argv[1:])