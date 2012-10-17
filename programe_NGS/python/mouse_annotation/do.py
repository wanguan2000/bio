__author__ = 'wanguan2000'
#coding=utf-8
import os.path
import os
import sys
import re
from myscript import *
from annovar import *
from stats_annotation import *


class Mouse_annotation:
    def do_annoation(self,anno_type):
        if anno_type == 'single':
            files = os.listdir('.')
            for dirname in files:
                if '_snp_hfiltered' in dirname:
                    snp_csv = Annovar('').do_pipeline(dirname,'snp')
                    Stats_Anotation('').stats_snp(snp_csv)
                    print dirname
                elif '_indel_hfiltered' in dirname:
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



