__author__ = 'wanguan2000'
# -*- coding: utf-8 -*-
import sys
import os
import locale
import codecs
import re
from myscript import *

'''
do vcf annotation

####input####
input (self,Input_vcf,meth='snp;indel'):
#######

java -Xmx4g -jar ./picard-tools-1.48/SamFormatConverter.jar \
   INPUT= ./testdata/31bwa.sam \
   OUTPUT= ./testdata/31bwa.bam \
   VALIDATION_STRINGENCY=LENIENT

####return####
return Input_vcf.cvs

'''

'''
###############convert2annovar##############
./convert2annovar.pl i951681B_snp.vcf -format vcf4 >i951681B_snp.human
./convert2annovar.pl i951681B_indel.vcf -format vcf4 >i951681B_indel.human

###############gene annotation#############
./annotate_variation.pl -geneanno --buildver hg19 -dbtype refgene ./1/i951681B_snp.human humandb/
./annotate_variation.pl -geneanno --buildver hg19 -dbtype refgene ./2/i951681B_indel.human humandb/

##########dbsnp135################
./annotate_variation.pl --buildver hg19 -filter -dbtype snp135 ./1/i951681B_snp.human humandb/
./annotate_variation.pl --buildver hg19 -filter -dbtype snp135 ./2/i951681B_indel.human humandb/
###########1000 Genomes Project (2010 March/July/November and 2011 release) annotations ################

./annotate_variation.pl --buildver hg19 -filter -dbtype 1000g2011may_all ./1/i951681B_snp.human humandb/
./annotate_variation.pl --buildver hg19 -filter -dbtype 1000g2011may_all ./2/i951681B_indel.human humandb/
./annotate_variation.pl --buildver hg19 -filter -dbtype 1000g2012feb_all ./2/i951681B_indel.human humandb/

#hg19_ALL.sites.2011_05.txt

###########Identify variants reported in previously published GWAS (Genome-wide association studies) ##################
annotate_variation.pl -regionanno -dbtype gwascatalog ex1.human humandb/
./annotate_variation.pl --buildver hg19 -regionanno -dbtype gwascatalog ./1/i951681B_snp.human humandb/
./annotate_variation.pl --buildver hg19 -regionanno -dbtype gwascatalog ./2/i951681B_indel.human humandb/

###########visift#################
./annotate_variation.pl --buildver hg19 -filter -dbtype avsift ./1/i951681B_snp.human humandb/ -sift 0
./annotate_variation.pl --buildver hg19 -filter -dbtype avsift ./2/i951681B_indel.human humandb/ -sift 0

##############PolyPhen2, MutationTaster, LRT, PhyloP###################

##############tfbs###################
./annotate_variation.pl --buildver hg19 -dbtype tfbs -regionanno ./data/ST_Hqual_snp.human humandb/

################mirna###########
./annotate_variation.pl --buildver hg19 -dbtype mirna -regionanno ./data/ST_Hqual_snp.human humandb/

##################mirnatarget############
./annotate_variation.pl --buildver hg19 -dbtype mirnatarget -regionanno ./data/ST_Hqual_snp.human humandb/

######################dgv ANNOVAR can also conveniently annotate deletions and duplications and compare them to previously published variants.####
annotate_variation.pl --buildver hg19 -regionanno -dbtype dgv ./data/ST_Hqual_snp.human humandb/ -minqueryfrac 0.5

###########mce46 annotate variants that fall within conserved genomic regions###########
annotate_variation.pl --buildver hg19 -regionanno -dbtype mce46way ./data/ST_Hqual_snp.human humandb/


####################cosmic#
./annotate_variation.pl ST_Hqual_snp.human . -gff3dbfile cosmic.gff3 -dbtype gff3 -regionanno


'''

