__author__ = 'wanguan2000'
#coding=utf-8
import sys
import re
import os.path
import os
from myscript import *

'''
do mergebam
####input####
input list bam files
#######
#################mergebam######
#java -jar GenomeAnalysisTK.jar -T PrintReads -I <first>.bam -I <next>.bam -R <your>.fasta --outputBamFile <merged>.bam

####return####
return _merge.bam
'''
class GATKMerge:
    def __init__(self,config):
        self.const=config
    def GATKMergeBam(self,Input_Bam):
         ######data, software ,path  initialization#########
        const = self.const

        GATK = const.GATK_last
        Output_Folder = const.Output_Folder
        Output_List=[]
        FastaDatabase = const.FastaDatabase

        ######!data, software ,path  initialization#########
        mergebam = StringMeth().changeName(Input_Bam[0],'_ALLmerge.bam')
        out_mergebam = os.path.join(const.Output_Folder,os.path.basename(mergebam))
        allbam = '-I '+ ' -I '.join(Input_Bam)
        cmd_merge = ' '.join(['java',const.memory,'-jar',GATK,'-T PrintReads',allbam,'-R',FastaDatabase,'-o',out_mergebam])
        print cmd_merge
        os.system(cmd_merge)
        Output_List.append(out_mergebam)
        return Output_List





'''test
bamfile = ['/home/wanguan2000/pg/myNGS/result_NGS/test1/s1_1_s1_2_sort.bam','/home/wanguan2000/pg/myNGS/result_NGS/test1/s1_1_s1_2_sort2.bam']
a = GATKMerge('config').GATKMergeBam(bamfile)
print a
'''

