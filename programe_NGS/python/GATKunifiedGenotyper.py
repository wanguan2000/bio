
__author__ = 'wanguan2000'
#coding=utf-8
import sys
import re
import os.path
import os
from myscript import *

'''
do bam to raw snp and indel 
####input####
input list bam files
#######
#################discovery raw snp and indel######
java -Xmx4g -jar ./GenomeAnalysisTK-1.0.5777/GenomeAnalysisTK.jar \
  -l INFO \
  -T UnifiedGenotyper \
  -nt 2 \
  -glm BOTH \
  -A DepthOfCoverage \
  -R ucsc.hg19.fasta \
  -I ./testdata/31bwa_RG_realign_dedup_mate_recal.bam \
  -B:dbsnp,vcf /share/user_data/wfz1/database/hg19database/dbsnp_132.hg19.vcf \
  -o ./testdata/snps.raw31.vcf \
  -stand_call_conf 50.0 \
  -stand_emit_conf 10.0 \
  -dcov 500

##stand_call_conf
Generic command for calling single or multiple samples, whole genome or whole exome

java -jar GenomeAnalysisTK.jar \
 -R resources/Homo_sapiens_assembly18.fasta \
 -T UnifiedGenotyper \
 -I sample1.bam [-I sample2.bam ...] \
 -B:dbsnp,VCF dbSNP.vcf \
 -o snps.raw.vcf \
 -stand_call_conf [50.0] \
 -stand_emit_conf 10.0 \
 -dcov [50] \
 [-L targets.interval_list]

-A FisherStrand -A MappingQualityRankSumTest -A ReadPosRankSumTest -A RMSMappingQuality -A MappingQualityZero -A QualByDepth -A HaplotypeScore -A DepthOfCoverage -A BaseQualityRankSumTest

The above command will call all of the samples in your provided BAM files [-I arguments] together and produce a VCF file with sites and genotypes for all samples. The easiest way to get the dbSNP file is from the GATK resource bundle. Several arguments have parameters that should be chosen based on the average coverage per sample in your data:

-dcov
    downsample term per sample. The UG sees only this amount of coverage per sample. It's used to avoid overwhelming the engine at sites where misalignments lead to 10-10,000,000 fold increases in coverage per sample. A safe value here is 10x the average coverage, so for a 100x data set, use 1000x, but for a 4x data set 50x is fine. The Unified Genotyper engine defaults to 250x.

-stand_call_conf and -stand_emit_conf
    we recommend keeping stand_emit_conf at 10, so that you will always see variant sites with at least Q10 confidence that they are non-reference, but they will be filter out as LowQual unless they exceed the stand_call_conf. The stand_call_conf term needs to be chosen based again on the expected coverage per sample. If you have deep data (10x or better) a stand_call_conf threshold of 50 is fine. If you have very low-pass data, such as the 1000 Genomes low-coverage wing with 4x average and you want to call everything possibly variant, resulting in lots of FPs to be sorted out later, you can set this to a lower value of Q30 or even Q10.

-L targets.interval_list
    if you have an target capture data set, it's best to call only the targeted intervals (for a variety of reasons, beyond the scope of this document). You should provide the target list in one of the interval file formats. 
######################ok################

####return####
return raw.vcf

'-nt', const.cpu,' 
'''
class GATKUnifiedGenotyper:
    def __init__(self,config):
        self.const=config
    def GATKHighcoverage(self,Input_Bam):
         ######data, software ,path  initialization#########
        const = self.const

        GATK =  const.GATK_last
        Output_Folder = const.Output_Folder
        dbsnp = const.dbsnp132
        FastaDatabase = const.FastaDatabase

        ######!data, software ,path  initialization#########
        Output_List=[]
        for bam in Input_Bam:
            #RealignerTargetCreator
            bam_vcf = StringMeth().changeExtension(bam,'_raw.vcf')
            cmd_UnifiedGenotyper = ' '.join(['java','-Djava.io.tmpdir='+const.Temp_Folder,const.memory,'-jar',GATK,'-l INFO -T UnifiedGenotyper','-nt','1','-glm BOTH','-A FisherStrand -A MappingQualityRankSumTest -A ReadPosRankSumTest -A RMSMappingQuality -A MappingQualityZero -A QualByDepth -A HaplotypeScore -A DepthOfCoverage -A BaseQualityRankSumTest','','-I',bam,'-R',FastaDatabase,'-o',bam_vcf,'--dbsnp',dbsnp,'-stand_call_conf 20.0 -stand_emit_conf 10.0 -dcov',str(int(const.Seq_Depth)*10)])
            print cmd_UnifiedGenotyper
            os.system(cmd_UnifiedGenotyper)
            Output_List.append(bam_vcf)
        return Output_List
        
    def GATKHighcoverage_sp(self,Input_Bam,FastaDatabase,dbsnp):
         ######data, software ,path  initialization#########
        const = self.const

        GATK =  const.GATK_last
        Output_Folder = const.Output_Folder

        ######!data, software ,path  initialization#########
        Output_List=[]
        for bam in Input_Bam:
            #RealignerTargetCreator
            bam_vcf = StringMeth().changeExtension(bam,'_raw.vcf')
            cmd_UnifiedGenotyper = ' '.join(['java','-Djava.io.tmpdir='+const.Temp_Folder,const.memory,'-jar',GATK,'-l INFO -T UnifiedGenotyper','-nt','1','-glm BOTH','-A FisherStrand -A MappingQualityRankSumTest -A ReadPosRankSumTest -A RMSMappingQuality -A MappingQualityZero -A QualByDepth -A HaplotypeScore -A DepthOfCoverage -A BaseQualityRankSumTest','','-I',bam,'-R',FastaDatabase,'-o',bam_vcf,'--dbsnp',dbsnp,'-stand_call_conf 20.0 -stand_emit_conf 10.0 -dcov',str(int(const.Seq_Depth)*10)])
            print cmd_UnifiedGenotyper
            os.system(cmd_UnifiedGenotyper)
            Output_List.append(bam_vcf)
        return Output_List


'''test
bamfile = ['/home/wanguan2000/pg/myNGS/result_NGS/test1/s1_1_s1_2_sort_realign_dedup_mate_recal.bam']
a = GATKUnifiedGenotyper('config').GATKHighcoverage(bamfile)
print a
'''
