#!/usr/bin/env python
__author__ = 'wanguan2000'
import sys
import re
import os.path
import os


def todict(filename,keyroot):
    redict={}
    with open(filename, 'rU') as f:
        for line in f:
            line = line.rstrip()
            if not line:
                break
            spline = line.split('\t')
            mykey = '\t'.join([spline.__getitem__(elem) for elem in keyroot])
            redict[mykey] = line
    return redict

def do_pipeline(myfile,filekey,filedata,filedatakey):
    filedatadict = todict(filedata,filedatakey)
    with open('merage.txt', 'w') as infile:
        with open(myfile, 'rU') as f:
            for line in f:
                line = line.rstrip()
                if not line:
                    break
                spline = line.split('\t')
                mykey = '\t'.join([spline.__getitem__(elem) for elem in filekey])
                if mykey in filedatadict:
                    infile.write(line+'\t'+filedatadict[mykey]+'\n')
                else:
                    infile.write(line+'\n')




filekey=[0,1]
myfile='1.txt'

filedatakey=[0,1]
filedata='data.txt'

do_pipeline(myfile,filekey,filedata,filedatakey)

