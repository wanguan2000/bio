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
from python.bwa_species import *
from python.samAligment import *
from python.GATKhardFilter import *
from python.GATKvariantrecalibrate_indel import *
from python.annovar import *
from python.stats_annotation import *

'''
#pipeline####
#1.mapping to ucscmm9 bwa return list (.sam)################
my_sam = bwaMethSP(const).bwaPairendSP(const.Pair_File,const.mm9_bwa)[0]
#2. select out aligment fastq
fastq_aligment = samAligmentfasta().runAligmnetfasta(my_sam,const.mm9_Fasta,'_aligned.fastq')
#3. aligment to fusion1 and fusion2
sam_fusion1 = bwaMethSP(const).bwaPairendSP(fastq_aligment,const.hg19mm9_fusion1)[0]
sam_fusion2 = bwaMethSP(const).bwaPairendSP(fastq_aligment,const.hg19mm9_fusion2)[0]
#4. get the mouse sequecing name, and the rests are considered to be human fastq
human_fastq = samAligmentfasta().separate_mm9hg19(const.Pair_File, sam_fusion1, sam_fusion2, '_human.fastq')




##2 get alingemnt fastq file



#####
'''


#########initialization###############
const = Init_Pipeline().doInit(sys.argv[1])

#Output_Folder check###
try:
    os.makedirs(const.Output_Folder)
    os.makedirs(const.Temp_Folder)
except OSError as inst:
    print inst.args
    print const.Output_Folder + " is exist, you should change the Output_Folder name!!!"
    raise SystemExit


#pipeline####
#1.mapping to ucscmm9 bwa return list (.sam)################
my_sam = bwaMethSP(const).bwaPairendSP(const.Pair_File,const.mm9_bwa)[0]
#2. select out aligment fastq
fastq_aligment = samAligmentfasta().runAligmnetfasta(my_sam,const.Pair_File,'_aligned.fastq')
#3. aligment to fusion1 and fusion2
sam_fusion1 = bwaMethSP(const).bwaPairendSP(fastq_aligment,const.hg19mm9_fusion1)[0]
sam_fusion2 = bwaMethSP(const).bwaPairendSP(fastq_aligment,const.hg19mm9_fusion2)[0]
#4. get the mouse sequecing name, and the rests are considered to be human fastq
human_fastq = samAligmentfasta().separate_mm9hg19(const.Pair_File, sam_fusion1, sam_fusion2, '_human.fastq')

####deepseq_pipeline

###1. fastqc return none ##############
Fastqc(const).doFastqc(human_fastq)
###2. DynamicTrim return list (.trimed)################
#my_trimed = Trim(const).DynamicTrim(human_fastq)

###3.bwa return list (.sam)################
my_sam = bwaMeth(const).bwaPairend(human_fastq)

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
#######

###10.bam to raw snp and indel, return raw.vcf################
raw_vcf = GATKUnifiedGenotyper(const).GATKHighcoverage(bam_recal)
'''
##11.VariantAnnotator is a GATK tool for annotating variant calls based on their context
anno_vcf = GATKAnnotator(const).GATKVariantAnnotator(raw_vcf[0],bam_recal[0])
'''
###12.Select Variants operates on VCF files return list [['_snp.vcf','_indel.vcf'],]#####
snp_indel_vcf = GATKSelectvariant(const).GATKSelect_snp_indel(raw_vcf)
###13.Variant quality score recalibration, return ([snp_filtered,indel_filtered])#####
snp_indel_filtered = GATKVariantRecalibrate(const).GATKRecalibrate(snp_indel_vcf)
if not os.path.exists(snp_indel_filtered[0][1]):
    snp_indel_filtered[0][1] = GATKVariantRecalibrate_indel(const).GATKRecalibrate_indel(snp_indel_vcf[0][1])

####14.annotation
csv_snp = Annovar(const).vcf_anotation(snp_indel_filtered[0][0], meth='snp')
csv_indel = Annovar(const).vcf_anotation(snp_indel_filtered[0][1], meth='indel')
####15.csv stats###
Stats_Anotation(const).stats_snp(csv_snp)
Stats_Anotation(const).stats_indel(csv_indel)







