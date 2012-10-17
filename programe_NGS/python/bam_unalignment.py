__author__ = 'wanguan2000'
#coding=utf-8
import sys
import re
import os.path
import os
from myscript import *

'''
BamIndexStats for bam
####input####
input list bam files
#######

java -Xmx4g -jar ./picard-tools-1.48/BamIndexStats.jar \
   INPUT= ./testdata/31bwa_RG_realign_dedup.bam \
   >testdata/31bwa_RG_realign_dedup_stats.txt

####return####
return list _Stats.txt

'''





class Bam_Unalignment:
    def __init__(self,config):
        self.const=config
    def picardBamIndexStats(self,Input_Bam):
        const = self.const
        ######data, software ,path  initialization#########
        picard = const.picard_BamIndexStats

        ######!data, software ,path  initialization#########
        Output_List=[]
        for bam in Input_Bam:
            outbam = StringMeth().changeExtension(bam,'_Stats.txt')
            cmd = ' '.join(['java',const.memory,'-jar',picard,'INPUT=',bam,'>'+outbam])
            print cmd
            os.system(cmd)
            Output_List.append(outbam)
        return Output_List

