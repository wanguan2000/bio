__author__ = 'wanguan2000'
# -*- coding: utf-8 -*-
import sys
import os
import locale
import codecs
import re
import commands


def readallfile(filelist,head,rootkey=[2, 3, 5, 6], result=[1],rename='_R1.*'):
    keydict={}
    dictall={}
    pattern = re.compile(rename)
    for filename in filelist:
        listall=[]
        with open(filename, 'rU') as f:
            for line in f:
                line = line.rstrip()
                if not line:
                    break
                if not line.startswith('#CHROM'):
                    spline = line.split('\t')
                    if not spline[12].startswith('NA'):
                        mykey = '\t'.join([spline.__getitem__(elem) for elem in rootkey])
                        listall.append(mykey)
                        keydict[mykey]=mykey
        dictall[filename]=listall
        filename = re.sub(pattern, '', filename)
        head=head+'\t'+filename

    #####
    for filename in filelist:
        for allkey in keydict.keys():

            if allkey in dictall[filename]:
                keydict[allkey] = keydict[allkey]+'\t1'
                #print keydict[allkey]
            else:
                keydict[allkey] = keydict[allkey]+'\t0'
                #print keydict[allkey]


    return head,keydict



mydict = {}
rootkey = range(0,23)
rootkey.remove(6)
rootkey.remove(7)
result = [7]

head= '#CHROM\tStart\tEnd\tREF\tALT\tVariation_type\tGene_location\tGene\tExon_syno\tExon\tdbSNP\t1000G\tGWAS\tVisift\tTFbs\tMirna\tMirnatarget\tConservedElements\tcosmic'

mypath = os.getcwd()
files = os.listdir('.')
filelist=[]

for dirname in files:
    if '_snp_filtered' in dirname:
        filelist.append(dirname)

head,keydict = readallfile(filelist,head,rootkey,result)
print head
for a in keydict:
    print keydict[a]




