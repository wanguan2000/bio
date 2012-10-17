#coding=utf-8
__author__ = 'wanguan2000'
import sys
import re
import os.path
import os
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




#must input your config file!!!!!#############
myconfig = re.compile(r'\.py(|c)$').sub('', sys.argv[1])

exec "from %s import *" % myconfig
#Output_Folder check###
localPath = re.compile(r'/programe_NGS/.*\.py(|c)$').sub('', os.path.abspath(__file__))
Output_Folder = os.path.join(localPath, 'result_NGS', const.Output_Folder)

'''
try:
    os.makedirs(Output_Folder)
except OSError as inst:
    print inst.args
    print Output_Folder + " is exist, you should change the Output_Folder name!!!"
    raise SystemExit
#########end-initialization###############
'''
'''
###1. fastqc return none ##############
Fastqc(myconfig).doFastqc(const.Pair_File)
###2. DynamicTrim return list (.trimed)################
my_trimed = Trim(myconfig).DynamicTrim(const.Pair_File)
print my_trimed

###3.bwa return list (.sam)################
my_sam = bwaMeth(myconfig).bwaPairend(const.Pair_File)
print my_sam

###4.sam2bamsortgroup return list (.bam)################
my_bam = Sam2BamSortGroup(myconfig).picardAddOrReplaceReadGroups(my_sam,const.Pair_Info)
###5.bamindex return none ################
BamIndex(myconfig).picardBuildBamIndex(my_bam)
####
'''
'''for lane
realigned
MarkDuplicate
FixmateInformation
recalibrated
'''
#####
'''
###6.realigned return list _realign.bam ################

realign = GATKRealign(myconfig).GATKTargetCreatorIndelRealigner(my_bam)
###7.realigned return list _dedup.bam ################
MarkDuplicate = MarkDuplicates(myconfig).picardMarkDuplicates(realign)
###8.FixmateInformation return list _mate.bam ################
FixmateInformation = FixMate(myconfig).picardFixMateInformation(MarkDuplicate)
###9.FixmateInformation return list _mate.bam ################

FixmateInformation=['/home/wanguan2000/myNGS/result_NGS/result_ige2/ge_R1_ge_R2_sort_realign_dedup.bam']
BamIndex(myconfig).picardBuildBamIndex(FixmateInformation)
bam_recal = GATKRecalibrate(myconfig).GATKCovariateRecalibrate(FixmateInformation)

#######
###10.bam to raw snp and indel, return raw.vcf################
raw_vcf = GATKUnifiedGenotyper(myconfig).GATKHighcoverage(bam_recal)

'''
###11.Select Variants operates on VCF files return list [['_snp.vcf','_indel.vcf'],]#####
raw_vcf='/home/wanguan2000/myNGS/result_NGS/result_ige2/ge_R1_ge_R2_sort_realign_dedup_recal_raw.vcf'

snp_indel_vcf = GATKSelectvariant(myconfig).GATKSelect_snp_indel([raw_vcf])
###12.Variant quality score recalibration, return ([snp_filtered,indel_filtered])#####
snp_indel_filtered = GATKVariantRecalibrate(myconfig).GATKRecalibrate(snp_indel_vcf)
print snp_indel_filtered














