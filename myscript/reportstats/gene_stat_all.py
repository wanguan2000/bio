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

    def getindex(self,line, name):
        line = line.rstrip()
        if line.startswith('#CHROM'):
            chrom = line.split('\t')
        return chrom.index(name)


    def mutation_type_stats(self,filename,mutation_type):
        allmutation = dict([(x, 0) for x in mutation_type])
        pattern = re.compile('(,|;).*')
        gene_symbol = 0
        gene_syno = 0
        mygene={}
        samplename  = re.sub('_.*', '', os.path.splitext(os.path.basename(filename))[0])
        allgene=set()
        with open(filename, 'rU') as f:
             for line in f:
                 line = line.rstrip()
                 if not line:
                     break
                 if not line.startswith('#CHROM'):
                     spline = line.split('\t')
                     if not 'NA' in spline[gene_syno]:
                         symbol_name = re.sub(pattern, '', spline[gene_symbol])
                         allgene.add(symbol_name)
                         mutationtype = spline[gene_syno]
                         
                         if symbol_name in mygene:
                             mygene[symbol_name][mutationtype] = mygene[symbol_name][mutationtype]+1
                         else:
                             mygene[symbol_name] = deepcopy(allmutation)
                             mygene[symbol_name][mutationtype] = mygene[symbol_name][mutationtype]+1

                 else:
                     gene_symbol=self.getindex(line,'Gene')
                     gene_syno = self.getindex(line,'Exon_syno')
        return samplename,allgene,mygene

    

    def pipeline(self,fileslist,mutation_type = ['stopgain SNV','stoploss SNV','nonsynonymous SNV','synonymous SNV','unknown']):
        all_result=[]
        #files = os.listdir('.')
        result_dict = {}
        result_samplename=[]
        result_allgene=set()

        for dirname in fileslist:
            samplename,allgene,mygene = self.mutation_type_stats(dirname,mutation_type)
            result_samplename.append(samplename)
            result_allgene.update(allgene)
            result_dict[samplename]=mygene

        head2=[]
        head2.append('#gene')
        for samplename in result_samplename:
            for type in mutation_type:
                head2.append(samplename+'_'+type)
        #all_sample
        for type in mutation_type:
            head2.append('ALL_'+type)

        all_result.append('\t'.join(head2))
        
        for gene in result_allgene:
            gene_stat=[]
            gene_stat.append(gene)
            for samplename in result_samplename:
                if gene in result_dict[samplename]:
                    for type in mutation_type:
                        gene_stat.append(str(result_dict[samplename][gene][type]))
                else:
                    gene_stat.extend(['0']*len(mutation_type))
                    
            #allsample
            allsample = []
            for typelist in range(len(mutation_type)):
                allsample.append(str(sum([1  for elem in range(typelist,len(gene_stat)-1,len(mutation_type)) if int(gene_stat[elem+1])>0])))
            gene_stat.extend(allsample)
            all_result.append('\t'.join(gene_stat))
        return all_result

'''
#snp
fileslist=['WGC000184_R1_WGC000184_R2_sort_realign_dedup_mate_recal_raw_snp_filtered_Hqual.csv','WGC000185_R1_WGC000185_R2_sort_realign_dedup_mate_recal_raw_snp_filtered_Hqual.csv']
for a in Stats_Exon_syno().pipeline(fileslist,mutation_type = ['stopgain SNV','stoploss SNV','nonsynonymous SNV','synonymous SNV','unknown']):
    print a

#indel
fileslist=['WGC000184_R1_WGC000184_R2_sort_realign_dedup_mate_recal_raw_indel_filtered_Hqual.csv','WGC000185_R1_WGC000185_R2_sort_realign_dedup_mate_recal_raw_indel_filtered_Hqual.csv']
for a in Stats_Exon_syno().pipeline(fileslist,mutation_type = ['stopgain SNV','stoploss SNV','frameshift deletion','frameshift insertion','nonframeshift deletion','nonframeshift insertion','unknown',]):
    print a
'''
