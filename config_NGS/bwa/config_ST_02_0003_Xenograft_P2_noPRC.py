# NGS settings for bioinfor project.
#data information
##single end the fastq files in inputfile_NGS folder ############
Sin_Files = ['inputfile_NGS/s1/s1_1.fq', 'inputfile_NGS/s1/s1_2.fq']

Sin_Info = [
    ['RGID=HGExons1', 'RGLB=HGExons1', 'RGPL=illumina', 'RGPU=A8092JABXX-8-GCCAATAT', 'RGSM=HGExons1', 'RGCN=Huada', 'RGDS=HumanExon'],
    ['RGID=HGExons1', 'RGLB=HGExons1', 'RGPL=illumina', 'RGPU=A8092JABXX-8-GCCAATAT', 'RGSM=HGExons1', 'RGCN=Huada', 'RGDS=HumanExon'],
                      ]
###pair end file list#########

Pair_File = [['/gpfs/home/wanguan2000/Project_fastq/xenograft/ST_02_0003_Xenograft_P2_noPRC/ST_02_0003_Xenograft_P2_noPRC_R1.fastq','/gpfs/home/wanguan2000/Project_fastq/xenograft/ST_02_0003_Xenograft_P2_noPRC/ST_02_0003_Xenograft_P2_noPRC_R2.fastq'],]

###Pair Info list#########


Pair_Info = [['RGID=ST_02_0003_Xenograft_P2_noPRC', 'RGLB=ST_02_0003_Xenograft_P2_noPRC', 'RGPL=illumina', 'RGPU=HWI-ST966', 'RGSM=ST_02_0003_Xenograft_P2_noPRC', 'RGCN=wuxiapp', 'RGDS=exon-genome'],]


#[output_folder]
Output_Folder = '/tmp/xenograft20111231/result_ST_02_0003_Xenograft_P2_noPRC'
#[cpu_no]
cpu = '6'
#[memory]
memory = '-Xmx15g'

####item info for Pair_Info#########
#RGID=String    Read Group ID Default value: 1. This option can be set to 'null' to clear the default value.
#RGLB=String    Read Group Library Required.
#RGPL=String    Read Group platform (e.g. illumina, solid) Required.
#RGPU=String    Read Group platform unit (eg. run barcode) Required.
#RGSM=String    Read Group sample name Required.
#RGCN=String    Read Group sequencing center name Default value: null.
#RGDS=String    Read Group description Default value: null.

#[platform_info]
Seq_Depth = '50'
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
'''
The current best set of known indels to be used for local realignment (note that we don't use dbSNP for this anymore); use both files:
    1000G_biallelic.indels.b37.vcf (currently from the 1000 Genomes Phase I indel calls)
    Mills_Devine_2hit.indels.b37.vcf


   -resource:hapmap,VCF,known=false,training=true,truth=true,prior=15.0 hapmap_3.3.b37.sites.vcf \
   -resource:omni,VCF,known=false,training=true,truth=false,prior=12.0 1000G_omni2.5.b37.sites.vcf \
   -resource:dbsnp,VCF,known=true,training=false,truth=false,prior=8.0 dbsnp_132.b37.vcf \
   -an QD -an HaplotypeScore -an MQRankSum -an ReadPosRankSum -an FS -an MQ -an InbreedingCoeff -an DP \
   -mode SNP \

   -resource:mills,VCF,known=true,training=true,truth=true,prior=12.0 Mills_Devine_2hit.indels.b37.sites.vcf \
   -an QD -an FS -an HaplotypeScore -an ReadPosRankSum -an InbreedingCoeff \
   -mode INDEL \

'''

AlignDatabase = Root_Database + 'database_NGS/hg19fastadatabase/hg19_bwa/hg19_bwa'
FastaDatabase = Root_Database + 'database_NGS/hg19fastadatabase/ucsc.hg19.fasta'
dbsnp132 = Root_Database + 'database_NGS/GATK_hg19_1.2/dbsnp_132.hg19.vcf'

omni = Root_Database + 'database_NGS/GATK_hg19_1.2/1000G_omni2.5.hg19.sites.vcf'
hapmap = Root_Database + 'database_NGS/GATK_hg19_1.2/hapmap_3.3.hg19.sites.vcf'
indels_mills = Root_Database + 'database_NGS/GATK_hg19_1.2/Mills_Devine_2hit.indels.hg19.sites.vcf'
indels_mills_realignment = Root_Database + 'database_NGS/GATK_hg19_1.2/Mills_Devine_2hit.indels.hg19.vcf'
indels_1000G_realignment = Root_Database + 'database_NGS/GATK_hg19_1.2/1000G_biallelic.indels.hg19.vcf'

TruSeq =Root_Database + 'database_NGS/hg19_bed/TruSeq.bed'
TruSeq150 =Root_Database + 'database_NGS/hg19_bed/TruSeq150.bed'
TruSeq500 =Root_Database + 'database_NGS/hg19_bed/TruSeq500.bed'
TruSeq_RefCoding =Root_Database +  'database_NGS/hg19_bed/TruSeq_RefCoding.bed'

###mouse mm9####
mm9_bwa = Root_Database + 'database_NGS/UCSCmm9/mm9_index/mm9_bwa'
mm9_Fasta = Root_Database + 'database_NGS/UCSCmm9/mm9.fasta'
hg19mm9_fusion1 = Root_Database + 'database_NGS/fusion_hg19mm9/fusion_index/hg19_mm9_1_bwa'
hg19mm9_fusion2 = Root_Database + 'database_NGS/fusion_hg19mm9/fusion_index/hg19_mm9_2_bwa'



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
GATK_last = Root_Software + 'software_NGS/GATK/GenomeAnalysisTK-1.3-24-gc8b1c92/GenomeAnalysisTK.jar'
BEDTools = Root_Software + 'software_NGS/BEDTools-Version-2.13.1/bin/'



