#coding=utf-8
import sys
import re
import os.path
import os
from  myscript import StringMeth


'''
input:
for pair-end
Input_Pair_Files = [
    ['inputfile_NGS/s1/s1_1.fq', 'inputfile_NGS/s1/s1_2.fq'],
    ['inputfile_NGS/s2/c.fastq', 'inputfile_NGS/s2/d.fastq']
]

for Single-end
Input_Sin_Files = ['inputfile_NGS/s1/s1_1.fq', 'inputfile_NGS/s1/s1_2.fq']

output:
Output_List

result_NGS/test1/s1_1_s1_2.sam
result_NGS/test1/s1_1.sai
result_NGS/test1/s1_2.sai


################
bwa single and pairp-end class
####################bwa bowtie index############
./bwa index -p ./indexhg19_bwa/hg19_bwa -a bwtsw ucsc.hg19.fasta
################bwa align###########
./bwa aln -t 4 -f ./testdata/leftreads.sai ./indexhg19_bwa/hg19_bwa ./testdata/s_5_1_GCCAAT.fastq
./bwa aln -t 4 -f ./testdata/rightRead.sai ./indexhg19_bwa/hg19_bwa ./testdata/s_5_2_GCCAAT.fastq
./bwa sampe -f ./testdata/31bwa.sam ./indexhg19_bwa/hg19_bwa ./testdata/leftreads.sai ./testdata/rightRead.sai ./testdata/s_5_1_GCCAAT.fastq ./testdata/s_5_2_GCCAAT.fastq
###################bwa single end#########
./bwa aln -t 4 -f single.sai ./indexhg19_bwa/hg19_bwa single.fastq
bwa samse -f single.sam ./indexhg19_bwa/hg19_bwa single.sai single.fastq


'''

class bwaMeth:
    def __init__(self,config):
        self.const=config
    def bwaPairend(self,Input_Pair_Files):
        ######data, software ,path  initialization#########
        const = self.const

        bwa = const.bwa
        Output_Folder = const.Output_Folder
        AlignDatabase = const.AlignDatabase
        FastaDatabase = const.FastaDatabase
        ######!data, software ,path  initialization#########

        Output_List=[]
        for Pair_File in Input_Pair_Files:
            leftFastq = Pair_File[0]
            RightFastq = Pair_File[1]
            LeftName = StringMeth().getPathName(Pair_File[0])
            RightName = StringMeth().getPathName(Pair_File[1])
            Output_Folder_Leftsai = Output_Folder + '/' + LeftName + '.sai'
            Output_Folder_Rightsai = Output_Folder + '/' + RightName + '.sai'
            Output_Folder_sam = Output_Folder + '/' + LeftName + '_' + RightName + '.sam'
            LeftAlign = ' '.join([bwa, 'aln -t', const.cpu, '-f', Output_Folder_Leftsai, AlignDatabase, leftFastq])
            print LeftAlign
            os.system(LeftAlign)

            RightAlign = ' '.join([bwa, 'aln -t', const.cpu, '-f', Output_Folder_Rightsai, AlignDatabase, RightFastq])
            print RightAlign
            os.system(RightAlign)

            SamFile = ' '.join(
                [bwa, 'sampe -f', Output_Folder_sam, AlignDatabase, Output_Folder_Leftsai, Output_Folder_Rightsai,
                 leftFastq,
                 RightFastq])
            print SamFile
            os.system(SamFile)
            Output_List.append(Output_Folder_sam)
        return Output_List

    def bwaSinend(self,Input_Sin_Files):

        ######data, software ,path  initialization#########
        const = self.const
        
        bwa = const.bwa
        Output_Folder = const.Output_Folder
        AlignDatabase = const.AlignDatabase
        FastaDatabase = const.FastaDatabase

        ######!data, software ,path  initialization#########

        Output_List=[]
        for Sin_Files in Input_Sin_Files:
            FastqFile =Sin_Files
            NameFastq = StringMeth().getPathName(Sin_Files)
            Output_Folder_sai = Output_Folder + '/' + NameFastq + '.sai'
            Output_Folder_sam = Output_Folder + '/' + NameFastq + '.sam'
            SinAlign = ' '.join([bwa, 'aln -t', const.cpu, '-f', Output_Folder_sai, AlignDatabase, FastqFile])
            print SinAlign
            os.system(SinAlign)
            SamFile = ' '.join([bwa, 'samse -f', Output_Folder_sam, AlignDatabase, Output_Folder_sai, FastqFile])
            print SamFile
            os.system(SamFile)
            Output_List.append(Output_Folder_sam)
        return Output_List





'''
test
mPair_File = [
    ['inputfile_NGS/s1/s1_1m.fq', 'inputfile_NGS/s1/s1_2m.fq'],
    ['inputfile_NGS/s2/cm.fastq', 'inputfile_NGS/s2/dm.fastq']
]
Sin_Files = ['inputfile_NGS/s1/s1_1.fq', 'inputfile_NGS/s1/s1_2.fq']
a = bwaMeth('config')
#print a.bwaPairend(mPair_File)
print a.bwaSinend(Sin_Files)
'''










