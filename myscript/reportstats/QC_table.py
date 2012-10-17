__author__ = 'wanguan2000'
# -*- coding: utf-8 -*-
import sys
import os
import locale
import codecs
import re


def todict(filelist):
    mydict = {}
    mylist=[]
    for filename in filelist:
        with open(filename,'rU') as f:
            for line in f:
                line = line.rstrip()
                if not line:
                    break
                spline = line.split('\t')
                if not spline[0] in mydict.keys():
                    mydict[spline[0]]=[spline[1]]
                else:
                    mydict[spline[0]].append(spline[1])
                if not spline[0] in mylist:
                    mylist.append(spline[0])
    with open('qc_table_eachsample.xls', 'w') as infile:
        for line in mylist:
            infile.write(line+'\t'+'\t'.join(mydict[line])+'\n')
    return mydict,mylist



filelist=[]
for dirname in os.listdir('.'):
    if 'QCtbale.txt' in dirname and not dirname.startswith('.'):
        filelist.append(dirname)

todict(filelist)




