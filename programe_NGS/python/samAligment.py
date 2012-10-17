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

class samAligmentfasta:
    def Unaligment(self, filename):
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


    def OutReads(self, filename):
        myset = set()
        with open(filename, 'rU') as f:
            for line in f:
                if not line:
                    break
                line = line.rstrip()
                myset.add(line)
        return myset


    def alignedReads(self, fastqfile, myset, suffix='_aligned.fastq'):
        aligned_fastq = StringMeth().changeExtension(fastqfile, suffix)
        with open(aligned_fastq, 'w') as input:
            with open(fastqfile, 'rU') as f:
                for line in f:
                    if not line:
                        break
                    if line.startswith('@'):
                        line = line.rstrip()
                        spline = line.split(' ')
                        spline[0] = spline[0].replace('@', '')
                        spline[0] = spline[0].replace('#0/1', '#0')
                        spline[0] = spline[0].replace('#0/2', '#0')
                        if not spline[0] in myset:
                            input.write(line+'\n')
                            input.write(f.next())
                            input.write(f.next())
                            input.write(f.next())
                        else:
                            f.next()
                            f.next()
                            f.next()

        return aligned_fastq

    def runAligmnetfasta(self, sam, fastqpair,suffix='_aligned.fastq'):
        myset = self.Unaligment(sam)
        aligned_fastq1 = self.alignedReads(fastqpair[0][0], myset,suffix)
        aligned_fastq2 = self.alignedReads(fastqpair[0][1], myset,suffix)
        return [[aligned_fastq1, aligned_fastq2]]

    def separate_mm9hg19(self, fastqpair, fusion1sam, fusion2sam, suffix='_human.fastq'):
        myset = set()
        with open(fusion1sam, 'rU') as f:
            with open(fusion2sam, 'rU') as m:
                n1 = ''
                for line in m:

                    if not line.startswith('@'):
                        break
                    n1 = n1 + line
                m.seek(len(n1))

                n2 = ''
                for line in f:

                    if not line.startswith('@'):
                        break
                    n2 = n2 + line
                f.seek(len(n2))

                while True:
                    try:
                        L1 = f.next()
                    except:
                        break
                    L1 = L1.split('\t')
                    R1 = f.next().split('\t')

                    L2 = m.next().split('\t')
                    R2 = m.next().split('\t')

                    #in the case of MAPQ >= 40
                    if int(L2[4]) == int(L1[4]) and int(R2[4]) == int(R1[4]):
                        if 'mm9_' in L1[2] or 'mm9_' in R1[2] or 'mm9_' in L2[2] or 'mm9_' in R2[2]:
                            myset.add(L1[0])
                            myset.add(R1[0])
                            myset.add(L2[0])
                            myset.add(R2[0])
                    elif int(L2[4]) > int(L1[4]) and int(R2[4]) > int(R1[4]):
                        if 'mm9_' in L2[2] or 'mm9_' in R2[2]:
                            myset.add(L2[0])
                            myset.add(R2[0])

                    elif int(L2[4]) < int(L1[4]) and int(R2[4]) < int(R1[4]):
                        if 'mm9_' in L1[2] or 'mm9_' in R1[2]:
                            myset.add(L1[0])
                            myset.add(R1[0])
                    else:
                        if 'mm9_' in L1[2] or 'mm9_' in R1[2] or 'mm9_' in L2[2] or 'mm9_' in R2[2]:
                            myset.add(L1[0])
                            myset.add(R1[0])
                            myset.add(L2[0])
                            myset.add(R2[0])

        aligned_fastq1 = self.alignedReads(fastqpair[0][0], myset, suffix)
        aligned_fastq2 = self.alignedReads(fastqpair[0][1], myset, suffix)
        return [[aligned_fastq1, aligned_fastq2]]
'''
Pair_File = [['/gpfs2/home/luoqin/fastq/NVS10001/WUXI002/FQ/pe_1.fq','/gpfs2/home/luoqin/fastq/NVS10001/WUXI002/FQ/pe_2.fq'],]
samAligmentfasta().runAligmnetfasta('/gpfs2/home/luoqin/result/NVS10001/result_WUXI002/pe_1_pe_22347596.sam',Pair_File,'_aligned.fastq')
'''

