__author__ = 'wanguan2000'
#coding=utf-8
import os.path
import os
import sys
import re
from myscript import *
from annovar import *
from stats_annotation import *


'''
snp_vcf= '/gpfs2/home/wanguan2000/result2_NGS/xh/result_D28/D28_R1_D28_R2_sort_realign_dedup_mate_recal_raw_snp_filtered.vcf'
indel_vcf= '/gpfs2/home/wanguan2000/result2_NGS/xh/result_D28/D28_R1_D28_R2_sort_realign_dedup_mate_recal_raw_indel_filtered.vcf'

Annovar('a').vcf_anotation(snp_vcf,'snp')
Annovar('a').vcf_anotation(indel_vcf,'indel')
'''


#Stats_Anotation('a').stats_snp('A3_R1_A3_R2_sort_realign_dedup_mate_recal_raw_snp_filtered_Hqual.csv')
#Stats_Anotation('a').stats_indel('A3_R1_A3_R2_sort_realign_dedup_mate_recal_raw_indel_filtered_Hqual.csv')




'''
         files = os.listdir('.')
         for dirname in files:
             if '_snp_filtered' in dirname:
                 do_annoation(dirname,anno_type)
                 snp_csv = Annovar('').vcf_anotation(dirname,'snp')
                 Stats_Anotation('').stats_snp(snp_csv)
                 print dirname
             elif '_indel_filtered' in dirname:
                 indel_csv = Annovar('').vcf_anotation(dirname,'indel')
                 Stats_Anotation('').stats_indel(indel_csv)
                 print dirname
'''


def do_annoation(anno_type):
    if anno_type == 'single':
        files = os.listdir('.')
        for dirname in files:
            if '_snp_' in dirname:
                snp_csv = Annovar('').do_pipeline(dirname,'snp')
                Stats_Anotation('').stats_snp(snp_csv)
                print dirname
            elif '_indel_' in dirname:
                indel_csv = Annovar('').do_pipeline(dirname,'indel')
                Stats_Anotation('').stats_indel(indel_csv)
                print dirname
    if anno_type == 'muti':
        files = os.listdir('.')
        for dirname in files:
            if '_snp_filtered' in dirname:
                snp_csv = Annovar('').domuti_pipeline(dirname,'snp')
                Stats_Anotation('').stats_snp_muti(snp_csv)
                print dirname
            elif '_indel_filtered' in dirname:
                indel_csv = Annovar('').domuti_pipeline(dirname,'indel')
                Stats_Anotation('').stats_indel_muti(indel_csv)
                print dirname

anno_type = sys.argv[1]
print anno_type
do_annoation(anno_type)