class Annovar:
    def __init__(self, config):
        self.const = config

    def ALT_Ratio(self,a):
        #0/1:10,11:21:99:474,0,545
        pattern = re.compile('\d\/\d:\d+,(.*?):(\d+):')
        match = re.search(pattern, a)
        #alt_count = float(match.group(1))
        alt_count =sum([int(a) for a in (match.group(1)).split(',')])


        dp_count = float(match.group(2))
        jieguo = ('%0.0f%%' % (alt_count*100.0/(dp_count)))
        return jieguo
    
    def vcf_anotation(self, Input_vcf, meth='snp;indel'):
        ######data, software ,path  initialization#########
        const = self.const
        #annovar = const.annovar
        annovar = '/gpfs/home/wanguan2000/NGSToolkit/software_NGS/annovar20120401/'


        ######!data, software ,path  initialization#########
        if meth == 'snp':
            snp_Hqual = self.filterVCF(Input_vcf, suffix='_Hqual.vcf')
            self.geneAnnotation(snp_Hqual, annovar)
            #########result######
            [mydict,key_list,vcf_head] = self.csv_snp_indel(snp_Hqual,'snp')
            result_SNP = StringMeth().changeExtension(snp_Hqual, '.csv')

            vcf_head[1] = 'Start'
            vcf_head.insert(2,'End')

            head_snp = '\t'.join(vcf_head) + '\tALT_ratio\tVariation_type\tGenotype\tGene_location\tGene\tExon_syno\tExon\tdbSNP\t1000G\tGWAS\tVisift\tTFbs\tMirna\tMirnatarget\tConservedElements\tcosmic'
            with open(result_SNP, mode='w') as f:
                f.write(head_snp + '\n')
                for mykey in key_list:
                    spline = mydict[mykey].split('\t')
                    spline.insert(1,spline[1])
                    try:
                        ALT_ratio = self.ALT_Ratio(spline[7])
                    except:
                        ALT_ratio='NA'
                    spline.insert(8,ALT_ratio)
                    spline.insert(9,'SNP')


                    if spline[7].startswith('1/1'):
                        spline.insert(10,'hom')
                    elif spline[7].startswith('0/1'):
                        spline.insert(10,'het')
                    else:
                        spline.insert(10,'unknow')

                    f.write('\t'.join(spline) + '\n')


            return result_SNP
        
        elif meth == 'indel':
            indel_Hqual = self.filterVCF(Input_vcf, suffix='_Hqual.vcf')
            self.geneAnnotation(indel_Hqual, annovar)

            #########result######
            [mydict,key_list,vcf_head] = self.csv_snp_indel(indel_Hqual,'indel')
            result_indel = StringMeth().changeExtension(indel_Hqual, '.csv')

            vcf_head[1] = 'Start'
            vcf_head.insert(2,'End')

            head_snp = '\t'.join(vcf_head) + '\tALT_ratio\tVariation_type\tGenotype\tGene_location\tGene\tExon_syno\tExon\tdbSNP\t1000G\tGWAS\tVisift\tTFbs\tMirna\tMirnatarget\tConservedElements\tcosmic'
            with open(result_indel, mode='w') as f:
                f.write(head_snp + '\n')
                for mykey in key_list:
                    spline = mydict[mykey].split('\t')
                    spline.insert(1,spline[1])
                    spline[2] = str(int(spline[1])+len(spline[3])-1)

                    try:
                        ALT_ratio = self.ALT_Ratio(spline[7])
                    except:
                        ALT_ratio='NA'
                    spline.insert(8,ALT_ratio)

                    if spline[3].startswith('-'):
                        spline.insert(9,'insertion')
                    else:
                        spline.insert(9,'deletion')


                    if spline[7].startswith('1/1'):
                        spline.insert(10,'hom')
                    elif spline[7].startswith('0/1'):
                        spline.insert(10,'het')
                    else:
                        spline.insert(10,'unknow')

                    f.write('\t'.join(spline) + '\n')
            return result_indel
            


    
    ####methods
    def filterVCF(self, filename, suffix='_Hqual.vcf'):
        outvcf = StringMeth().changeExtension(filename, suffix)
        with open(filename, 'rU') as f:
            with open(outvcf, 'w') as infile:
                for line in f:
                    if not line:
                        break
                    line = line.rstrip()
                    if not line.startswith('#'):
                        if not 'LowQual' in line and not 'TruthSensitivityTranche' in line:
                            infile.write(line + '\n')
                    else:
                        infile.write(line + '\n')
        return outvcf

    def geneAnnotation(self, filename, annovar, species='hg19', gene='refgene', database='humandb/', dnsnp='snp135',
                       G1000='1000g2012feb_all', gwas='gwascatalog', avsift='avsift', tfbs='tfbs', mirna='mirna',
                       mirnatarget='mirnatarget', mce46way='mce46way',cosmic='cosmic.gff3'):
        #vcf2human
        outhuman = StringMeth().changeExtension(filename, '.human')
        cmd = ' '.join([annovar + 'convert2annovar.pl', filename, '-format vcf4', '>' + outhuman])
        print cmd
        os.system(cmd)

        ##gene annotation .variant_function .exonic_variant_function
        cmd = ' '.join([annovar + 'annotate_variation.pl', '-geneanno --buildver', species, '-dbtype', gene, outhuman,
                        annovar + database])
        print cmd
        os.system(cmd)

        #dbsnp
        cmd = ' '.join([annovar + 'annotate_variation.pl', '--buildver', species, '-filter', '-dbtype', dnsnp, outhuman,
                        annovar + database])
        #filename+'.hg19_snp135_dropped'
        print cmd
        os.system(cmd)

        ##1000G
        cmd = ' '.join([annovar + 'annotate_variation.pl', '--buildver', species, '-filter', '-dbtype', G1000, outhuman,
                        annovar + database])
        #filename+'.hg19_snp135_dropped'
        print cmd
        os.system(cmd)

        ##GWAS
        cmd = ' '.join(
            [annovar + 'annotate_variation.pl', '--buildver', species, '-regionanno', '-dbtype', gwas, outhuman,
             annovar + database])
        #filename+'.hg19_ALL.sites.2011_05_dropped'
        print cmd
        os.system(cmd)

        ##visift ./annotate_variation.pl --buildver hg19 -filter -dbtype avsift ./1/i951681B_snp.human humandb/ -sift 0
        cmd = ' '.join(
            [annovar + 'annotate_variation.pl', '--buildver', species, '-filter', '-dbtype', avsift, outhuman,
             annovar + database, '-sift 0'])
        #filename+'.hg19_snp135_dropped'
        print cmd
        os.system(cmd)

        ##tfbs ./annotate_variation.pl --buildver hg19 -dbtype tfbs -regionanno ./data/ST_Hqual_snp.human humandb/
        cmd = ' '.join(
            [annovar + 'annotate_variation.pl', '--buildver', species, '-dbtype', tfbs, '-regionanno',
             outhuman, annovar + database])
        #filename+'.hg19_snp135_dropped'
        print cmd
        os.system(cmd)

        ##mirna ./annotate_variation.pl --buildver hg19 -dbtype mirna -regionanno ./data/ST_Hqual_snp.human humandb/
        cmd = ' '.join(
            [annovar + 'annotate_variation.pl', '--buildver', species, '-dbtype', mirna, '-regionanno',
             outhuman, annovar + database])
        #filename+'.hg19_snp135_dropped'
        print cmd
        os.system(cmd)

        ##mirnatarget ./annotate_variation.pl --buildver hg19 -dbtype mirnatarget -regionanno ./data/ST_Hqual_snp.human humandb/
        cmd = ' '.join(
            [annovar + 'annotate_variation.pl', '--buildver', species, '-dbtype', mirnatarget, '-regionanno',
             outhuman, annovar + database])
        #filename+'.hg19_snp135_dropped'
        print cmd
        os.system(cmd)

        ##mce46way ./annotate_variation.pl --buildver hg19 -regionanno -dbtype mce46way ./data/ST_Hqual_snp.human humandb/
        cmd = ' '.join(
            [annovar + 'annotate_variation.pl', '--buildver', species,'-dbtype', mce46way, '-regionanno',
             outhuman, annovar + database])
        #filename+'.hg19_snp135_dropped'
        print cmd
        os.system(cmd)


        ##cosmic ./annotate_variation.pl ST_Hqual_snp.human . -gff3dbfile cosmic.gff3 -dbtype gff3 -regionanno
        cmd = ' '.join([annovar + 'annotate_variation.pl', '--buildver',species,'-dbtype','gff3','-regionanno','-gff3dbfile',cosmic,outhuman,annovar+database])
        #filename+'human.hg19_gff3'
        print cmd
        os.system(cmd)

        return None





    def seletVCF_snp(self,filename, rootkey=[0, 1, 3, ]):
        mydict = {}
        key_list=[]
        result=[]
        vcf_head=[]

        with open(filename, 'rU') as f:
            for line in f:
                line = line.rstrip()
                if not line:
                    break
                if not line.startswith('#'):
                    spline = line.split('\t')
                    mykey = '\t'.join([spline.__getitem__(elem) for elem in rootkey])
                    key_list.append(mykey)
                    mydict[mykey] = '\t'.join([spline.__getitem__(elem) for elem in result])
                elif line.startswith('#CHROM'):
                    spline = line.split('\t')
                    result=range(0,len(spline))
                    result.remove(2)
                    result.remove(6)
                    result.remove(7)
                    vcf_head = [spline.__getitem__(elem) for elem in result]

        return [mydict,key_list,vcf_head]

    
    def bedMarge(self,filename, rootkey=[2, 3, 5, 6], result=[1],mydict={}):
        if mydict:
            for mykey in mydict:
                mydict[mykey] = mydict[mykey] +'\tNA'*len(result)

        with open(filename, 'rU') as f:
            for line in f:
                line = line.rstrip()
                if not line:
                    break
                spline = line.split('\t')
                mykey = '\t'.join([spline.__getitem__(elem) for elem in rootkey])
                if not mydict.get(mykey, ):
                    mydict[mykey] = '\t'.join([spline.__getitem__(elem) for elem in result])
                else:
                    mydict[mykey] = '\t'.join(mydict[mykey].split('\t')[0:-len(result)]) + '\t' + '\t'.join(
                        [spline.__getitem__(elem) for elem in result])
        return mydict


    def csv_snp_indel(self,HqualVCF,meth='snpindel'):
        if meth == 'snp':
            ##vcf
            [mydict,key_list,vcf_head] = self.seletVCF_snp(HqualVCF)
        elif meth == 'indel':
            ##vcf
            [mydict,key_list,vcf_head] = self.seletVCF_indel(HqualVCF)


        ##gene
        gene = StringMeth().changeExtension(HqualVCF, '.human.variant_function')
        rootkey = [2, 3, 5]
        result = [0, 1]
        mydict = self.bedMarge(gene, rootkey, result, mydict)

        ##exon
        exon = StringMeth().changeExtension(HqualVCF, '.human.exonic_variant_function')
        rootkey = [3, 4, 6,]
        result = [1, 2]
        mydict = self.bedMarge(exon, rootkey, result, mydict)

        ###dbsnp135##
        dbsnp = StringMeth().changeExtension(HqualVCF, '.human.hg19_snp135_dropped')
        rootkey = [2, 3, 5, ]
        result = [1]
        mydict = self.bedMarge(dbsnp, rootkey, result, mydict)

        ##1000G
        G1000 = StringMeth().changeExtension(HqualVCF, '.human.hg19_ALL.sites.2012_02_dropped')
        rootkey = [2, 3, 5,]
        result = [1]
        mydict = self.bedMarge(G1000, rootkey, result, mydict)

        ##GWAS
        GWAS = StringMeth().changeExtension(HqualVCF, '.human.hg19_gwasCatalog')
        rootkey = [2, 3, 5,]
        result = [1]
        mydict = self.bedMarge(GWAS, rootkey, result, mydict)

        ##visift
        visift = StringMeth().changeExtension(HqualVCF, '.human.hg19_avsift_dropped')
        rootkey = [2, 3, 5,]
        result = [1]
        mydict = self.bedMarge(visift, rootkey, result, mydict)

        ##tfbs
        tfbs = StringMeth().changeExtension(HqualVCF, '.human.hg19_tfbsConsSites')
        rootkey = [2, 3, 5,]
        result = [1]
        mydict = self.bedMarge(tfbs, rootkey, result, mydict)
        
        ##mirna
        mirna = StringMeth().changeExtension(HqualVCF, '.human.hg19_wgRna')
        rootkey = [2, 3, 5,]
        result = [1]
        mydict = self.bedMarge(mirna, rootkey, result, mydict)

        ##mirnatarget
        mirnatarget = StringMeth().changeExtension(HqualVCF, '.human.hg19_targetScanS')
        rootkey = [2, 3, 5,]
        result = [1]
        mydict = self.bedMarge(mirnatarget, rootkey, result, mydict)

        ##mce46way
        mce46way = StringMeth().changeExtension(HqualVCF, '.human.hg19_phastConsElements46way')
        rootkey = [2, 3, 5,]
        result = [1]
        mydict = self.bedMarge(mce46way, rootkey, result, mydict)

        ##cosmic
        cosmic = StringMeth().changeExtension(HqualVCF, '.human.hg19_gff3')
        rootkey = [2, 3, 5,]
        result = [1]
        mydict = self.bedMarge(cosmic, rootkey, result, mydict)

        return [mydict,key_list,vcf_head]


    def seletVCF_indel(self, filename):
        mydict = {}
        key_list=[]
        result=[]
        vcf_head=[]
        with open(filename, 'rU') as f:
            for line in f:
                line = line.rstrip()
                if not line:
                    break
                if not line.startswith('#'):
                    spline = line.split('\t')
                    chr = spline[0]
                    stat = int(spline[1])
                    end = 0
                    ref = spline[3]
                    alt = spline[4]

                    if len(spline[3]) > 1:
                        #delete
                        stat = stat+1
                        strinfo = re.compile('^'+alt)
                        ref = strinfo.sub('',ref)
                        alt = '-'
                        end = stat+len(ref)-1
                    else:
                        #insert
                        strinfo = re.compile('^'+ref)
                        alt = strinfo.sub('',alt)
                        ref = '-'
                        end = stat

                    spline[3] = ref
                    spline[4] = alt
                    spline[1] = str(stat)

                    mykey = '\t'.join([chr,str(stat),ref,])
                    key_list.append(mykey)
                    mydict[mykey] = '\t'.join([spline.__getitem__(elem) for elem in result])

                elif line.startswith('#CHROM'):
                    spline = line.split('\t')
                    result=range(0,len(spline))
                    result.remove(2)
                    result.remove(6)
                    result.remove(7)
                    vcf_head = [spline.__getitem__(elem) for elem in result]

        return [mydict,key_list,vcf_head]








##########test
#/gpfs2/home/wanguan2000/result2_NGS/xh/result_D28/D28_R1_D28_R2_sort_realign_dedup_mate_recal_raw_snp_filtered.vcf
#/gpfs2/home/wanguan2000/result2_NGS/xh/result_D28/D28_R1_D28_R2_sort_realign_dedup_mate_recal_raw_indel_filtered.vcf
'''
snp_vcf= '/gpfs2/home/wanguan2000/result2_NGS/xh/result_D28/D28_R1_D28_R2_sort_realign_dedup_mate_recal_raw_snp_filtered.vcf'
indel_vcf= '/gpfs2/home/wanguan2000/result2_NGS/xh/result_D28/D28_R1_D28_R2_sort_realign_dedup_mate_recal_raw_indel_filtered.vcf'

Annovar('a').vcf_anotation(snp_vcf,'snp')
Annovar('a').vcf_anotation(indel_vcf,'indel')
'''
