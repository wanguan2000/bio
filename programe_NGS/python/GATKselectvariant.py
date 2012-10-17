__author__ = 'wanguan2000'
#coding=utf-8
import sys
import re
import os.path
import os
from myscript import *

'''
Select Variants operates on VCF files
####input####
input list VCF files
#######
#################Select snp and indel######
java -jar GenomeAnalysisTK.jar \
     -T SelectVariants \
     -R human_g1k_v37.fasta \
     -B:variant,VCF my.big.vcf \
     -indels \
     -o rwa.indel.vcf

java -jar GenomeAnalysisTK.jar \
     -T SelectVariants \
     -R human_g1k_v37.fasta \
     -B:variant,VCF my.big.vcf \
     -snps  \
     -o rwa.snps.vcf

 Select only indels from a VCF:
 java -Xmx2g -jar GenomeAnalysisTK.jar \
   -R ref.fasta \
   -T SelectVariants \
   --variant input.vcf \
   -o output.vcf \
   -selectType INDEL

####return####
return list [['_snp.vcf','_indel.vcf'],]

'''
class GATKSelectvariant:
    def __init__(self,config):
        self.const=config
    def GATKSelect_snp_indel(self,Input_vcf):
         ######data, software ,path  initialization#########
        const = self.const

        GATK = const.GATK_last
        Output_Folder = const.Output_Folder
        dbsnp = const.dbsnp132
        FastaDatabase = const.FastaDatabase

        ######!data, software ,path  initialization#########
        Output_List=[]
        for bigvcf in Input_vcf:
            #RealignerTargetCreator
            vcf_snp = StringMeth().changeExtension(bigvcf,'_snp.vcf')
            vcf_indel = StringMeth().changeExtension(bigvcf,'_indel.vcf')
            cmd_snp = ' '.join(['java',const.memory,'-jar',GATK,'-T SelectVariants','-R',FastaDatabase,'--variant',bigvcf,'-selectType SNP','-o',vcf_snp])
            print cmd_snp
            os.system(cmd_snp)
            cmd_indel = ' '.join(['java',const.memory,'-jar',GATK,'-T SelectVariants','-R',FastaDatabase,'--variant',bigvcf,'-selectType INDEL','-o',vcf_indel])
            print cmd_indel
            os.system(cmd_indel)
            Output_List.append([vcf_snp,vcf_indel])
        return Output_List
    def GATKSelect_snp_indel_sp(self,Input_vcf,FastaDatabase):
         ######data, software ,path  initialization#########
        const = self.const

        GATK = const.GATK_last
        Output_Folder = const.Output_Folder


        ######!data, software ,path  initialization#########
        Output_List=[]
        for bigvcf in Input_vcf:
            #RealignerTargetCreator
            vcf_snp = StringMeth().changeExtension(bigvcf,'_snp.vcf')
            vcf_indel = StringMeth().changeExtension(bigvcf,'_indel.vcf')
            cmd_snp = ' '.join(['java',const.memory,'-jar',GATK,'-T SelectVariants','-R',FastaDatabase,'--variant',bigvcf,'-selectType SNP','-o',vcf_snp])
            print cmd_snp
            os.system(cmd_snp)
            cmd_indel = ' '.join(['java',const.memory,'-jar',GATK,'-T SelectVariants','-R',FastaDatabase,'--variant',bigvcf,'-selectType INDEL','-o',vcf_indel])
            print cmd_indel
            os.system(cmd_indel)
            Output_List.append([vcf_snp,vcf_indel])
        return Output_List





'''test
vcffile = ['/home/wanguan2000/pg/myNGS/result_NGS/test1/s1_1_s1_2_sort_realign_dedup_mate_recal_raw.vcf']
a = GATKUnifiedGenotyper('config').GATKSelect_snp_indel(vcffile)
print a
'''
