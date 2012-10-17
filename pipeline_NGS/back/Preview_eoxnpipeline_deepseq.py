#coding=utf-8
__author__ = 'wanguan2000'
import sys
import re
import os.path
import os
sys.path.insert(0,os.path.join(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0], 'programe_NGS'))
from python.myscript import *
from python.fastqc import *
from python.trim import *
from python.bwa_align import *
from python.sam2bamsortgroup import *
from python.bamindex import *
from python.GATKrealigned import *
from python.markduplicate import *
from python.fixmate import *
from python.GATKrecalibrate import *
from python.GATKunifiedGenotyper import *
from python.GATKselectvariant import *
from python.GATKvariantrecalibrate import *



#########initialization###############
const = Init_Pipeline().doInit(sys.argv[1])

'''
#Output_Folder check###
try:
    os.makedirs(const.Output_Folder)
    os.makedirs(const.Temp_Folder)
except OSError as inst:
    print inst.args
    print const.Output_Folder + " is exist, you should change the Output_Folder name!!!"
    raise SystemExit

###1. fastqc return none ##############
Fastqc(const).doFastqc(const.Pair_File)
###2. DynamicTrim return list (.trimed)################
my_trimed = Trim(const).DynamicTrim(const.Pair_File)

###3.bwa return list (.sam)################
my_sam = bwaMeth(const).bwaPairend(my_trimed)

###4.sam2bamsortgroup return list (.bam)################
my_bam = Sam2BamSortGroup(const).picardAddOrReplaceReadGroups(my_sam,const.Pair_Info)

'''
#for lane
#realigned
#MarkDuplicate
#FixmateInformation
#recalibrated
'''
#####

###6.realigned return list _realign.bam ################
realign = GATKRealign(const).GATKTargetCreatorIndelRealigner(my_bam)

###7.realigned return list _dedup.bam ################
MarkDuplicate = MarkDuplicates(const).picardMarkDuplicates(realign)

###8.FixmateInformation return list _mate.bam ################
FixmateInformation = FixMate(const).picardFixMateInformation(MarkDuplicate)

###9.Recalibrate return list _recal.bam ################
BamIndex(const).picardBuildBamIndex(FixmateInformation)
bam_recal = GATKRecalibrate(const).GATKCovariateRecalibrate(FixmateInformation)
'''
#######
###10.bam to raw snp and indel, return raw.vcf################
bam_recal=['/home/wanguan2000/NGSToolkit/result_NGS/reuslt_i951681P3human/i951681P3_R1_human.fastq_i951681P3_R2_human.fastq_sort_realign_dedup_mate_recal.bam']

raw_vcf = GATKUnifiedGenotyper(const).GATKHighcoverage(bam_recal)

###11.Select Variants operates on VCF files return list [['_snp.vcf','_indel.vcf'],]#####
snp_indel_vcf = GATKSelectvariant(const).GATKSelect_snp_indel(raw_vcf)

###12.Variant quality score recalibration, return ([snp_filtered,indel_filtered])#####
snp_indel_filtered = GATKVariantRecalibrate(const).GATKRecalibrate(snp_indel_vcf)
print snp_indel_filtered





