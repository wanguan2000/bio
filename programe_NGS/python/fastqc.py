__author__ = 'wanguan2000'
#coding=utf-8
import sys
import re
import os.path
import os
'''
do fastqc for pair-end list and single-end list
####input####
input list fastq files
#######
./fastqc -f fastq -t 4 -o out2 test-6_1.fq test2-6_2.fq test32-6_2.fq test432-6_2.fq
return none
##run###
a = Fastqc('config')
a.doFastqc(mPair_File)
a.doFastqc(Sin_Files)
####return####
return none

'''
class Fastqc:
    def __init__(self, config):
        self.const=config
    def doFastqc(self, Input_Files):
        const = self.const

        fastqc = const.fastqc
        Output_Folder = const.Output_Folder

        filename = []
        for a in Input_Files:
            if isinstance(a, list):
                filename.append(a[0])
                filename.append(a[1])
            else:
                filename.append(a)

        runFastqc = ' '.join(['perl',fastqc,'-t',const.cpu,'-o',Output_Folder,''])+ ' '.join(filename)
        print runFastqc
        os.system(runFastqc)
        print "fastqc is ok"


'''
test
mPair_File = [
    ['inputfile_NGS/s1/s1_1m.fq', 'inputfile_NGS/s1/s1_2m.fq'],
    ['inputfile_NGS/s2/cm.fastq', 'inputfile_NGS/s2/dm.fastq']
]
Sin_Files = ['inputfile_NGS/s1/s1_1.fq', 'inputfile_NGS/s1/s1_2.fq']
a = Fastqc('config')
a.doFastqc(Sin_Files)
'''
