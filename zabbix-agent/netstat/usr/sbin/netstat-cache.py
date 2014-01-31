#!/usr/bin/python

from optparse import OptionParser
import sys

if __name__ == "__main__":
    parser = OptionParser(
                        usage="%prog [-file <file>] [-k <item>]",
                        prog="Parse data from netstat and optionaly save as cache",
                        description="This program get item from file")
    parser.add_option(
                      "-f",
                      action="store",
                      type="string",
                      dest="file",
                      help="File name to store cache.",
                      )

    (opts, args) = parser.parse_args()


class CustomCounter():
    "Uniwersalny licznik"

    name = None
    counter = None
    def __init__(self, name=None):
        self.name = name
        self.counter = dict()
    def add(self, k):
        c = self.counter
        if k in c:
            c[k] += 1
        else:
            c[k] = 1
    def get(self, k):
        v = self.counter.get(k)
        if v is not None:
            return v 
        else:
            return 0
    def iter(self):
        i = self.counter.iterkeys()
        i = sorted(i)
        return i

def printCustomCounter(cnt):
    ci = cnt.iter()
    for k in ci:
        c = cnt.get(k)
	if toFile:
		fw.write('%s=%s\n' % (k, c))
	else:
		print '%s=%s' % (k, c)

counter = CustomCounter('Licznik')

f = open('/tmp/netstat-fetch', 'r')
fileToSave = opts.file
toFile = 0
if not(fileToSave == None):
	toFile = 1
	fw = open(fileToSave, 'w')
lineCnt = 0
for line in f:
	if lineCnt > 1:
		lineCols = line.split()
#		print lineCols
		lineColNr = 0
		for col in lineCols:
			if lineColNr == 3:
				LocalAddress = col
				if LocalAddress.startswith("::ffff:"):
					LocalAddress = LocalAddress[7:]
				LocalAddress = LocalAddress.split(":")
				LocalAddressIp = LocalAddress[0]
				LocalAddressPort = LocalAddress[1]
			if lineColNr == 4:
				ForeignAddress = col
				if ForeignAddress.startswith("::ffff:"):
					ForeignAddress = ForeignAddress[7:]
				ForeignAddress = ForeignAddress.split(":")
				ForeignAddressIp = ForeignAddress[0]
				ForeignAddressPort = ForeignAddress[1]
			if lineColNr == 5:
				State = col
			lineColNr +=1
#		print "LocalAddressIp:%s, LocalAddressPort:%s, ForeignAddressIp:%s, ForeignAddressPort:%s, State:%s" % (LocalAddressIp, LocalAddressPort, ForeignAddressIp, ForeignAddressPort, State)
#		counter.add(LocalAddressIp + ':x,x:x,state.all')

		counter.add('state.all')
		counter.add(LocalAddressIp + ',state.all')

		counter.add('state.' + State)
		counter.add(LocalAddressIp + ',state.' + State)

		counter.add(LocalAddressIp + ':' + LocalAddressPort + ',state.all')

		counter.add('all:all,' + ForeignAddressIp + ':all,state.all')
		counter.add('all:all,' + ForeignAddressIp + ':all,state.' + State)
		counter.add('all:all,' + ForeignAddressIp + ':' + ForeignAddressPort + ',state.all')
		counter.add('all:all,' + ForeignAddressIp + ':' + ForeignAddressPort + ',state.' + State)

	lineCnt += 1
f.close()
printCustomCounter(counter)

if toFile:
	fw.close()
