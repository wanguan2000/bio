__author__ = 'wanguan2000'
#coding=utf-8
import sys
import re
import os.path
import os
from myscript import *

'''
do bam to recalibrate
####input####
input list bam files
#######
#################covariates slowly 4h######
java -Xmx4g -jar ./GenomeAnalysisTK-1.1-12-g2d94037/GenomeAnalysisTK.jar \
  -l INFO \
  -nt 8 \
  -R ucsc.hg19.fasta \
  -B:dbsnp,vcf /share/user_data/wfz1/database/hg19database/dbsnp_132.hg19.vcf \
  -I ./testdata/31bwa_RG_realign_dedup_mate.bam \
  -T CountCovariates \
  -cov ReadGroupCovariate \
  -cov QualityScoreCovariate \
  -cov CycleCovariate \
  -cov DinucCovariate \
  -recalFile ./testdata/31bwa_RG_realign_dedup_mate.csv

 java -Xmx4g -jar GenomeAnalysisTK.jar \
   -R resources/Homo_sapiens_assembly18.fasta \
   -knownSites bundle/hg18/dbsnp_132.hg18.vcf \
   -knownSites another/optional/setOfSitesToMask.vcf \
   -I my_reads.bam \
   -T CountCovariates \
   -cov ReadGroupCovariate \
   -cov QualityScoreCovariate \
   -cov CycleCovariate \
   -cov DinucCovariate \
   -recalFile my_reads.recal_data.csv

###############################recalibrated slowly 4h #####################

java -Xmx4g -jar ./GenomeAnalysisTK-1.1-12-g2d94037/GenomeAnalysisTK.jar \
  -R ucsc.hg19.fasta \
  -I ./testdata/31bwa_RG_realign_dedup_mate.bam \
  -T TableRecalibration \
  -o ./testdata/31bwa_RG_realign_dedup_mate_recal.bam \
  -recalFile ./testdata/31bwa_RG_realign_dedup_mate.csv

 java -Xmx4g -jar GenomeAnalysisTK.jar \
   -R resources/Homo_sapiens_assembly18.fasta \
   -I my_reads.bam \
   -T TableRecalibration \
   -o my_reads.recal.bam \
   -recalFile my_reads.recal_data.csv

######################ok################

####return####
return list _recal.bam

'''
class GATKRecalibrate:
    def __init__(self,config):
        self.const=config
    def GATKCovariateRecalibrate(self,Input_Bam):
         ######data, software ,path  initialization#########
        const = self.const


        GATK = const.GATK_last
        Output_Folder = const.Output_Folder
        dbsnp = const.dbsnp132
        FastaDatabase = const.FastaDatabase

        ######!data, software ,path  initialization#########
        Output_List=[]
        for bam in Input_Bam:
            #RealignerTargetCreator
            bam_csv = StringMeth().changeExtension(bam,'.csv')
            cmd_CountCovariate = ' '.join(['java',const.memory,'-jar',GATK,'-l INFO -nt',const.cpu,'-T CountCovariates','-I',bam,'-R',FastaDatabase,'-knownSites',dbsnp,'-cov ReadGroupCovariate -cov QualityScoreCovariate -cov CycleCovariate -cov DinucCovariate','-recalFile',bam_csv])
            print cmd_CountCovariate
            os.system(cmd_CountCovariate)

            #TableRecalibration
            bam_Recalibration = StringMeth().changeExtension(bam,'_recal.bam')
            cmd_Recalibration = ' '.join(['java','-Djava.io.tmpdir='+const.Temp_Folder,const.memory,'-jar',GATK,'-T TableRecalibration','-I',bam,'-R',FastaDatabase,'-recalFile',bam_csv,'-o',bam_Recalibration])
            print cmd_Recalibration
            os.system(cmd_Recalibration)
            Output_List.append(bam_Recalibration)
        return Output_List

    def GATKCountCovariates(self,Input_Bam):
         ######data, software ,path  initialization#########
        const = self.const


        GATK = const.GATK_last
        Output_Folder = const.Output_Folder
        dbsnp = const.dbsnp132
        FastaDatabase = const.FastaDatabase

        ######!data, software ,path  initialization#########
        for bam in Input_Bam:
            #RealignerTargetCreator
            bam_csv = StringMeth().changeExtension(bam,'.csv')
            cmd_CountCovariate = ' '.join(['java',const.memory,'-jar',GATK,'-l INFO -nt',const.cpu,'-T CountCovariates','-I',bam,'-R',FastaDatabase,'-knownSites',dbsnp,'-cov ReadGroupCovariate -cov QualityScoreCovariate -cov CycleCovariate -cov DinucCovariate','-recalFile',bam_csv])
            print cmd_CountCovariate
            os.system(cmd_CountCovariate)
        return bam_csv





'''test
bamfile = ['/home/wanguan2000/pg/myNGS/result_NGS/test1/s1_1_s1_2_sort.bam']
a = GATKRecalibrate('config').GATKCovariateRecalibrate(bamfile)
print a
'''

