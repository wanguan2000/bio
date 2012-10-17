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
from python.GATKmergebam import *

#sudo ulimit -n 9000
#must input your config file!!!!!#############
myconfig = re.compile(r'\.py(|c)$').sub('', sys.argv[1])

exec "from %s import *" % myconfig
#Output_Folder check###
localPath = re.compile(r'/programe_NGS/.*\.py(|c)$').sub('', os.path.abspath(__file__))
Output_Folder = os.path.join(localPath, 'result_NGS', const.Output_Folder)

'''
for each sample
    lanes.bam <- merged lane.bam's for sample
    dedup.bam <- MarkDuplicates(lanes.bam)

samples.bam <- merged dedup.bam's for all samples
realigned.bam <- realign(samples.bam)
recal.bam <- recal(realigned.bam)
'''
'''
all_bam = os.listdir(Output_Folder)
list_dedup = []
for my_bam in all_bam:
    my_bam = os.path.join(Output_Folder, my_bam)
    print my_bam
    ###1.MarkDuplicates return list _dedup.bam ################
    MarkDuplicate = MarkDuplicates(myconfig).picardMarkDuplicates([my_bam])
    list_dedup.append(MarkDuplicate)

'''
list_dedup=['/home/wanguan2000/myNGS/result_NGS/result_zhao/763104N_sort_dedup.bam','/home/wanguan2000/myNGS/result_NGS/result_zhao/763104T_sort_dedup.bam','/home/wanguan2000/myNGS/result_NGS/result_zhao/775122N_sort_dedup.bam','/home/wanguan2000/myNGS/result_NGS/result_zhao/775122T_sort_dedup.bam','/home/wanguan2000/myNGS/result_NGS/result_zhao/777965N_sort_dedup.bam','/home/wanguan2000/myNGS/result_NGS/result_zhao/777965T_sort_dedup.bam','/home/wanguan2000/myNGS/result_NGS/result_zhao/780297N_sort_dedup.bam','/home/wanguan2000/myNGS/result_NGS/result_zhao/780297T_sort_dedup.bam','/home/wanguan2000/myNGS/result_NGS/result_zhao/790138N_sort_dedup.bam','/home/wanguan2000/myNGS/result_NGS/result_zhao/790138T_sort_dedup.bam','/home/wanguan2000/myNGS/result_NGS/result_zhao/790252N_sort_dedup.bam','/home/wanguan2000/myNGS/result_NGS/result_zhao/790252T_sort_dedup.bam','/home/wanguan2000/myNGS/result_NGS/result_zhao/791228N_sort_dedup.bam','/home/wanguan2000/myNGS/result_NGS/result_zhao/791228T_sort_dedup.bam','/home/wanguan2000/myNGS/result_NGS/result_zhao/835709N_sort_dedup.bam','/home/wanguan2000/myNGS/result_NGS/result_zhao/835709T_sort_dedup.bam','/home/wanguan2000/myNGS/result_NGS/result_zhao/846803N_sort_dedup.bam','/home/wanguan2000/myNGS/result_NGS/result_zhao/846803T_sort_dedup.bam','/home/wanguan2000/myNGS/result_NGS/result_zhao/881916N_sort_dedup.bam','/home/wanguan2000/myNGS/result_NGS/result_zhao/881916T_sort_dedup.bam',
]


###2.merged################
BamIndex(myconfig).picardBuildBamIndex(list_dedup)
mergebam = GATKMerge(myconfig).GATKMergeBam(list_dedup)




###3.realigned return list _realign.bam ################
realign = GATKRealign(myconfig).GATKTargetCreatorIndelRealigner(mergebam)
###4.FixmateInformation return list _mate.bam ################
FixmateInformation = FixMate(myconfig).picardFixMateInformation(realign)
###5.GATKRecalibrate return list _recal.bam ################
BamIndex(myconfig).picardBuildBamIndex(FixmateInformation)
bam_recal = GATKRecalibrate(myconfig).GATKCovariateRecalibrate(FixmateInformation)
###6.bam to raw snp and indel, return raw.vcf################
raw_vcf = GATKUnifiedGenotyper(myconfig).GATKHighcoverage(bam_recal)
###7.Select Variants operates on VCF files return list [['_snp.vcf','_indel.vcf'],]#####
snp_indel_vcf = GATKSelectvariant(myconfig).GATKSelect_snp_indel(raw_vcf)
###8.Variant quality score recalibration, return ([snp_filtered,indel_filtered])#####
snp_indel_filtered = GATKVariantRecalibrate(myconfig).GATKRecalibrate(snp_indel_vcf)
print snp_indel_filtered









