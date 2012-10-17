__author__ = 'wanguan2000'
#coding=utf-8
import sys
import re
import os.path
import os
from myscript import *

'''
VariantFiltration is used to filter out suspicious calls from VCF files based on their failing given filters
###input####
for snp and indels
input list vcf files like:[['recal_raw_snp.vcf', 'recal_raw_indel.vcf']]
for indels
input list vcf files like:['recal_raw_indel.vcf',]




    For SNPs
        DATA_TYPE_SPECIFIC_FILTERS should be "QD < 2.0", "MQ < 40.0", "FS > 60.0", "HaplotypeScore > 13.0", "MQRankSum < -12.5", "ReadPosRankSum < -8.0". 

    For Indels
        DATA_TYPE_SPECIFIC_FILTERS should be "QD < 2.0", "ReadPosRankSum < -20.0", "FS > 200.0 ,"InbreedingCoeff < -0.8 (not every one)" 



#######indel#########
java -jar /path/to/dist/GenomeAnalysisTK.jar \
  -T VariantFiltration \
  -R /seq/references/Homo_sapiens_assembly18/v0/Homo_sapiens_assembly18.fasta \
  -o /path/to/output.vcf \
  -B:variant,VCF /path/to/input.vcf \
  --filterExpression "QD < 2.0 || ReadPosRankSum < -20.0 || FS > 200.0 || InbreedingCoeff < -0.8" \
  --filterName GATKStandard

Note the InbreedingCoeff statistic is a population-level calculation that is only available with 10 or more samples.
If you have fewer samples you will need to omit that particular filter statement.
DATA_TYPE_SPECIFIC_FILTERS should be "QD < 2.0 || ReadPosRankSum < -20.0 || InbreedingCoeff < -0.8 || FS > 200.0"
###########for snp###############
java -jar /path/to/dist/GenomeAnalysisTK.jar \
  -T VariantFiltration \
  -R /seq/references/Homo_sapiens_assembly18/v0/Homo_sapiens_assembly18.fasta \
  -o /path/to/output.vcf \
  -B:variant,VCF /path/to/input.vcf \
  -B:mask,VCF /path/to/indels.filtered.vcf \
  --filterExpression "QD < 5.0 || HRun > 5 || FS > 200.0" \
  --filterName GATKStandard



 java -Xmx2g -jar GenomeAnalysisTK.jar \
   -R ref.fasta \
   -T VariantFiltration \
   -o output.vcf \
   --variant input.vcf \
   --filterExpression "AB < 0.2 || MQ0 > 50" \
   --filterName "Nov09filters" \
   --mask mask.vcf \
   --maskName InDel



####snp
DATA_TYPE_SPECIFIC_FILTERS should be "QD < 2.0", "MQ < 40.0", "FS > 60.0", "HaplotypeScore > 13.0", "MQRankSum < -12.5", "ReadPosRankSum < -8.0".
########indel
indel:    DATA_TYPE_SPECIFIC_FILTERS should be "QD < 2.0", "ReadPosRankSum < -20.0", "InbreedingCoeff < -0.8", "FS > 200.0"


####return####
for snp and indels
return ([snp_filtered,indel_filtered])
for indels
return ([indel_filtered])

'''
class GATKHardFilter:
    def __init__(self,config):
        self.const=config
    def GATKFilter_indel(self,Input_vcf):
        ######data, software ,path  initialization#########
        const = self.const

        GATK = const.GATK_last
        Output_Folder = const.Output_Folder
        dbsnp =  const.dbsnp132
        omni =  const.omni
        hapmap = const.hapmap
        indels_mills = const.indels_mills
        FastaDatabase = const.FastaDatabase

        ######!data, software ,path  initialization#########

        indel_filtered = StringMeth().changeExtension(Input_vcf,'_hfiltered.vcf')
        cmd_VariantFiltration = ' '.join(['java','-Djava.io.tmpdir='+const.Temp_Folder,const.memory,'-jar',GATK,'-T VariantFiltration','-R',FastaDatabase,'--variant',Input_vcf,'-o',indel_filtered,'--filterExpression \"QD < 2.0 || ReadPosRankSum < -20.0 || FS > 200.0\" --filterName TruthSensitivityTranche_handfilter'])
        print cmd_VariantFiltration
        os.system(cmd_VariantFiltration)
        return indel_filtered


        
    def GATKFilter_indel_snp(self,Input_vcf):
        ######data, software ,path  initialization#########
        const = self.const

        GATK = const.GATK_last
        Output_Folder = const.Output_Folder
        dbsnp = const.dbsnp132
        omni = const.omni
        hapmap = const.hapmap
        indels_mills = const.indels_mills
        FastaDatabase = const.FastaDatabase

        ######!data, software ,path  initialization#########
        Output_List=[]

        for pairvcf in Input_vcf:
            snp_filtered = StringMeth().changeExtension(pairvcf[0],'_hfiltered.vcf')
            indel_filtered = StringMeth().changeExtension(pairvcf[1],'_hfiltered.vcf')
            ####run indel###
            cmd_VariantFiltration = ' '.join(['java','-Djava.io.tmpdir='+const.Temp_Folder,const.memory,'-jar',GATK,'-T VariantFiltration','-R',FastaDatabase,'--variant',pairvcf[1],'-o',indel_filtered,'--filterExpression \"QD < 2.0 || ReadPosRankSum < -20.0 || FS > 200.0\" --filterName TruthSensitivityTranche_handfilter'])
            print cmd_VariantFiltration
            os.system(cmd_VariantFiltration)
            ####run snp###
            cmd_VariantFiltration = ' '.join(['java','-Djava.io.tmpdir='+const.Temp_Folder,const.memory,'-jar',GATK,'-T VariantFiltration','-R',FastaDatabase,'--variant',pairvcf[0],'--mask',indel_filtered,'--maskName InDel','-o',snp_filtered,'--filterExpression \"QD < 2.0 || MQ < 40.0 || FS > 60.0 || HaplotypeScore > 13.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0 \" --filterName TruthSensitivityTranche_handfilter'])
            print cmd_VariantFiltration
            os.system(cmd_VariantFiltration)


            
            Output_List.append([snp_filtered,indel_filtered])
        return Output_List
    def GATKFilter_snp_indel_sp(self,Input_vcf,FastaDatabase):
        ######data, software ,path  initialization#########
        const = self.const

        GATK = const.GATK_last
        Output_Folder = const.Output_Folder

        ######!data, software ,path  initialization#########
        Output_List=[]

        for pairvcf in Input_vcf:
            snp_filtered = StringMeth().changeExtension(pairvcf[0],'_hfiltered.vcf')
            indel_filtered = StringMeth().changeExtension(pairvcf[1],'_hfiltered.vcf')
            ####run indel "QD < 2.0", "ReadPosRankSum < -20.0", "InbreedingCoeff < -0.8", "FS > 200.0". ###
            cmd_VariantFiltration = ' '.join(['java','-Djava.io.tmpdir='+const.Temp_Folder,const.memory,'-jar',GATK,'-T VariantFiltration','-R',FastaDatabase,'--variant',pairvcf[1],'-o',indel_filtered,'--filterExpression \"QD < 2.0 || ReadPosRankSum < -20.0 || FS > 200.0\" --filterName TruthSensitivityTranche_handfilter'])
            print cmd_VariantFiltration
            os.system(cmd_VariantFiltration)
            ####run snp "QD < 2.0", "MQ < 40.0", "FS > 60.0", "HaplotypeScore > 13.0", "MQRankSum < -12.5", "ReadPosRankSum < -8.0". ###
            cmd_VariantFiltration = ' '.join(['java','-Djava.io.tmpdir='+const.Temp_Folder,const.memory,'-jar',GATK,'-T VariantFiltration','-R',FastaDatabase,'--variant',pairvcf[0],'--mask',indel_filtered,'--maskName InDel','-o',snp_filtered,'--filterExpression \"QD < 2.0 || MQ < 40.0 || FS > 60.0 || HaplotypeScore > 13.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0 \" --filterName TruthSensitivityTranche_handfilter'])
            print cmd_VariantFiltration
            os.system(cmd_VariantFiltration)



            Output_List.append([snp_filtered,indel_filtered])
        return Output_List



#"QD < 2.0", "MQ < 40.0", "FS > 60.0", "HaplotypeScore > 13.0", "MQRankSum < -12.5", "ReadPosRankSum < -8.0".

'''test indel
indelfile=['/home/wanguan2000/pg/myNGS/result_NGS/test1/s1_1_s1_2_sort_realign_dedup_mate_recal_raw_indel.vcf']
a = GATKVariantFiltration('config').GATKFilter_indel(indelfile)
print a
'''
