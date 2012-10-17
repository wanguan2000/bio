__author__ = 'wanguan2000'
#coding=utf-8
import sys
import re
import os.path
import os
from myscript import *

'''
do bam to realigned
####input####
input list bam files
#######
#################Creating Intervals slowly 4h######
java -Xmx4g -jar ./GenomeAnalysisTK-1.1-12-g2d94037/GenomeAnalysisTK.jar \
  -T RealignerTargetCreator \
  -I ./testdata/31bwa_RG.bam \
  -R ucsc.hg19.fasta \
  -o ./testdata/31bwa_RG.intervals \
  -B:dbsnp,vcf /share/user_data/wfz1/database/hg19database/dbsnp_132.hg19.vcf


The current best set of known indels to be used for local realignment (note that we don't use dbSNP for this anymore); use both files:
    1000G_biallelic.indels.b37.vcf (currently from the 1000 Genomes Phase I indel calls)
    Mills_Devine_2hit.indels.b37.vcf 


 java -Xmx1g -jar /path/to/GenomeAnalysisTK.jar \
  -T RealignerTargetCreator \
  -R /path/to/reference.fasta \
  -o /path/to/output.intervals \
  --known /path/to/indel_calls.vcf


###############################Realigning slowly 4h #####################

java -Djava.io.tmpdir=/share/user_data/wfz1/tmp \
  -Xmx4g \
  -jar ./GenomeAnalysisTK-1.1-12-g2d94037/GenomeAnalysisTK.jar \
  -I ./testdata/31bwa_RG.bam \
  -R ucsc.hg19.fasta \
  -T IndelRealigner \
  -targetIntervals ./testdata/31bwa_RG.intervals \
  -o ./testdata/31bwa_RG_realign.bam \
  -B:dbsnp,vcf /share/user_data/wfz1/database/hg19database/dbsnp_132.hg19.vcf

java -Xmx4g -Djava.io.tmpdir=/path/to/tmpdir \
  -jar /path/to/GenomeAnalysisTK.jar \
  -I <lane-level.bam> \
  -R <ref.fasta> \
  -T IndelRealigner \
  -targetIntervals <intervalListFromStep1Above.intervals> \
  -o <realignedBam.bam> \
  --known /path/to/indel_calls.vcf
  --consensusDeterminationModel KNOWNS_ONLY \
  -LOD 0.4
######################ok################

####return####
return list _realign.bam

'''
class GATKRealign:
    def __init__(self,config):
        self.const=config
    def GATKTargetCreatorIndelRealigner(self,Input_Bam):
         ######data, software ,path  initialization#########
        const = self.const


        GATK = const.GATK_last
        Output_Folder = const.Output_Folder
        dbsnp = const.dbsnp132
        FastaDatabase = const.FastaDatabase

        ######!data, software ,path  initialization#########
        Output_List=[]
        for bam in Input_Bam:
            #RealignerTargetCreator
            bam_intervals = StringMeth().changeExtension(bam,'.intervals')
            cmd_TargetCreator = ' '.join(['java',const.memory,'-jar',GATK,'-T RealignerTargetCreator','-I',bam,'-R',FastaDatabase,'-o',bam_intervals,'-known:',const.indels_1000G_realignment,'-known:',const.indels_mills_realignment])
            print cmd_TargetCreator
            os.system(cmd_TargetCreator)
            #IndelRealigner
            bam_realign = StringMeth().changeExtension(bam,'_realign.bam')
            cmd_realign = ' '.join(['java','-Djava.io.tmpdir='+const.Temp_Folder,const.memory,'-jar',GATK,'-T IndelRealigner','-I',bam,'-R',FastaDatabase,'-targetIntervals' ,bam_intervals,'-o',bam_realign,'-known:',const.indels_1000G_realignment,'-known:',const.indels_mills_realignment,'--consensusDeterminationModel KNOWNS_ONLY -LOD 0.4'])
            print cmd_realign
            os.system(cmd_realign)
            Output_List.append(bam_realign)
        return Output_List





'''test
bamfile = ['/home/wanguan2000/pg/myNGS/result_NGS/test1/s1_1_s1_2_sort.bam']
a = GATKRealign('config').GATKTargetCreatorIndelRealigner(bamfile)
print a
'''

