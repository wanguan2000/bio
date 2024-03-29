#!/usr/bin/env python
__author__ = 'wanguan2000'
#coding=utf-8
import os.path
import os
import sys
import re
from myscript import *
from annovar_muti import *
from stats_annotation_muti import *


'''
snp_vcf= '/gpfs2/home/wanguan2000/result2_NGS/xh/result_D28/D28_R1_D28_R2_sort_realign_dedup_mate_recal_raw_snp_filtered.vcf'
indel_vcf= '/gpfs2/home/wanguan2000/result2_NGS/xh/result_D28/D28_R1_D28_R2_sort_realign_dedup_mate_recal_raw_indel_filtered.vcf'

Annovar('a').vcf_anotation(snp_vcf,'snp')
Annovar('a').vcf_anotation(indel_vcf,'indel')
'''


#Stats_Anotation('a').stats_snp('A3_R1_A3_R2_sort_realign_dedup_mate_recal_raw_snp_filtered_Hqual.csv')
#Stats_Anotation('a').stats_indel('A3_R1_A3_R2_sort_realign_dedup_mate_recal_raw_indel_filtered_Hqual.csv')


files = os.listdir('.')
for dirname in files:
    if 'somatic_snp.vcf' in dirname:
        snp_csv = Annovar('').vcf_anotation(dirname, 'snp')
        Stats_Anotation('').stats_snp(snp_csv)
        print dirname
    elif 'somatic_indel.vcf' in dirname:
        indel_csv = Annovar('').vcf_anotation(dirname, 'indel')
        Stats_Anotation('').stats_indel(indel_csv)
        print dirname
