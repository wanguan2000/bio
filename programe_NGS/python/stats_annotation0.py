__author__ = 'wanguan2000'
# -*- coding: utf-8 -*-
import sys
import os
import locale
import codecs
import re
from myscript import *
from operator import attrgetter

class Stats_Anotation:
    def __init__(self, config):
        pass
        #self.const = config

    def stats_snp(self, Input_cvs):
        ######data, software ,path  initialization#########
        outcvs = StringMeth().changeExtension(Input_cvs, '_stats.txt')
        het_hom={}
        Gene_location={}
        Exon_syno={}
        dbSNP = 0
        G1000 = 0
        total_number = 0

        with open(Input_cvs, 'rU') as f:
            for line in f:
                line = line.rstrip()
                if not line:
                    break
                total_number = total_number+1
                spline = line.split('\t')
                key_stats=[7,8,10,12,13]
                #7 sample 1/1:0,54:54:99:2011,159,0
                if spline[7].startswith('0/1'):
                    het_hom['het'] =het_hom.get('het',0) +1
                elif spline[7].startswith('1/1'):
                    het_hom['hom'] =het_hom.get('hom',0) +1

                #8 A3_R1_A3_R2_sort_realign_dedup_mate_recal_raw_snp_filtered_Hqual.csv
                if not spline[10].startswith('Gene_location'):
                    Gene_location[spline[10]] = Gene_location.get(spline[10],0)+1

                #10 Exon_syno
                if not spline[12].startswith('NA') and not spline[12].startswith('Exon_syno') :
                    Exon_syno[spline[12]] = Exon_syno.get(spline[12],0)+1

                #12 dbSNP
                if spline[14].startswith('rs') and not spline[14].startswith('dbSNP') :
                    dbSNP = dbSNP+1

                #13 1000G
                if not spline[15].startswith('NA') and not spline[15].startswith('1000G') :
                    G1000 = G1000+1

        with open(outcvs, 'w') as infile:
            infile.write('Variant Statistics Items\t'+ re.sub('_R1.*', '_snp', StringMeth().getPathName(Input_cvs)) +'\n')
            infile.write('High-confidence SNPs number:\t'+ str(total_number-1) +'\n')
            infile.write('Heterozygotes:\t'+str(het_hom['het'])+'\n')
            infile.write('Homozygotes:\t'+str(het_hom['hom'])+'\n')
            infile.write('dbSNP:\t%s(%0.1f%%)\n'%(str(dbSNP),(dbSNP*100.0/(het_hom['het']+het_hom['hom']))))
            infile.write('1000G:\t%s(%0.1f%%)\n'%(str(G1000),(G1000*100.0/(het_hom['het']+het_hom['hom']))))
            #Gene_location
            for element in sorted(Gene_location.keys()):
                infile.write(element+':\t'+str(Gene_location[element])+'\n')
            #Exon
            for element in sorted(Exon_syno.keys()):
                infile.write('Exon_'+element+':\t'+str(Exon_syno[element])+'\n')
        return outcvs

    def stats_indel(self, Input_cvs):
        ######data, software ,path  initialization#########
        outcvs = StringMeth().changeExtension(Input_cvs, '_stats.txt')
        het_hom={}
        Gene_location={}
        Exon_syno={}
        dbSNP = 0
        G1000 = 0
        delete = 0
        insert = 0
        total_number = 0
        with open(Input_cvs, 'rU') as f:
            for line in f:
                line = line.rstrip()
                if not line:
                    break
                total_number = total_number+1
                spline = line.split('\t')
                key_stats=[7,8,10,12,13]
                #7 sample 1/1:0,54:54:99:2011,159,0
                if spline[7].startswith('0/1'):
                    het_hom['het'] =het_hom.get('het',0) +1
                elif spline[7].startswith('1/1'):
                    het_hom['hom'] =het_hom.get('hom',0) +1

                #delete insert
                if spline[8].startswith('deletion'):
                    delete = delete+1
                elif spline[8].startswith('insertion'):
                    insert = insert + 1

                #8 A3_R1_A3_R2_sort_realign_dedup_mate_recal_raw_snp_filtered_Hqual.csv
                if not spline[10].startswith('Gene_location'):
                    Gene_location[spline[10]] = Gene_location.get(spline[10],0)+1

                #10 Exon_syno
                if not spline[12].startswith('NA') and not spline[12].startswith('Exon_syno') :
                    Exon_syno[spline[12]] = Exon_syno.get(spline[12],0)+1

                #12 dbSNP
                if spline[14].startswith('rs') and not spline[14].startswith('dbSNP') :
                    dbSNP = dbSNP+1

                #13 1000G
                if not spline[15].startswith('NA') and not spline[15].startswith('1000G') :
                    G1000 = G1000+1

        with open(outcvs, 'w') as infile:
            infile.write('Variant Statistics Items\t'+ re.sub('_R1.*', '_indel', StringMeth().getPathName(Input_cvs)) +'\n')
            infile.write('High-confidence Indels number:\t'+ str(total_number-1) +'\n')
            infile.write('Deletion:\t'+str(delete)+'\n')
            infile.write('Insertion:\t'+str(insert)+'\n')

            infile.write('Heterozygosis:\t'+str(het_hom['het'])+'\n')
            infile.write('Homozygosis:\t'+str(het_hom['hom'])+'\n')
            infile.write('dbSNP:\t%s(%0.1f%%)\n'%(str(dbSNP),(dbSNP*100.0/(het_hom['het']+het_hom['hom']))))
            #infile.write('1000G:\t%s(%0.1f%%)\n'%(str(G1000),(G1000*100.0/(het_hom['het']+het_hom['hom']))))
            #Gene_location
            for element in sorted(Gene_location.keys()):
                infile.write(element+':\t'+str(Gene_location[element])+'\n')
            #Exon
            for element in sorted(Exon_syno.keys()):
                infile.write('Exon_'+element+':\t'+str(Exon_syno[element])+'\n')
        return outcvs




'''
Stats_Anotation('a').stats_snp('WGC000170_R1_human_WGC000170_R2_human_sort_realign_dedup_mate_recal_raw_snp_filtered_Hqual.csv')
Stats_Anotation('a').stats_indel('WGC000170_R1_human_WGC000170_R2_human_sort_realign_dedup_mate_recal_raw_indel_filtered_Hqual.csv')
'''



