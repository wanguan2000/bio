__author__ = 'wanguan2000'
#coding=utf-8
import sys
import re
import os.path
import os
from myscript import *

'''
FixMateInformation for bam
####input####
input list bam files
#######

java -Xmx4g -jar ./picard-tools-1.48/FixMateInformation.jar \
   INPUT= ./testdata/31bwa_RG_realign_dedup.bam \
   OUTPUT= ./testdata/31bwa_RG_realign_dedup_mate.bam \
   SORT_ORDER=coordinate \
   VALIDATION_STRINGENCY=LENIENT

####return####
return list _mate.bam

'''

class FixMate:
    def __init__(self,config):
        self.const=config
    def picardFixMateInformation(self,Input_Bam):
        ######data, software ,path  initialization#########
        const = self.const

        picard = const.picard_FixMateInformation
        Output_Folder = const.Output_Folder
        AlignDatabase = const.AlignDatabase
        FastaDatabase = const.FastaDatabase
        ######!data, software ,path  initialization#########

        Output_List=[]
        for bam in Input_Bam:
            outbam = StringMeth().changeExtension(bam,'_mate.bam')
            cmd = ' '.join(['java',const.memory,'-jar',picard,'INPUT=',bam,'OUTPUT=',outbam,'TMP_DIR=',const.Temp_Folder,'MAX_RECORDS_IN_RAM=5000000 SORT_ORDER=coordinate VALIDATION_STRINGENCY=SILENT'])
            print cmd
            os.system(cmd)
            Output_List.append(outbam)
        return Output_List



'''test
bamfile = ['/home/wanguan2000/pg/myNGS/result_NGS/test1/s1_1_s1_2_sort.bam']
a = FixMate('config').picardFixMateInformation(bamfile)
print a
'''


