__author__ = 'wanguan2000'
#coding=utf-8
import sys
import re
import os.path
import os
from myscript import *

'''

java -Xmx15g -jar /gpfs/home/wanguan2000/NGSToolkit/software_NGS/GATK/GenomeAnalysisTK-1.3-24-gc8b1c92/GenomeAnalysisTK.jar \
  -R /gpfs/home/wanguan2000/NGSToolkit/database_NGS/hg19fastadatabase/ucsc.hg19.fasta \
  -T PrintReads \
  --sample_name blood19 \
  --sample_name xeno19 \
  -I blood19_ALLmerge_realign_mate_recal.bam \

blood19	tissue19	xeno19


HWI-ST966:76:D0B43ACXX:8:2203:18402:159435	99	chrM	2699	60	100M	=	2838238	GGCGGGCATGACACAGCAAGACGAGAAGACCCTATGGAGCTTTAATTTATTAATGCAAACAGTACCTAACAAACCCACAGGTCCTAAACTACCAAACCTG	BGE?EFFEDHCEEFEIGEEHCF@CHCEICFGGFDDHHCGGFDCDDCCCCCDDECFFEEEEEE@BDGECEEEEEEGFEEEHFCFHEDFEDFDEGEEDDFDE	X0:i:1	X1:i:0	MD:Z:100	RG:Z:tissue19	XG:i:0	AM:i:37	NM:i:0	SM:i:37	XM:i:0	XO:i:0	MQ:i:60	OQ:Z:CCCFFFFFHHHHHIJJJIJJJJIIJJJJJJJJIJJJJIHFHHHHFFFFFFFFEEDEEEEDDC>ACDCDDDDDDDD@BDDDBCDDDDDDCDDDDDDDDDCD	XT:A:U

java -Xmx15g -jar /gpfs/home/wanguan2000/NGSToolkit/software_NGS/GATK/GenomeAnalysisTK-1.3-24-gc8b1c92/GenomeAnalysisTK.jar \
  -R /gpfs/home/wanguan2000/NGSToolkit/database_NGS/hg19fastadatabase/ucsc.hg19.fasta \
  -T PrintReads \
  --sample_name blood19 \
  -I blood19_ALLmerge_realign_mate_recal.bam \
  -L chrX \
  -o output.bam

RGID=String    Read Group ID Default value: 1. This option can be set to 'null' to clear the default value.
RGLB=String    Read Group Library Required.
RGPL=String    Read Group platform (e.g. illumina, solid) Required.
RGPU=String    Read Group platform unit (eg. run barcode) Required.
RGSM=String    Read Group sample name Required.
RGCN=String    Read Group sequencing center name Default value: null.
RGDS=String    Read Group description Default value: null.
'''


class SeparaBam:
    def __init__(self,config):
        self.const=config
    def Separa_Sample(self,Input_Bam,SampleName):
        ######data, software ,path  initialization#########
        const = self.const
        GATK =  const.GATK_last
        Output_Folder = const.Output_Folder
        dbsnp = const.dbsnp132
        FastaDatabase = const.FastaDatabase
        ######!data, software ,path  initialization#########
        for name in SampleName:
            outname = StringMeth().changeExtension(Input_Bam,'_'+name+'.bam')
            cmd = ' '.join(['java','-jar',GATK,'-T PrintReads','--sample_name',name,'-I',Input_Bam,'-o',outname])
            print cmd
            os.system(cmd)
        return None
    def Separa_chr(self,Input_Bam,chrname):
        ######data, software ,path  initialization#########
        if not chrname:
           chrname = ['chrM','chr1','chr2','chr3','chr4','chr5','chr6','chr7','chr8','chr9','chr10','chr11','chr12','chr13','chr14','chr15','chr16','chr17','chr18','chr19','chr20','chr21','chr22','chrX','chrY']

        const = self.const
        GATK =  const.GATK_last
        Output_Folder = const.Output_Folder
        FastaDatabase = const.FastaDatabase

        ######!data, software ,path  initialization#########
        for name in chrname:
            outchr = StringMeth().changeExtension(Input_Bam,'_'+name+'.bam')
            cmd = ' '.join(['java','-jar',GATK,'-T PrintReads','-L',name,'-I',Input_Bam,'-o',outchr])
            print cmd
            os.system(cmd)
        return None

'''
        cmd_UnifiedGenotyper = ' '.join(['java','-Djava.io.tmpdir='+const.Temp_Folder,const.memory,'-jar',GATK,'-l INFO -T UnifiedGenotyper','-nt','1','-glm BOTH','-A FisherStrand -A MappingQualityRankSumTest -A ReadPosRankSumTest -A RMSMappingQuality -A MappingQualityZero -A QualByDepth -A HaplotypeScore -A DepthOfCoverage -A BaseQualityRankSumTest',inputbam,'-R',FastaDatabase,'-o',bam_vcf,'--dbsnp',dbsnp,'-stand_call_conf 20.0 -stand_emit_conf 10.0 -dcov',str(int(const.Seq_Depth)*10)])
        print cmd_UnifiedGenotyper
        os.system(cmd_UnifiedGenotyper)
        return(bam_vcf)
'''







