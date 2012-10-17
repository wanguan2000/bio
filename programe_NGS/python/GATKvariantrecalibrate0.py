__author__ = 'wanguan2000'
#coding=utf-8
import sys
import re
import os.path
import os
from myscript import *

'''
Note that, for the above to work, the input vcf needs to be annotated with the corresponding values (QD, FS, MQ, etc.). If any of these values are somehow missing, then VariantAnnotator needs to be run first so that VariantRecalibration can run properly. 

 java -Xmx2g -jar GenomeAnalysisTK.jar \
   -R ref.fasta \
   -T VariantAnnotator \
   -I input.bam \
   -o output.vcf \
   -A DepthOfCoverage
   --variant input.vcf \
   --dbsnp dbsnp.vcf


Variant quality score recalibration
####input####
input list vcf files like:[['recal_raw_snp.vcf', 'recal_raw_indel.vcf']]

#######
The variant recalibrator contrastively evaluates variants in a two step process:
    VariantRecalibration - Create a Gaussian mixture model by looking at the annotations values over a high quality subset of the input call set and then evaluate all input variants.
    ApplyRecalibration - Apply the model parameters to each variant in input VCF files producing a recalibrated VCF file in which each variant is annotated with its VQSLOD value.
    In addition, this step will filter the calls based on this new lod score by adding lines to the FILTER column for variants that don't meet the lod threshold as provided by the user (with the ts_filter_level parameter).
#################BuildErrorModelWithVQSR######
#################SNP######

java -Xmx4g -jar GenomeAnalysisTK.jar \
   -T VariantRecalibrator \
   -R path/to/reference/human_g1k_v37.fasta \
   -B:input,VCF NA12878.HiSeq.WGS.bwa.cleaned.raw.hg19.subset.vcf \
   -B:hapmap,VCF,known=false,training=true,truth=true,prior=15.0 hapmap_3.3.b37.sites.vcf \
   -B:omni,VCF,known=false,training=true,truth=false,prior=12.0 1000G_omni2.5.b37.sites.vcf \
   -B:dbsnp,VCF,known=true,training=false,truth=false,prior=8.0 dbsnp_132.b37.vcf \
   -an QD -an HaplotypeScore -an MQRankSum -an ReadPosRankSum -an FS -an MQ \
   -mode SNP \
   -recalFile path/to/output.recal \
   -tranchesFile path/to/output.tranches \
   -rscriptFile path/to/output.plots.R

java -Xmx3g -jar GenomeAnalysisTK.jar \
   -T ApplyRecalibration \
   -R path/to/reference/human_g1k_v37.fasta \
   -B:input,VCF NA12878.HiSeq.WGS.bwa.cleaned.raw.hg19.subset.vcf \
   --ts_filter_level 99.0 \
   -tranchesFile path/to/output.tranches \
   recalFile path/to/output.recal
   -o path/to/output.recalibrated.filtered.vcf

#################indel######

Additionally, notice that DP was removed when working with hybrid capture datasets since there is extreme variation in the depth to which targets are captured.
In whole genome experiments this variation is indicative of error but that is not the case in capture experiments.

######################ok################

   -B:hapmap,VCF,known=false,training=true,truth=true,prior=15.0 hapmap_3.3.b37.sites.vcf \
   -B:omni,VCF,known=false,training=true,truth=false,prior=12.0 1000G_omni2.5.b37.sites.vcf \
   -B:dbsnp,VCF,known=true,training=false,truth=false,prior=8.0 dbsnp_132.b37.vcf \
   -an QD -an HaplotypeScore -an MQRankSum -an ReadPosRankSum -an FS -an MQ -an InbreedingCoeff -an DP \
   -mode SNP \

####return####
return ([snp_filtered,indel_filtered])

'''
class GATKVariantRecalibrate:
    def __init__(self,config):
        self.const=config
    def GATKRecalibrate(self,Input_vcf):
        ######data, software ,path  initialization#########
        const = self.const


        GATK = const.GATK_last
        Output_Folder = const.Output_Folder
        dbsnp = const.dbsnp132
        omni =  const.omni
        hapmap = const.hapmap
        indels_mills = const.indels_mills
        FastaDatabase = const.FastaDatabase

        ######!data, software ,path  initialization#########
        Output_List=[]
        for bigvcf in Input_vcf:
            #RealignerTargetCreator
            vcf_snp = bigvcf[0]
            vcf_indel = bigvcf[1]
            #do snp#########################
            snp_recal = StringMeth().changeExtension(vcf_snp,'.recal')
            snp_tranches = StringMeth().changeExtension(vcf_snp,'.tranches')
            snp_rscript = StringMeth().changeExtension(vcf_snp,'_plots.R')
            snp_filtered = StringMeth().changeExtension(vcf_snp,'_filtered.vcf')

            cmd_VariantRecalibrator = ' '.join(['java','-Djava.io.tmpdir='+const.Temp_Folder,const.memory,'-jar',GATK,'-T VariantRecalibrator','-R',FastaDatabase,'-input',vcf_snp,'-resource:hapmap,known=false,training=true,truth=true,prior=15.0',hapmap,'-resource:omni,known=false,training=true,truth=false,prior=12.0',omni,'-resource:dbsnp,known=true,training=false,truth=false,prior=8.0',dbsnp,'-an QD -an HaplotypeScore -an MQRankSum -an ReadPosRankSum -an FS -an MQ','--maxGaussians 6','-mode SNP','-recalFile',snp_recal,'-tranchesFile',snp_tranches,'-rscriptFile',snp_rscript])
            print cmd_VariantRecalibrator
            os.system(cmd_VariantRecalibrator)
            cmd_ApplyRecalibration = ' '.join(['java','-Djava.io.tmpdir='+const.Temp_Folder,const.memory,'-jar',GATK,'-T ApplyRecalibration','-R',FastaDatabase,'-input',vcf_snp,'--ts_filter_level 99.0','-tranchesFile',snp_tranches,'-recalFile',snp_recal,'-o', snp_filtered,'-mode SNP'])
            print cmd_ApplyRecalibration
            os.system(cmd_ApplyRecalibration)

            #do indel#########################
            indel_recal = StringMeth().changeExtension(vcf_indel,'.recal')
            indel_tranches = StringMeth().changeExtension(vcf_indel,'.tranches')
            indel_rscript = StringMeth().changeExtension(vcf_indel,'_plots.R')
            indel_filtered  = StringMeth().changeExtension(vcf_indel,'_filtered.vcf')

            cmd_VariantRecalibrator = ' '.join(['java','-Djava.io.tmpdir='+const.Temp_Folder,const.memory,'-jar',GATK,'-T VariantRecalibrator','-R',FastaDatabase,'-input',vcf_indel,'-resource:mills,known=true,training=true,truth=true,prior=12.0',const.indels_mills,'-an QD -an FS -an HaplotypeScore -an ReadPosRankSum ','--maxGaussians 6','-mode INDEL','-recalFile',indel_recal,'-tranchesFile',indel_tranches,'-rscriptFile',indel_rscript])
            print cmd_VariantRecalibrator
            os.system(cmd_VariantRecalibrator)
            cmd_ApplyRecalibration = ' '.join(['java','-Djava.io.tmpdir='+const.Temp_Folder,const.memory,'-jar',GATK,'-T ApplyRecalibration','-R',FastaDatabase,'-input',vcf_indel,'--ts_filter_level 99.0','-tranchesFile',indel_tranches,'-recalFile',indel_recal,'-o', indel_filtered,'-mode INDEL'])
            print cmd_ApplyRecalibration
            os.system(cmd_ApplyRecalibration)


            
            Output_List.append([snp_filtered,indel_filtered])
        return Output_List





'''test
vcfile=[['/home/wanguan2000/pg/myNGS/result_NGS/test1/s1_1_s1_2_sort_realign_dedup_mate_recal_raw_snp.vcf', '/home/wanguan2000/pg/myNGS/result_NGS/test1/s1_1_s1_2_sort_realign_dedup_mate_recal_raw_indel.vcf']]
a = GATKVariantRecalibrate('config').GATKRecalibrate(vcfile)
print a
'''


