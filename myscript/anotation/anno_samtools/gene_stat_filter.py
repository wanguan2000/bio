#!/usr/bin/env python
__author__ = 'wanguan2000'
# -*- coding: utf-8 -*-
import sys
import os.path
import os
import locale
import codecs
import re
from copy import deepcopy

class Stats_Exon_syno:
    def getindex(self, line, name):
        line = line.rstrip()
        if line.startswith('#CHROM'):
            chrom = line.split('\t')
        return chrom.index(name)


    def mutation_type_stats(self, filename, mutation_type, datatype):
        allmutation = dict([(x, 0) for x in mutation_type])
        pattern = re.compile('(,|;).*')
        gene_symbol = 0
        gene_syno = 0
        mygene = {}
        samplename = re.sub('_.*', '', os.path.splitext(os.path.basename(filename))[0])
        allgene = set()
        with open(filename, 'rU') as f:
            for line in f:
                line = line.rstrip()
                if not line:
                    break
                if not line.startswith('#CHROM'):
                    spline = line.split('\t')
                    re_dbsnp = (spline[dbsnp])
                    re_G1000 = (spline[G1000])
                    re_Conserve = (spline[Conserve])

                    try:
                        re_visift = float(spline[Visift])
                    except:
                        re_visift = 1.0
                    if datatype == 'snp':
                        #filter 1000G and visift
                        #if re_visift  < 0.05 and re_G1000.startswith('NA'):
                        if True:

                            if not 'NA' in spline[gene_syno]:
                                symbol_name = re.sub(pattern, '', spline[gene_symbol])
                                allgene.add(symbol_name)
                                mutationtype = spline[gene_syno]

                                if symbol_name in mygene:
                                    mygene[symbol_name][mutationtype] = mygene[symbol_name][mutationtype] + 1
                                else:
                                    mygene[symbol_name] = deepcopy(allmutation)
                                    mygene[symbol_name][mutationtype] = mygene[symbol_name][mutationtype] + 1
                    if datatype == 'indel':
                        #if re_G1000.startswith('NA'):
                        if True :
                            if not 'NA' in spline[gene_syno]:
                                symbol_name = re.sub(pattern, '', spline[gene_symbol])
                                allgene.add(symbol_name)
                                mutationtype = spline[gene_syno]

                                if symbol_name in mygene:
                                    mygene[symbol_name][mutationtype] = mygene[symbol_name][mutationtype] + 1
                                else:
                                    mygene[symbol_name] = deepcopy(allmutation)
                                    mygene[symbol_name][mutationtype] = mygene[symbol_name][mutationtype] + 1
                else:
                    gene_symbol = self.getindex(line, 'Gene')
                    gene_syno = self.getindex(line, 'Exon_syno')
                    dbsnp = self.getindex(line, 'dbSNP')
                    G1000 = self.getindex(line, '1000G')
                    Visift = self.getindex(line, 'Visift')
                    Conserve = self.getindex(line, 'ConservedElements')

        return samplename, allgene, mygene


    def pipeline(self, fileslist, datatype='snporindel',
                 mutation_type=['stopgain SNV', 'stoploss SNV', 'nonsynonymous SNV', 'synonymous SNV', 'unknown']):
        all_result = []
        #files = os.listdir('.')
        result_dict = {}
        result_samplename = []
        result_allgene = set()

        for dirname in fileslist:
            samplename, allgene, mygene = self.mutation_type_stats(dirname, mutation_type, datatype)
            result_samplename.append(samplename)
            result_allgene.update(allgene)
            result_dict[samplename] = mygene

        head2 = []
        head2.append('#gene')
        for samplename in result_samplename:
            for type in mutation_type:
                head2.append(samplename + '_' + type)
            #all_sample
        for type in mutation_type:
            head2.append('ALL_' + type)
        head2.append('Frequency_AminoAcid_change')
        all_result.append('\t'.join(head2))

        for gene in result_allgene:
            gene_stat = []
            gene_stat.append(gene)
            for samplename in result_samplename:
                if gene in result_dict[samplename]:
                    for type in mutation_type:
                        gene_stat.append(str(result_dict[samplename][gene][type]))
                else:
                    gene_stat.extend(['0'] * len(mutation_type))

            #allsample
            allsample = []
            for typelist in range(len(mutation_type)):
                allsample.append(str(sum([1  for elem in range(typelist, len(gene_stat) - 1, len(mutation_type)) if
                                          int(gene_stat[elem + 1]) > 0])))
            frequency = 0
            if datatype == 'snp':
                #mutation_type=['stopgain SNV', 'stoploss SNV', 'nonsynonymous SNV', 'synonymous SNV', 'unknown'])
                AminoAcid_change = [1, 2, 3] #add 0 gene name
            if datatype == 'indel':
                #mutation_type = ['stopgain SNV','stoploss SNV','frameshift deletion','frameshift insertion','nonframeshift deletion','nonframeshift insertion','unknown',]
                AminoAcid_change = [1, 2, 3, 4, 5, 6] #add 0 gene name
            aachangeSmaple = []
            for n in range(0, len(result_samplename)):
                aachangeSmaple.append([len(mutation_type) * n + elem for elem in AminoAcid_change])
            for a in aachangeSmaple:
                if sum([int(gene_stat.__getitem__(elem)) for elem in a]) > 0:
                    frequency = frequency + 1

            allsample.append(str(frequency))
            gene_stat.extend(allsample)
            all_result.append('\t'.join(gene_stat))
        return all_result



mypath = os.getcwd()
files = os.listdir('.')

snpfilelist = []
for dirname in files:
    if '_somatic_snp_Hqual.xls' in dirname:
        snpfilelist.append(dirname)
with open('snps_gene_allsample.xls', 'w') as infile:
    for a in Stats_Exon_syno().pipeline(snpfilelist, datatype='snp',
                                        mutation_type=['stopgain SNV', 'stoploss SNV', 'nonsynonymous SNV', 'synonymous SNV', 'unknown']):
        infile.write(a + '\n')


indelfilelist = []
for dirname in files:
    if '_somatic_indel_Hqual.xls' in dirname:
        indelfilelist.append(dirname)
with open('indel_gene_allsample.xls', 'w') as infile:
    for a in Stats_Exon_syno().pipeline(indelfilelist, datatype='indel', mutation_type=['stopgain SNV', 'stoploss SNV', 'frameshift deletion', 'frameshift insertion', 'nonframeshift deletion', 'nonframeshift insertion', 'unknown', ]):
        infile.write(a + '\n')

