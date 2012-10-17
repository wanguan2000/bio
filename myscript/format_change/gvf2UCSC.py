__author__ = 'wanguan2000'
#coding=utf-8
import os.path
import os
import sys
import re
import commands
ref = re.compile(r';Reference_seq=(.*)')
alt = re.compile(r';Variant_seq=(.*?);')
dbsnp = re.compile(r'Dbxref=dbSNP_132:(.*?);')


'''
['SNV', 'insertion', 'deletion', 'sequence_alteration', 'substitution']
['single', 'mnp', 'mixed', 'insertion', 'in-del', 'deletion', 'named']

dui={'SNV':'single','insertion':'insertion','deletion':'deletion','sequence_alteration':'in-del','substitution':'in-del'}

'''
def revsrse(a):
    code_dict={'A':'T','T':'A','C':'G','G':'C','-':'-'}
    try:
        b = ','.join([code_dict[a.upper()] for a in a.split(',')])
        return b
    except :
        print a
        raise SystemExit

def decode(a):
    p = re.compile(r'A|T|C|G',re.I)
    code_dict={'M':'A,C','R':'A,G','Y':'C,T','W':'A,T','S':'C,G','K':'G,T','N':'A,T,C,G','A':'A','T':'T','C':'C','G':'G','-':'-'}
    try:
        b = ','.join([code_dict[a.upper()] for a in a.split(',')])
        return b
    except :
        print a
        raise SystemExit



#Y	dbSNP	SNV	2536534	2536534	.	+	.	ID=15453674;Variant_seq=A;Dbxref=dbSNP_132:rs108145871;Reference_seq=G
def getSequece_fasta(bed,fasta='/gpfs2/home/wanguan2000/NGSToolkit/database_NGS/UCSCmm9/mm9.fasta'):
    with open('bedfile.bed','w') as f:
        f.write(bed+'\n')
    cmd='fastaFromBed -fi '+fasta+' -bed bedfile.bed -fo test.fa.out -tab;cat test.fa.out'
    result = commands.getstatusoutput(cmd)
    addDNA = result[1].split('\t')[-1]
    return addDNA

#print getSequece_fasta('chr2	143622377	143622378')



with open('Mus_musculus.gvf','rU') as f:
    for line in f:
        if not line.startswith('#'):
            line = line.rstrip()
            spline = line.split('\t')
            R = ref.findall(line)[0]
            A = alt.findall(line)[0]
            rssnp = dbsnp.findall(line)[0]

            if spline[6] == '+':
                a =['chr'+spline[0],spline[3],spline[4],rssnp,spline[6],R,A]
            elif spline[6] == '-':
                a =['chr'+spline[0],spline[3],spline[4],rssnp,spline[6],revsrse(R),revsrse(A)]

            if not 'deletion' in line and not 'insertion' in line and not 'sequence_alteration' in line and not 'substitution' in line:
                #print line
                #print '\t'.join(a)
                ALT= decode(a[6])
                snp = '\t'.join(['100',a[0],a[1],a[2],a[-2],a[-1],'.','PASS','.'])
                ucsc = ['100',a[0],str(int(a[1])-1),a[2],a[3],'0',a[4],a[5],a[5],str(a[5]+'/'+ALT),'genomic',spline[2],'unknown	0	0	unknown	exact	1']

                ucsc[9] = ucsc[9].replace(',','/')
                print '\t'.join(ucsc)
            else:
                snp = '\t'.join(['100',a[0],a[1],a[2],a[-2],a[-1],'.','PASS','.'])
                ucsc = ['100',a[0],str(int(a[1])-1),a[2],a[3],'0',a[4],a[5],a[5],str(a[5]+'/'+a[6]),'genomic',spline[2],'unknown	0	0	unknown	exact	1']
                ucsc[9] = ucsc[9].replace(',','/')
                print '\t'.join(ucsc)

