# NGS settings for bioinfor project.
#data information
##single end the fastq files in inputfile_NGS folder ############
Sin_Files = ['inputfile_NGS/s1/s1_1.fq', 'inputfile_NGS/s1/s1_2.fq']

Sin_Info = [
    ['RGID=HGExons1', 'RGLB=HGExons1', 'RGPL=illumina', 'RGPU=A8092JABXX-8-GCCAATAT', 'RGSM=HGExons1', 'RGCN=Huada', 'RGDS=HumanExon'],
    ['RGID=HGExons1', 'RGLB=HGExons1', 'RGPL=illumina', 'RGPU=A8092JABXX-8-GCCAATAT', 'RGSM=HGExons1', 'RGCN=Huada', 'RGDS=HumanExon'],
                      ]
###pair end file list#########

#%%Pair_File  const.Pair_File =[  ['/home/wanguan2000/Project_fastq/763104N/763104N_R1.fastq', '/home/wanguan2000/Project_fastq/763104N/763104N_R2.fastq'],]

###Pair Info list#########


#%%Pair_Info   const.Pair_Info = [ ['RGID=763104N', 'RGLB=763104N', 'RGPL=illumina', 'RGPU=HWI-ST966-76', 'RGSM=N763104N', 'RGCN=wuxiapp', 'RGDS=exon-genome'],]


#[output_folder]
#%%Output_Folder  const.Output_Folder = 'result_763104N'
#[cpu_no]
cpu = '4'
#[memory]
memory = '-Xmx20g'

####item info for Pair_Info#########
#RGID=String    Read Group ID Default value: 1. This option can be set to 'null' to clear the default value.
#RGLB=String    Read Group Library Required.
#RGPL=String    Read Group platform (e.g. illumina, solid) Required.
#RGPU=String    Read Group platform unit (eg. run barcode) Required.
#RGSM=String    Read Group sample name Required.
#RGCN=String    Read Group sequencing center name Default value: null.
#RGDS=String    Read Group description Default value: null.

#[platform_info]
Seq_Depth = '100'
Read_Length = '100'


#[pair_end]
# The minimum insert size for valid paired-end alignments.bowtie -I
Mininsert_Size = '20'
#The maximum insert size for valid paired-end alignments.bowtie -X
Maxinsert_Size = '100'




#[species_database]
#[Root_Server for database]
Root_Database = '/gpfs/home/wanguan2000/NGSToolkit/'
#####
AlignDatabase = Root_Database + 'database_NGS/hg19fastadatabase/hg19_bwa/hg19_bwa'
FastaDatabase = Root_Database + 'database_NGS/hg19fastadatabase/ucsc.hg19.fasta'
#dbsnp132 = Root_Database + 'database_NGS/GATK_hg19_1.2/dbsnp_132.hg19.vcf'
dbsnp132 = Root_Database + 'database_NGS/budle1_5/dbsnp_135.hg19.vcf'


#omni = Root_Database + 'database_NGS/GATK_hg19_1.2/1000G_omni2.5.hg19.sites.vcf'
omni = Root_Database + 'database_NGS/budle1_5/1000G_omni2.5.hg19.sites.vcf'

#hapmap = Root_Database + 'database_NGS/GATK_hg19_1.2/hapmap_3.3.hg19.sites.vcf'
hapmap = Root_Database + 'database_NGS/budle1_5/hapmap_3.3.hg19.sites.vcf'


#indels_mills = Root_Database + 'database_NGS/GATK_hg19_1.2/Mills_Devine_2hit.indels.hg19.sites.vcf'
indels_mills = Root_Database + 'database_NGS/budle1_5/Mills_and_1000G_gold_standard.indels.hg19.sites.vcf'

#indels_mills_realignment = Root_Database + 'database_NGS/GATK_hg19_1.2/Mills_Devine_2hit.indels.hg19.vcf'
indels_mills_realignment = Root_Database + 'database_NGS/budle1_5/Mills_and_1000G_gold_standard.indels.hg19.vcf'

#indels_1000G_realignment = Root_Database + 'database_NGS/GATK_hg19_1.2/1000G_biallelic.indels.hg19.vcf'
indels_1000G_realignment = Root_Database + 'database_NGS/budle1_5/1000G_phase1.indels.hg19.vcf'

