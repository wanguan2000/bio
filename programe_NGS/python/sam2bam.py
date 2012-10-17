__author__ = 'wanguan2000'
#coding=utf-8
import sys
import re
import os.path
import os
from myscript import *

'''
do sam to bam
####input####
input list sam files
#######

java -Xmx4g -jar ./picard-tools-1.48/SamFormatConverter.jar \
   INPUT= ./testdata/31bwa.sam \
   OUTPUT= ./testdata/31bwa.bam \
   VALIDATION_STRINGENCY=LENIENT

####return####
return list bam

'''

class Sam2Bam:
    def __init__(self,config):
        self.const=config
    def picardSamFormatConverter(self,Input_Sam):
        ######data, software ,path  initialization#########
        const = self.const
        
        picard = const.picard_SamFormatConverter
        Output_Folder =  const.Output_Folder
        AlignDatabase =  const.AlignDatabase
        FastaDatabase =  const.FastaDatabase
        ######!data, software ,path  initialization#########

        Output_List=[]
        for sam in Input_Sam:
            outbam = StringMeth().changeExtension(sam,'.bam')
            cmd = ' '.join(['java',const.memory,'-jar',picard,'INPUT=',sam,'OUTPUT=',outbam,'TMP_DIR=',const.Temp_Folder,'VALIDATION_STRINGENCY=LENIENT'])
            print cmd
            os.system(cmd)
            Output_List.append(outbam)
        return Output_List


'''test
samfile = ['inputfile_NGS/s1/s1_1.fq', 'inputfile_NGS/s1/s1_2.fq']
a = Sam2Bam('config').picardSamFormatConverter(samfile)
print a
'''

