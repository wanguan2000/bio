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

#chr15	57990354	rs4230749	tG	t(16 BP DEL)	.	PASS	.


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
            #print line

            if spline[6] == '+':
                a =['chr'+spline[0],spline[3],spline[4],rssnp,spline[6],R,A]
            elif spline[6] == '-':
                a =['chr'+spline[0],spline[3],spline[4],rssnp,spline[6],revsrse(R),revsrse(A)]

            if not 'deletion' in line and not 'insertion' in line and not 'sequence_alteration' in line and not 'substitution' in line :
                #print line
                #print '\t'.join(a)
                ALT= decode(a[-1])
                snp = '\t'.join([a[0],a[1],a[3],a[-2],ALT,'.','PASS','.'])
                print snp
            else:
                #['chr18', '20833523', '20833523']    print a[0:3]
                addDNA = getSequece_fasta('\t'.join([a[0],str(int(a[1])-2),str(int(a[1])-1)]))
                #print addDNA

                R2 =addDNA+a[-2]
                R2 = R2.replace('-','')

                A2 = ','.join([addDNA+l for l in a[-1].split(',')])
                A2 = A2.replace('-','')
                
                okresult = ('\t'.join(a)+'\t'+R2+'\t'+A2+'\t'+str(int(a[1])-1)).split('\t')
                #ALT= decode(okresult[-2])
                vcf_result = '\t'.join([okresult[0],okresult[-1],okresult[3],okresult[-3],okresult[-2],'.','PASS','.'])
                print vcf_result






#sequence_alteration


#fastaFromBed -fi test.fa -bed test.bed -s -name -fo test.fa.out

#/gpfs2/home/wanguan2000/NGSToolkit/database_NGS/UCSCmm9/mm9.fasta



