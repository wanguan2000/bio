__author__ = 'wanguan2000'
# -*- coding: utf-8 -*-
import sys
import os
import locale
import codecs
import re
from myscript import *

'''
java -Xmx15g -jar /gpfs/home/wanguan2000/NGSToolkit/software_NGS/GATK/GenomeAnalysisTK-1.3-24-gc8b1c92/GenomeAnalysisTK.jar\
-R /gpfs/home/wanguan2000/NGSToolkit/database_NGS/hg19fastadatabase/ucsc.hg19.fasta\
-T PrintReads\
-I /gpfs/home/wanguan2000/NGSToolkit/result_NGS/xenograft20111231/result_LP_19_0001_Xenograft_P1/LP_19_0001_Xenograft_P1_R1_human_LP_19_0001_Xenograft_P1_R2_human_sort_realign_dedup_mate_recal.bam\
-o TP53.bam\
-L chr17:7571720-7590863

java -Xmx4g -jar /gpfs/home/wanguan2000/NGSToolkit/software_NGS/picard-tools-1.55/SamFormatConverter.jar\
INPUT= TP53.bam\
OUTPUT= TP53.sam

java -Xmx4g -jar /gpfs/home/wanguan2000/NGSToolkit/software_NGS/picard-tools-1.55/SamToFastq.jar\
INPUT= TP53.sam\
FASTQ= TP53_R1.fastq\
SECOND_END_FASTQ= TP53_R2.fastq
'''






def getbamfastq(bam,region):
    ##bam region
    GATK='/gpfs/home/wanguan2000/NGSToolkit/software_NGS/GATK/GenomeAnalysisTK-1.3-24-gc8b1c92/GenomeAnalysisTK.jar'
    picard = '/gpfs/home/wanguan2000/NGSToolkit/software_NGS/picard-tools-1.55/'
    ref_fasta = '/gpfs/home/wanguan2000/NGSToolkit/database_NGS/hg19fastadatabase/ucsc.hg19.fasta'
    bam_TP53 = StringMeth().changeExtension(bam,'_TP53.bam')


    cmd_region=' '.join(['java -Xmx15g -jar',GATK,'-R',ref_fasta,'-T PrintReads','-I',bam,'-o',bam_TP53,'-L',region])
    print cmd_region
    os.system(cmd_region)
    ####bam2sam
    sam_TP53 = StringMeth().changeExtension(bam_TP53,'.sam')
    cmd_sam=' '.join(['java -Xmx4g -jar',picard+'SamFormatConverter.jar','INPUT=',bam_TP53,'OUTPUT=',sam_TP53])
    print cmd_sam
    os.system(cmd_sam)
    ###sam2fastq
    R1_fastq = StringMeth().changeExtension(sam_TP53,'_R1.fastq')
    R2_fastq = StringMeth().changeExtension(sam_TP53,'_R2.fastq')
    cmd_fastq=' '.join(['java -Xmx4g -jar',picard+'SamToFastq.jar','INPUT=',sam_TP53,'FASTQ=',R1_fastq,'SECOND_END_FASTQ=',R2_fastq])
    print cmd_fastq
    os.system(cmd_fastq)

    bam_TP53_index=StringMeth().changeExtension(bam_TP53,'.bai')

    return [bam_TP53,bam_TP53_index,R1_fastq,R2_fastq]

TP53_region='chr17:7571720-7590863'
bam='/gpfs2/home/wanguan2000/result2_NGS/ONL03009/result_WGC000229/WGC000229_combined_filtered_R1_human_WGC000229_combined_filtered_R2_human_sort_realign_dedup_mate_recal.bam'

result = getbamfastq(bam,TP53_region)
cmd = 'cp '+ ' '.join(result)+' /gpfs3/home/wanguan2000/lishi'
os.system(cmd)




