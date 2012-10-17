__author__ = 'wanguan2000'
# -*- coding: utf-8 -*-
import sys
import os
import locale
import codecs
import re
from myscript import *

class Stats_Anotation:
    def __init__(self, config):
        pass
        #self.const = config
    def getindex(self,line, somatic_samples):
        sample_index = {}
        line = line.rstrip()
        if line.startswith('#CHROM'):
            chrom = line.split('\t')
            for sample in somatic_samples:
                try:
                    sample_index[sample] = chrom.index(sample)
                except:
                    print sample, 'sample name RGSM not exist'
                    raise SystemExit
        return sample_index

    def stats_snp(self, Input_cvs,key_stats=['Genotype','Gene_location','Exon_syno','dbSNP']):
        ######data, software ,path  initialization#########
        outcvs = StringMeth().changeExtension(Input_cvs, '_stats.txt')
        het_hom={}
        Gene_location={}
        Exon_syno={}
        dbSNP = 0
        totalnumber = 0
        het = 0
        hom = 0


        with open(Input_cvs, 'rU') as f:
            for line in f:
                if not line:
                    break
                if line.startswith('#CHROM'):
                    key_stats=['Genotype','Gene_location','Exon_syno','dbSNP',]
                    sample_index = self.getindex(line,key_stats)
                else:
                   totalnumber = totalnumber +1
                   line = line.rstrip()
                   spline = line.split('\t')

                   #8 A3_R1_A3_R2_sort_realign_dedup_mate_recal_raw_snp_filtered_Hqual.csv
                   sample_index['Genotype']
                   sample_index['Gene_location']
                   sample_index['Exon_syno']
                   sample_index['dbSNP']


                   #het and hom
                   if spline[sample_index['Genotype']].startswith('het'):
                       het=het+1

                   if spline[sample_index['Genotype']].startswith('hom'):
                       hom=hom+1

                   #Gene_location
                   if not spline[sample_index['Gene_location']].startswith('Gene_location'):
                       Gene_location[spline[sample_index['Gene_location']]] = Gene_location.get(spline[sample_index['Gene_location']],0)+1

                   #10 Exon_syno
                   if not spline[sample_index['Exon_syno']].startswith('NA') and not spline[sample_index['Exon_syno']].startswith('Exon_syno') :
                       Exon_syno[spline[sample_index['Exon_syno']]] = Exon_syno.get(spline[sample_index['Exon_syno']],0)+1

                   #12 dbSNP
                   if spline[sample_index['dbSNP']].startswith('rs') and not spline[sample_index['dbSNP']].startswith('dbSNP') :
                       dbSNP = dbSNP+1


        with open(outcvs, 'w') as infile:
            infile.write('Variant Statistics Items\t'+ re.sub('_.*', '_ALL', StringMeth().getPathName(Input_cvs)) +'\n')
            infile.write('High-confidence SNPs number:\t'+ str(totalnumber) +'\n')
            infile.write('Heterozygotes:\t'+str(het)+'\n')
            infile.write('Homozygotes:\t'+str(hom)+'\n')
            infile.write('dbSNP:\t%s(%0.1f%%)\n'%(str(dbSNP),(dbSNP*100.0/(totalnumber))))
            #infile.write('1000G:\t%s(%0.1f%%)\n'%(str(G1000),(G1000*100.0/(totalnumber))))
            #Gene_location
            for element in sorted(Gene_location.keys()):
                infile.write(element+':\t'+str(Gene_location[element])+'\n')
            #Exon
            for element in sorted(Exon_syno.keys()):
                infile.write('Exon_'+element+':\t'+str(Exon_syno[element])+'\n')
        return outcvs



    def stats_indel(self, Input_cvs,key_stats=['Genotype','Gene_location','Exon_syno','dbSNP']):
        ######data, software ,path  initialization#########
        outcvs = StringMeth().changeExtension(Input_cvs, '_stats.txt')
        het_hom={}
        Gene_location={}
        Exon_syno={}
        dbSNP = 0
        totalnumber = 0
        delete = 0
        insert = 0
        het = 0
        hom = 0
    
        with open(Input_cvs, 'rU') as f:
            for line in f:
                if not line:
                    break
                if line.startswith('#CHROM'):
                    key_stats=['Variation_type','Genotype','Gene_location','Exon_syno','dbSNP','Variation_type']
                    sample_index = self.getindex(line,key_stats)
                else:
                   totalnumber = totalnumber +1
                   line = line.rstrip()
                   spline = line.split('\t')

                   #8 A3_R1_A3_R2_sort_realign_dedup_mate_recal_raw_snp_filtered_Hqual.csv
                   sample_index['Variation_type']
                   sample_index['Genotype']
                   sample_index['Gene_location']
                   sample_index['Exon_syno']
                   sample_index['dbSNP']
                   sample_index['Variation_type']

                   #delete insert
                   if spline[sample_index['Variation_type']].startswith('deletion'):
                        delete = delete+1
                   elif spline[sample_index['Variation_type']].startswith('insertion'):
                        insert = insert + 1

                   #het and hom
                   if spline[sample_index['Genotype']].startswith('het'):
                       het=het+1

                   if spline[sample_index['Genotype']].startswith('hom'):
                       hom=hom+1

                   #Gene_location
                   if not spline[sample_index['Gene_location']].startswith('Gene_location'):
                       Gene_location[spline[sample_index['Gene_location']]] = Gene_location.get(spline[sample_index['Gene_location']],0)+1

                   #10 Exon_syno
                   if not spline[sample_index['Exon_syno']].startswith('NA') and not spline[sample_index['Exon_syno']].startswith('Exon_syno') :
                       Exon_syno[spline[sample_index['Exon_syno']]] = Exon_syno.get(spline[sample_index['Exon_syno']],0)+1

                   #12 dbSNP
                   if spline[sample_index['dbSNP']].startswith('rs') and not spline[sample_index['dbSNP']].startswith('dbSNP') :
                       dbSNP = dbSNP+1



        with open(outcvs, 'w') as infile:
            infile.write('Variant Statistics Items\t'+ re.sub('_.*', '_ALL', StringMeth().getPathName(Input_cvs)) +'\n')
            infile.write('High-confidence Indels number:\t'+ str(totalnumber) +'\n')
            infile.write('Delete:\t'+str(delete)+'\n')
            infile.write('Insert:\t'+str(insert)+'\n')
            infile.write('Heterozygotes:\t'+str(het)+'\n')
            infile.write('Homozygotes:\t'+str(hom)+'\n')
            infile.write('dbSNP:\t%s(%0.1f%%)\n'%(str(dbSNP),(dbSNP*100.0/(totalnumber))))
            #infile.write('1000G:\t%s(%0.1f%%)\n'%(str(G1000),(G1000*100.0/(totalnumber))))
            #Gene_location
            for element in sorted(Gene_location.keys()):
                infile.write(element+':\t'+str(Gene_location[element])+'\n')
            #Exon
            for element in sorted(Exon_syno.keys()):
                infile.write('Exon_'+element+':\t'+str(Exon_syno[element])+'\n')
        return outcvs

    def stats_snp_muti(self, Input_cvs,key_stats=['Genotype','Gene_location','Exon_syno','dbSNP']):
        ######data, software ,path  initialization#########
        outcvs = StringMeth().changeExtension(Input_cvs, '_stats.txt')
        het_hom={}
        Gene_location={}
        Exon_syno={}
        dbSNP = 0
        totalnumber = 0



        with open(Input_cvs, 'rU') as f:
            for line in f:
                if not line:
                    break
                if line.startswith('#CHROM'):
                    key_stats=['Genotype','Gene_location','Exon_syno','dbSNP',]
                    sample_index = self.getindex(line,key_stats)
                else:
                    totalnumber = totalnumber +1
                    line = line.rstrip()
                    spline = line.split('\t')

                    #8 A3_R1_A3_R2_sort_realign_dedup_mate_recal_raw_snp_filtered_Hqual.csv
                    sample_index['Genotype']
                    sample_index['Gene_location']
                    sample_index['Exon_syno']
                    sample_index['dbSNP']


                    #Gene_location
                    if not spline[sample_index['Gene_location']].startswith('Gene_location'):
                        Gene_location[spline[sample_index['Gene_location']]] = Gene_location.get(spline[sample_index['Gene_location']],0)+1

                    #10 Exon_syno
                    if not spline[sample_index['Exon_syno']].startswith('NA') and not spline[sample_index['Exon_syno']].startswith('Exon_syno') :
                        Exon_syno[spline[sample_index['Exon_syno']]] = Exon_syno.get(spline[sample_index['Exon_syno']],0)+1

                    #12 dbSNP
                    if spline[sample_index['dbSNP']].startswith('rs') and not spline[sample_index['dbSNP']].startswith('dbSNP') :
                        dbSNP = dbSNP+1


        with open(outcvs, 'w') as infile:
            infile.write('Variant Statistics Items\t'+ re.sub('_.*', '_ALL', StringMeth().getPathName(Input_cvs)) +'\n')
            infile.write('High-confidence SNPs number:\t'+ str(totalnumber) +'\n')
            infile.write('dbSNP:\t%s(%0.1f%%)\n'%(str(dbSNP),(dbSNP*100.0/(totalnumber))))
            #infile.write('1000G:\t%s(%0.1f%%)\n'%(str(G1000),(G1000*100.0/(totalnumber))))
            #Gene_location
            for element in sorted(Gene_location.keys()):
                infile.write(element+':\t'+str(Gene_location[element])+'\n')
                #Exon
            for element in sorted(Exon_syno.keys()):
                infile.write('Exon_'+element+':\t'+str(Exon_syno[element])+'\n')
        return outcvs



    def stats_indel_muti(self, Input_cvs,key_stats=['Genotype','Gene_location','Exon_syno','dbSNP']):
        ######data, software ,path  initialization#########
        outcvs = StringMeth().changeExtension(Input_cvs, '_stats.txt')
        het_hom={}
        Gene_location={}
        Exon_syno={}
        dbSNP = 0
        totalnumber = 0
        delete = 0
        insert = 0


        with open(Input_cvs, 'rU') as f:
            for line in f:
                if not line:
                    break
                if line.startswith('#CHROM'):
                    key_stats=['Variation_type','Genotype','Gene_location','Exon_syno','dbSNP','Variation_type']
                    sample_index = self.getindex(line,key_stats)
                else:
                    totalnumber = totalnumber +1
                    line = line.rstrip()
                    spline = line.split('\t')

                    #8 A3_R1_A3_R2_sort_realign_dedup_mate_recal_raw_snp_filtered_Hqual.csv
                    sample_index['Variation_type']
                    sample_index['Genotype']
                    sample_index['Gene_location']
                    sample_index['Exon_syno']
                    sample_index['dbSNP']
                    sample_index['Variation_type']

                    #delete insert
                    if spline[sample_index['Variation_type']].startswith('deletion'):
                        delete = delete+1
                    elif spline[sample_index['Variation_type']].startswith('insertion'):
                        insert = insert + 1


                    #Gene_location
                    if not spline[sample_index['Gene_location']].startswith('Gene_location'):
                        Gene_location[spline[sample_index['Gene_location']]] = Gene_location.get(spline[sample_index['Gene_location']],0)+1

                    #10 Exon_syno
                    if not spline[sample_index['Exon_syno']].startswith('NA') and not spline[sample_index['Exon_syno']].startswith('Exon_syno') :
                        Exon_syno[spline[sample_index['Exon_syno']]] = Exon_syno.get(spline[sample_index['Exon_syno']],0)+1

                    #12 dbSNP
                    if spline[sample_index['dbSNP']].startswith('rs') and not spline[sample_index['dbSNP']].startswith('dbSNP') :
                        dbSNP = dbSNP+1



        with open(outcvs, 'w') as infile:
            infile.write('Variant Statistics Items\t'+ re.sub('_.*', '_ALL', StringMeth().getPathName(Input_cvs)) +'\n')
            infile.write('High-confidence Indels number:\t'+ str(totalnumber) +'\n')
            infile.write('Delete:\t'+str(delete)+'\n')
            infile.write('Insert:\t'+str(insert)+'\n')
            infile.write('dbSNP:\t%s(%0.1f%%)\n'%(str(dbSNP),(dbSNP*100.0/(totalnumber))))
            #infile.write('1000G:\t%s(%0.1f%%)\n'%(str(G1000),(G1000*100.0/(totalnumber))))
            #Gene_location
            for element in sorted(Gene_location.keys()):
                infile.write(element+':\t'+str(Gene_location[element])+'\n')
                #Exon
            for element in sorted(Exon_syno.keys()):
                infile.write('Exon_'+element+':\t'+str(Exon_syno[element])+'\n')
        return outcvs



'''
Stats_Anotation('a').stats_snp('WGC000139_R1_human_WGC000139_R2_human_sort_realign_dedup_mate_recal_raw_snp_filtered_Hqual.csv')
Stats_Anotation('a').stats_indel('WGC000139_R1_human_WGC000139_R2_human_sort_realign_dedup_mate_recal_raw_indel_filtered_Hqual.csv')
'''
