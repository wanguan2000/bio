__author__ = 'wanguan2000'
#coding=utf-8
import sys
import re
import os.path
import os
from myscript import *

'''
VariantAnnotator is a GATK tool for annotating variant calls based on their context. The tool is modular; new annotations can be written easily without modifying VariantAnnotator itself.
####input####
input  vcf file
#######
#################VariantAnnotator ######

java -Xmx20g -jar /home/wanguan2000/myNGS/software_NGS/GATK/GenomeAnalysisTK-1.3/GenomeAnalysisTK.jar \
   -T VariantAnnotator \
   -R /home/wanguan2000/myNGS/database_NGS/hg19fastadatabase/ucsc.hg19.fasta \
   -I i951681P3_R1_human_i951681P3_R2_human_sort_realign_dedup_mate_recal.bam \
   --variant i951681P3_R1_human_i951681P3_R2_human_sort_realign_dedup_mate_recal_raw.vcf \
   --dbsnp /home/wanguan2000/myNGS/database_NGS/hg19_GATK1_1/dbsnp_132.hg19.vcf \
   -o output.vcf \
   -A FisherStrand \
   -A MappingQualityRankSumTest \
   -A ReadPosRankSumTest \
   -A RMSMappingQuality \
   -A MappingQualityZero \
   -A QualByDepth \
   -A HaplotypeScore \
   -A DepthOfCoverage \
   -A BaseQualityRankSumTest



######################ok################

####return####
return  _anno.vcf

'''

class GATKAnnotator:
    def __init__(self,config):
        self.const=config
    def GATKVariantAnnotator(self,Input_vcf,Input_bam):
         ######data, software ,path  initialization#########
        const = self.const
        ######!data, software ,path  initialization#########
        vcf_anno = StringMeth().changeExtension(Input_vcf,'_anno.vcf')
        cmd = ' '.join(['java',const.memory,'-jar',const.GATK_last,'-T VariantAnnotator','-I',Input_bam,'-R',const.FastaDatabase,'--variant',Input_vcf,'--dbsnp',const.dbsnp132,'-o',vcf_anno,'-A FisherStrand -A MappingQualityRankSumTest -A ReadPosRankSumTest -A RMSMappingQuality -A MappingQualityZero -A QualByDepth -A HaplotypeScore -A DepthOfCoverage -A BaseQualityRankSumTest'])
        print cmd
        os.system(cmd)
        return vcf_anno


'''test
bamfile = ['/home/wanguan2000/pg/myNGS/result_NGS/test1/s1_1_s1_2_sort.bam']
a = GATKRealign('config').GATKTargetCreatorIndelRealigner(bamfile)
print a
'''

