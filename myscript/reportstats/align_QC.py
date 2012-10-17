__author__ = 'wanguan2000'
# -*- coding: utf-8 -*-
import sys
import os
import locale
import codecs
import re

'''
Total effective reads
Total effective yield(Mb)
Uniquely mapping reads rate
No-mismatch mapping reads rate
Mismatch alignment bases rate



The ratio of reads alignment to reference genome

Reads on target regions rate
Fraction of target covered by reads

Reads on +-150 target regions rate
Fraction of +-150 target covered by reads

Reads on near +-500 target regions rate
Fraction of +-500 target covered by reads


Fraction of target bases covered
Fraction of target covered with at least 4X
Fraction of target covered with at least 10X
Fraction of target covered with at least 20X
Mean coverage sequencing depth on target
>CodingExons  basecover

Fraction of CodingExons bases covered
Fraction of CodingExons covered with at least 4X
Fraction of CodingExons covered with at least 10X
Fraction of CodingExons covered with at least 20X
Mean coverage sequencing depth on CodingExons




files = os.listdir('.')
for myfile in files:
    if myfile.endswith('samstats.txt'):
        pass
        

'''



result=[]
files = os.listdir('.')
for myfile in files:
    if myfile.endswith('samstats.txt'):
        with open(myfile,'rU') as f:
            lineall = f.readlines()
            lineall.insert(0, myfile)
            #print lineall
            result.append(lineall)




print 'Statistics Items\t',
for mei in result:
    jie = mei[0].rstrip()
    print "%s\t" % (re.subn(r'_.*', '', jie)[0]),


print '\nTotal effective reads\t',
for mei in result:
    jie = mei[2].rstrip()
    print "%s\t" % (jie),

print '\nTotal effective yield(Mb)\t',
for mei in result:
    jie = int(mei[2].rstrip())
    print "%.2f\t" % (jie*100/1000000.0),


print '\nUniquely mapping reads rate\t',
for mei in result:
    jie = mei[3].rstrip()
    print "%s\t" % (re.subn(r'.*: ', '', jie)[0]),


print '\nNo-mismatch mapping reads rate\t',
for mei in result:
    jie = mei[4].rstrip()
    print "%s\t" % (re.subn(r'.*: ', '', jie)[0]),


print '\nMismatch alignment bases rate\t',
for mei in result:
    jie = mei[5].rstrip()
    print "%s\t" % (re.subn(r'.*: ', '', jie)[0]),

print '\nThe ratio of reads alignment to reference genome\t',
for mei in result:
    jie = mei[9].rstrip()
    print "%s\t" % (re.subn(r'.*: ', '', jie)[0]),

print '\nReads on target regions rate\t',
for mei in result:
    jie = mei[11].rstrip()
    print "%s\t" % (re.subn(r'.*: ', '', jie)[0]),

print '\nFraction of target covered by reads\t',
for mei in result:
    jie = mei[12].rstrip()
    print "%s\t" % (re.subn(r'.*: ', '', jie)[0]),


print '\nReads on +-150 target regions rate\t',
for mei in result:
    jie = mei[14].rstrip()
    print "%s\t" % (re.subn(r'.*: ', '', jie)[0]),

print '\nFraction of +-150 target covered by reads\t',
for mei in result:
    jie = mei[15].rstrip()
    print "%s\t" % (re.subn(r'.*: ', '', jie)[0]),


print '\nReads on +-500 target regions rate\t',
for mei in result:
    jie = mei[17].rstrip()
    print "%s\t" % (re.subn(r'.*: ', '', jie)[0]),

print '\nFraction of +-500 target covered by reads\t',
for mei in result:
    jie = mei[18].rstrip()
    print "%s\t" % (re.subn(r'.*: ', '', jie)[0]),


print '\nFraction of target bases covered\t',
for mei in result:
    jie = mei[21].rstrip()
    print "%s\t" % (re.subn(r'.*: ', '', jie)[0]),

print '\nFraction of target covered with at least 4X\t',
for mei in result:
    jie = mei[22].rstrip()
    print "%s\t" % (re.subn(r'.*: ', '', jie)[0]),


print '\nFraction of target covered with at least 10X\t',
for mei in result:
    jie = mei[23].rstrip()
    print "%s\t" % (re.subn(r'.*: ', '', jie)[0]),

print '\nFraction of target covered with at least 20X\t',
for mei in result:
    jie = mei[24].rstrip()
    print "%s\t" % (re.subn(r'.*: ', '', jie)[0]),


print '\nMean coverage sequencing depth on target\t',
for mei in result:
    jie = mei[25].rstrip()
    print "%s\t" % (re.subn(r'.*: ', '', jie)[0]),


print '\nFraction of CodingExons bases covered\t',
for mei in result:
    jie = mei[28].rstrip()
    print "%s\t" % (re.subn(r'.*: ', '', jie)[0]),

print '\nFraction of CodingExons covered with at least 4X\t',
for mei in result:
    jie = mei[29].rstrip()
    print "%s\t" % (re.subn(r'.*: ', '', jie)[0]),

print '\nFraction of CodingExons covered with at least 10X\t',
for mei in result:
    jie = mei[30].rstrip()
    print "%s\t" % (re.subn(r'.*: ', '', jie)[0]),

print '\nFraction of CodingExons covered with at least 20X\t',
for mei in result:
    jie = mei[31].rstrip()
    print "%s\t" % (re.subn(r'.*: ', '', jie)[0]),

print '\nMean coverage sequencing depth on CodingExons\t',
for mei in result:
    jie = mei[32].rstrip()
    print "%s\t" % (re.subn(r'.*: ', '', jie)[0]),

