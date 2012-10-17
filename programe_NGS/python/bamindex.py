__author__ = 'wanguan2000'
#coding=utf-8
import sys
import re
import os.path
import os
'''
do bam to index
####input####
input list bam files
#######
java -Xmx4g -jar ./picard-tools-1.48/BuildBamIndex.jar \
   INPUT= ./testdata/31bwa_RG.bam \
   VALIDATION_STRINGENCY=LENIENT

####return####
return none

'''

class BamIndex:
    def __init__(self,config):
        self.const=config
    def picardBuildBamIndex(self,Input_Bam):
         ######data, software ,path  initialization#########
        const = self.const

        picard = const.picard_BuildBamIndex
        Output_Folder = const.Output_Folder
        AlignDatabase = const.AlignDatabase
        FastaDatabase = const.FastaDatabase
        ######!data, software ,path  initialization#########

        for bam in Input_Bam:
            cmd = ' '.join(['java',const.memory,'-jar',picard,'INPUT=',bam,'VALIDATION_STRINGENCY=SILENT'])
            print cmd
            os.system(cmd)
        return None


        
'''test
bamfile = ['inputfile_NGS/s1/s1_1.bam', 'inputfile_NGS/s1/s1_2.bam']
a = BamIndex('config').picardBuildBamIndex(bamfile)
print a
'''

