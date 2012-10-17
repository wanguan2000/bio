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
from python.GATKvariantAnnotator import *
from python.GATKhardFilter import *
from python.GATKvariantrecalibrate_indel import *

#########initialization###############
const = Init_Pipeline().doInit(sys.argv[1])





raw_vcf=['/gpfs/home/wanguan2000/NGSToolkit/result_NGS/xenograft20111231/result_PC_07_0003_Xenograft_P2/PC_07_0003_Xenograft_P2_R1_human_PC_07_0003_Xenograft_P2_R2_human_sort_realign_dedup_mate_recal_raw.vcf']
###12.Select Variants operates on VCF files return list [['_snp.vcf','_indel.vcf'],]#####
snp_indel_vcf = GATKSelectvariant(const).GATKSelect_snp_indel(raw_vcf)
###13.Variant quality score recalibration, return ([snp_filtered,indel_filtered])#####
snp_indel_filtered = GATKVariantRecalibrate(const).GATKRecalibrate(snp_indel_vcf)
print snp_indel_filtered
###14.if indel_filtered failed , running hard filter #####
if os.path.exists(snp_indel_filtered[0][1]):
    snp_indel_filtered[0][1] = GATKVariantRecalibrate_indel(const).GATKRecalibrate_indel(snp_indel_vcf[0][1])
###15.anotation

print snp_indel_filtered







