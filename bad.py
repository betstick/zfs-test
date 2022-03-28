#readTest = "fio --ioengine=libaio --filename=/flash/testfile --direct=1 --sync=0 --rw=read --bs=4K --numjobs=1 --iodepth=1 --runtime=10 --time_based --name=fio --size=1G"

#zpoolModes = ["","raidz ","raidz1 ","raidz2 ","raidz3 "]
#devices = ["/dev/nvme0n1 ","/dev/nvme1n1 ","/dev/nvme2n1 ","/dev/nvme3n1 "]

print(zpoolModes)

"""atime = "-O atime="
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
					print(fullCreate)"""