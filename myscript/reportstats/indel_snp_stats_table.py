#coding=utf-8
import sys
import re
import os.path
import os
import copy



def merge(files,name):
    files.sort()
    result_dict=dict([(a,[]) for a in name])
    for file in files:
        mydict = dict([(a,'0') for a in name])
        with open(file,'rU') as f:
            for line in f:
                line = line.rstrip()
                spline = line.split('\t')
                if spline[0] in mydict:
                    mydict[spline[0]] = spline[1]
        for a in name:
            result_dict[a]=result_dict[a]+[mydict[a]]
    return result_dict





indel_name = ['Variant Statistics Items','High-confidence Indels number:','Delete:','Insert:','Heterozygotes:','Homozygotes:','dbSNP:','1000G:','UTR3:','UTR5:','UTR5;UTR3:','downstream:','exonic:','exonic;splicing:','intergenic:','intronic:','ncRNA_UTR3:','ncRNA_UTR5:','ncRNA_exonic:','ncRNA_intronic:','ncRNA_splicing:','splicing:','upstream:','upstream;downstream:','Exon_frameshift deletion:','Exon_frameshift insertion:','Exon_nonframeshift deletion:','Exon_nonframeshift insertion:','Exon_stopgain SNV:','Exon_stoploss SNV:','Exon_unknown:']
snp_name = ['Variant Statistics Items','High-confidence SNPs number:','Heterozygotes:','Homozygotes:','dbSNP:','1000G:','UTR3:','UTR5:','UTR5;UTR3:','downstream:','exonic:','exonic;splicing:','intergenic:','intronic:','ncRNA_UTR3:','ncRNA_UTR5:','ncRNA_exonic:','ncRNA_intronic:','ncRNA_splicing:','splicing:','upstream:','upstream;downstream:','Exon_nonsynonymous SNV:','Exon_stopgain SNV:','Exon_stoploss SNV:','Exon_synonymous SNV:','Exon_unknown:']
indel_file=[]
snp_file=[]

files = os.listdir('.')
for dirname in files:
    if not os.path.isdir(dirname) and not dirname.startswith('.') and not '~' in dirname and dirname.endswith('_stats.txt'):
        if dirname.endswith('indel_filtered_Hqual_stats.txt'):
            indel_file = indel_file+[dirname]
        elif dirname.endswith('snp_filtered_Hqual_stats.txt'):
            snp_file = snp_file+[dirname]


indel_result = merge(indel_file,indel_name)
snp_result = merge(snp_file,snp_name)

with open('indel_snp_stats.txt','w') as f:
    for a in indel_name:
        f.write(a+'\t'+'\t'.join(indel_result[a])+'\n')
    f.write('>snp'+'\n')
    for a in snp_name:
        f.write(a+'\t'+'\t'.join(snp_result[a])+'\n')