'''
###Nimblege
TruSeq =Root_Database + 'database_NGS/hg19_bed/Nimblege/SeqCap_EZ_Exome_v2_merge.bed'
TruSeq150 =Root_Database + 'database_NGS/hg19_bed/Nimblege/SeqCap_EZ_Exome_v2_merge150.bed'
TruSeq500 =Root_Database + 'database_NGS/hg19_bed/Nimblege/SeqCap_EZ_Exome_v2_merge500.bed'
TruSeq_RefCoding =Root_Database +  'database_NGS/hg19_bed/TruSeq_RefCoding.bed'
'''


#SureSelect
TruSeq =Root_Database + 'database_NGS/hg19_bed/Sureselect/SureSelect_merge.bed'
TruSeq150 =Root_Database + 'database_NGS/hg19_bed/Sureselect/SureSelect_merge150.bed'
TruSeq500 =Root_Database + 'database_NGS/hg19_bed/Sureselect/SureSelect_merge500.bed'
TruSeq_RefCoding =Root_Database +  'database_NGS/hg19_bed/TruSeq_RefCoding.bed'

'''
###TruSeq
TruSeq =Root_Database + 'database_NGS/hg19_bed/Turseq/TruSeq_merge.bed'
TruSeq150 =Root_Database + 'database_NGS/hg19_bed/Turseq/TruSeq_merge150.bed'
TruSeq500 =Root_Database + 'database_NGS/hg19_bed/Turseq/TruSeq_merge500.bed'
TruSeq_RefCoding =Root_Database +  'database_NGS/hg19_bed/TruSeq_RefCoding.bed'
'''
hg19_Genome =Root_Database +  'database_NGS/hg19_bed/hg19.genome'

###mouse mm9####
mm9_bwa = Root_Database + 'database_NGS/UCSCmm9/mm9_index/mm9_bwa'
mm9_Fasta = Root_Database + 'database_NGS/UCSCmm9/mm9.fasta'
hg19mm9_fusion1 = Root_Database + 'database_NGS/fusion_hg19mm9/fusion_index/hg19_mm9_1_bwa'
hg19mm9_fusion2 = Root_Database + 'database_NGS/fusion_hg19mm9/fusion_index/hg19_mm9_2_bwa'
mm9_dbsnp=Root_Database + 'database_NGS/GATK_mm9/mm9_dbSNP132.vcf'
mm9_Genome =Root_Database +  'database_NGS/mm9_bed/mm9.genome'

#[software]
#[Root_Server for software]
Root_Software = '/gpfs/home/wanguan2000/NGSToolkit/'
####
bwa = Root_Software + 'software_NGS/bwa-0.6.1/bwa'
botwie = Root_Software + 'software_NGS/bowtie-0.12.7'
fastqc = Root_Software + 'software_NGS/FastQC/fastqc'
dynamictrim = Root_Software + 'software_NGS/DynamicTrim_v.1.10/DynamicTrim.pl'
picard_SamFormatConverter = Root_Software + 'software_NGS/picard-tools-1.55/SamFormatConverter.jar'
picard_AddOrReplaceReadGroups = Root_Software + 'software_NGS/picard-tools-1.55/AddOrReplaceReadGroups.jar'
picard_BuildBamIndex = Root_Software + 'software_NGS/picard-tools-1.55/BuildBamIndex.jar'
picard_MarkDuplicates = Root_Software + 'software_NGS/picard-tools-1.55/MarkDuplicates.jar'
picard_FixMateInformation = Root_Software + 'software_NGS/picard-tools-1.55/FixMateInformation.jar'
picard_BamIndexStats = Root_Software + 'software_NGS/picard-tools-1.55/BamIndexStats.jar'
GATK_last = Root_Software + 'software_NGS/GATK/GenomeAnalysisTK-1.6-11-g3b2fab9/GenomeAnalysisTK.jar'
BEDTools = Root_Software + 'software_NGS/BEDTools-Version-2.13.1/bin/'
annovar = Root_Software + 'software_NGS/annovar20120401/'

