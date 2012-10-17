__author__ = 'wanguan2000'
#coding=utf-8
import sys
import re
import os.path
import os
from myscript import *

'''
MarkDuplicates for bam
####input####
input list bam files
#######

java -Xmx4g -jar ./picard-tools-1.48/MarkDuplicates.jar \
   INPUT= ./testdata/31bwa_RG_realign.bam \
   OUTPUT= ./testdata/31bwa_RG_realign_dedup.bam \
   METRICS_FILE=./testdata/31bwa_RG_cleaned.dedup.metrics \
   REMOVE_DUPLICATES=false \
   ASSUME_SORTED=true \
   VALIDATION_STRINGENCY=LENIENT

####return####
return list _dedup.bam

'''

class MarkDuplicates:
    def __init__(self,config):
        self.const=config
    def picardMarkDuplicates(self,Input_Bam):
        ######data, software ,path  initialization#########
        const = self.const

        picard =  const.picard_MarkDuplicates
        Output_Folder =  const.Output_Folder
        AlignDatabase =  const.AlignDatabase
        FastaDatabase = const.FastaDatabase
        ######!data, software ,path  initialization#########

        Output_List=[]
        for bam in Input_Bam:
            outbam = StringMeth().changeExtension(bam,'_dedup.bam')
            outmetrics = StringMeth().changeExtension(bam,'_dedup.metrics')
            cmd = ' '.join(['java',const.memory,'-jar',picard,'INPUT=',bam,'OUTPUT=',outbam,'TMP_DIR=',const.Temp_Folder,'METRICS_FILE=',outmetrics,'MAX_RECORDS_IN_RAM=5000000 REMOVE_DUPLICATES=false ASSUME_SORTED=true VALIDATION_STRINGENCY=LENIENT'])
            print cmd
            os.system(cmd)
            Output_List.append(outbam)
        return Output_List



'''test
bamfile = ['/home/wanguan2000/pg/myNGS/result_NGS/test1/s1_1_s1_2_sort.bam']
a = MarkDuplicates('config').picardMarkDuplicates(bamfile)
print a
'''


