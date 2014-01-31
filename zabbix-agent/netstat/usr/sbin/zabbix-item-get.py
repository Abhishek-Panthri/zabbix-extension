#!/usr/bin/python
from optparse import OptionParser
import sys
import re
import os.path

def checkRequiredArguments(opts, parser):
    missing_options = []
    for option in parser.option_list:
        if re.match(r'^\[REQUIRED\]', option.help) and eval('opts.' + option.dest) == None:
            missing_options.append(option)
    if len(missing_options) > 0:
        print 'Missing REQUIRED parameters'
        for o in missing_options:  
            print " %s %s" % (o, o.help) 
        sys.exit()

if __name__ == "__main__":
    parser = OptionParser(
                        usage="%prog [-fileData <file>] [-k <item>]",
                        prog="Zabbix item get from file",
                        description="This program get item from file")
    parser.add_option(
                      "-f",
                      action="store",
                      type="string",
                      dest="file",
                      help="[REQUIRED] File name with items.",
                      )
    parser.add_option(
                      "-k",
                      action="store",
                      type="string",
                      dest="item",
                      help="[REQUIRED] Zabbix item name.",
                      )
    parser.add_option(
                      "-v",
                      action="store",
                      type="int",
                      dest="verbose",
                      default=0,
                      help="Verbose - print details. [default: %default]",
                      )
    (opts, args) = parser.parse_args()
    checkRequiredArguments(opts, parser)


target = sys.argv[1]
itemName = opts.item
itemPattern = re.compile('([^=]+)=([0-9a-zA-Z\.]+)')
fileName = opts.file
itemFind = 0
if not(os.path.isfile(fileName)):
        print '0'
else:
        fileData = open(fileName, 'r')
        for line in fileData:
                m = itemPattern.match(line)
                if m:
                        k = m.group(1)
                        v = m.group(2)
                        if itemName == k:
                                itemFind = 1
                                print "%s" % (v)
                                break
if not(itemFind):
    print 0
fileData.close();