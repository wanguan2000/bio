__author__ = 'wanguan2000'
#coding=utf-8
import os.path
import os
import sys
import re
from myscript import *


'''
unaligmnet
1.RNAME *
2.POS 0
3.MAPQ 0
4.CIGAR *
5. SEQ N
6.QUAL !

'''



def Unaligment(filename):
    myset = set()
    with open(filename, 'rU') as f:
        for line in f:
            if not line:
                break
            if not line.startswith('@'):
                line = line.rstrip()
                spline = line.split('\t')
                if  not spline[2].startswith('chr'):# or spline[10] == '*':
                    #print spline[0]
                    myset.add(spline[0])
    return myset

def alignedReads(fastqfile,myset):
    unligned_fastq = StringMeth().changeExtension(fastqfile,'_aligned.fastq')
    with open(unligned_fastq,'w') as input:

       with open(fastqfile, 'rU') as f:
           for line in f:
               if not line:
                   break
               if line.startswith('@') and r':' in line:
                   spline = line.split('\s')
                   if not spline[0] in myset:
                       input.write(line)
                       input.write(f.next())
                       input.write(f.next())
                       input.write(f.next())


myset = Unaligment('mm9.sam')

alignedReads('/gpfs/home/wanguan2000/Project_fastq/backup/20111108/i951681P3/i951681P3_R1.fastq',myset)
alignedReads('/gpfs/home/wanguan2000/Project_fastq/backup/20111108/i951681P3/i951681P3_R2.fastq',myset)




