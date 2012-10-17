__author__ = 'wanguan2000'
#coding=utf-8
import sys
import re
import os.path
import os
from myscript import *
from sambamstats import *
from bamindex import *

'''
do sam2bam SORT_ORDER and AddOrReplaceReadGroups and lane information
####input####
input list sam files and const.Sin_Info or const.Pair_Info
#######
java -Xmx4g -jar ./picard-tools-1.48/AddOrReplaceReadGroups.jar \
   INPUT= ./testdata/pair-end31.sam \
   OUTPUT= ./testdata/31bwa_RG.bam \
   SORT_ORDER=coordinate \
   RGID= HGExon31 \
   RGLB=HGExon31 \
   RGPL=illumina \
   RGPU= HWI-ST499-5-GCCAAT \
   RGSM=HGExon31 \
   RGCN=JingNeng \
   RGDS=HumanExon \
   VALIDATION_STRINGENCY=LENIENT


RGID=String    Read Group ID Default value: 1. This option can be set to 'null' to clear the default value.
RGLB=String    Read Group Library Required.
RGPL=String    Read Group platform (e.g. illumina, solid) Required.
RGPU=String    Read Group platform unit (eg. run barcode) Required.
RGSM=String    Read Group sample name Required.
RGCN=String    Read Group sequencing center name Default value: null.
RGDS=String    Read Group description Default value: null.

####return####
return list _sort.bam



QC Statistics Items	WGC000184
Total effective data yield(Mb):	7210.66
Total effective reads:	72106620
Uniquely mapping reads rate:	83.87%
No-mismatch mapping reads rate:	82.33%
Mismatch alignment bases rate:	0.32%
The ratio of reads alignment to reference genome:	99.27%
Mean coverage sequencing depth on official target:	52
Fraction of reference genome covered:	96.02%
Fraction of reference genome covered with at least 4X:	93.46%
Fraction of reference genome covered with at least 10X:	88.91%
Fraction of reference genome covered with at least 20X:	79.15%

hg19_genome.bed

'''

class Sam2BamSortGroup_whole:
    def __init__(self,config):
        self.const=config
    def picardAddOrReplaceReadGroups(self,Input_Sam,Pair_Info,ref_genome):
        ######data, software ,path  initialization#########
        const = self.const

        picard = const.picard_AddOrReplaceReadGroups
        picard_BamIndexStats = const.picard_BamIndexStats
        BEDTools = const.BEDTools

        #ref_genome =  const.Refer_GenomeBed

        Output_Folder =  const.Output_Folder
        AlignDatabase = const.AlignDatabase
        FastaDatabase =  const.FastaDatabase
        
        ######!data, software ,path  initialization#########

        Output_List=[]
        myIndex = 0
        for sam in Input_Sam:

            ##sam to bam####
            outbam = StringMeth().changeExtension(sam,'_sort.bam')
            cmd = ' '.join(['java',const.memory,'-jar',picard,'INPUT=',sam,'OUTPUT=',outbam,'TMP_DIR=',const.Temp_Folder,'SORT_ORDER=coordinate'])+' '+' '.join(Pair_Info[myIndex])+' MAX_RECORDS_IN_RAM=5000000 VALIDATION_STRINGENCY=SILENT'
            print cmd
            os.system(cmd)
            Output_List.append(outbam)
            myIndex+=1

            ###input list bam files bamindex return none ################
            BamIndex(const).picardBuildBamIndex([outbam])

            ##sam stats####
            samstats = StringMeth().changeExtension(sam,'_QCtbale.txt')

            ##bam stats###
            Align_PF = StringMeth().changeExtension(sam,'_AlignPF.txt')
            cmd1 = ' '.join(['java',const.memory,'-jar',picard_BamIndexStats,'TMP_DIR=',const.Temp_Folder,'INPUT=',outbam,'>'+Align_PF])
            os.system(cmd1)
            print cmd1

            #all_read aligned_read aligned_ratio
            result_Align_PF = SamBamStats().Align_PF(Align_PF)
            print result_Align_PF
            total_reads = int(float(result_Align_PF[0]))

            ###ref_genome BaseCover##########
            ref_genome_BaseCover = StringMeth().changeExtension(sam,'_GenomeCover.txt')
            #genomeCoverageBed -i A.bed -g /gpfs2/home/wanguan2000/NGSToolkit/database_NGS/hg19_bed/hg19.genome
            cmd4 = ' '.join([BEDTools+'genomeCoverageBed','-ibam',outbam,'-g',ref_genome,'>',ref_genome_BaseCover])
            print cmd4
            os.system(cmd4)

            with open(samstats,'w') as f:
                f.write('QC Statistics Items\t'+re.sub('_R1.*', '', StringMeth().getPathName(sam))+'\n')
                f.write('\n'.join(SamBamStats().SamStats(sam))+'\n')
                f.write(result_Align_PF[2]+'\n')

                base_covered = SamBamStats().Whole_BaseCover(ref_genome_BaseCover)
                f.write('Mean coverage sequencing depth on genome:\t'+base_covered[0]+'\n')
                f.write('Fraction of genome covered:\t'+base_covered[1]+'\n')
                f.write('Fraction of genome covered with at least 4X:\t'+base_covered[2]+'\n')
                f.write('Fraction of genome covered with at least 10X:\t'+base_covered[3]+'\n')
                f.write('Fraction of genome covered with at least 20X:\t'+base_covered[4]+'\n')
                


        return Output_List


'''test
samfile = ['inputfile_NGS/s1/s1_1.sam', 'inputfile_NGS/s1/s1_2.sam']
Pair_Info = [
    ['RGID = HGExons1', 'RGLB = HGExons1', 'RGPL = illumina', 'RGPU = A8092JABXX-8-GCCAATAT', 'RGSM = HGExons1', 'RGCN = Huada', 'RGDS = HumanExon'],
    ['RGID = HGExons1', 'RGLB = HGExons1', 'RGPL = illumina', 'RGPU = A8092JABXX-8-GCCAATAT', 'RGSM = HGExons1', 'RGCN = Huada', 'RGDS = HumanExon'],
                 ]
a = Sam2BamSortGroup('config').picardAddOrReplaceReadGroups(samfile,Pair_Info)
print(a)


samfile = ['/home/wanguan2000/myNGS/result_NGS/result_A549_T/A549_R1_A549_R2.sam']
Pair_Info = [
    ['RGID=HGExons1', 'RGLB=HGExons1', 'RGPL=illumina', 'RGPU=A8092JABXX-8-GCCAATAT', 'RGSM=HGExons1', 'RGCN=Huada', 'RGDS=HumanExon'],
                 ]
a = Sam2BamSortGroup('config_human20111101').picardAddOrReplaceReadGroups(samfile,Pair_Info)
print a
'''



a = Sam2BamSortGroup_whole('/gpfs3/home/wanguan2000/config3_NGS/whole_4/config_183148L.py').picardAddOrReplaceReadGroups(['/gpfs3/home/wanguan2000/result3_NGS/whole/result_mouse/mouse_R1_mouse_R24960175_sort_realign_dedup_mate_recal.bam'],const.mm9_Fasta,const.mm9_dbsnp)

GATKHighcoverage(bam_recal,'/gpfs/home/wanguan2000/NGSToolkit/database_NGS/UCSCmm9/mm9.fasta','/gpfs/home/wanguan2000/NGSToolkit/database_NGS/GATK_mm9/mm9_dbSNP132.vcf')
print a

















