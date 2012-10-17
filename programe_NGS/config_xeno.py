import python.const as const
#const. It's means  a constant
# NGS settings for bioinfor project.
#data information
##single end the fastq files in inputfile_NGS folder ############
const.Sin_Files = ['inputfile_NGS/s1/s1_1.fq', 'inputfile_NGS/s1/s1_2.fq']

const.Sin_Info = [
    ['RGID=HGExons1', 'RGLB=HGExons1', 'RGPL=illumina', 'RGPU=A8092JABXX-8-GCCAATAT', 'RGSM=HGExons1', 'RGCN=Huada', 'RGDS=HumanExon'],
    ['RGID=HGExons1', 'RGLB=HGExons1', 'RGPL=illumina', 'RGPU=A8092JABXX-8-GCCAATAT', 'RGSM=HGExons1', 'RGCN=Huada', 'RGDS=HumanExon'],
                      ]
###pair end file list#########

const.Pair_File = [['/home/wanguan2000/Project_fastq/backup/20111108/i951681P3/i951681P3_R1_human.fastq','/home/wanguan2000/Project_fastq/backup/20111108/i951681P3/i951681P3_R2_human.fastq'],]

###Pair Info list#########

const.Pair_Info = [['RGID=xeno', 'RGLB=xeno', 'RGPL=illumina', 'RGPU=HWI-ST966', 'RGSM=xeno', 'RGCN=wuxiapp', 'RGDS=xenograft'],]



#[output_folder]
const.Output_Folder = 'result_xeno2'
#[cpu_no]
const.cpu = '20'
#[memory]
const.memory = '-Xmx30g'

####item info for const.Pair_Info#########
#RGID=String    Read Group ID Default value: 1. This option can be set to 'null' to clear the default value.
#RGLB=String    Read Group Library Required.
#RGPL=String    Read Group platform (e.g. illumina, solid) Required.
#RGPU=String    Read Group platform unit (eg. run barcode) Required.
#RGSM=String    Read Group sample name Required.
#RGCN=String    Read Group sequencing center name Default value: null.
#RGDS=String    Read Group description Default value: null.



#[species_database]
const.AlignDatabase = 'database_NGS/hg19fastadatabase/indexhg19_bwa/hg19_bwa'
const.FastaDatabase = 'database_NGS/hg19fastadatabase/ucsc.hg19.fasta'
const.dbsnp132 = 'database_NGS/hg19_GATK1_1/dbsnp_132.hg19.vcf'
const.omni = 'database_NGS/hg19_GATK1_1/1000G_omni2.5.hg19.sites.vcf'
const.hapmap = 'database_NGS/hg19_GATK1_1/hapmap_3.3.hg19.sites.vcf'
const.indels_mills = 'database_NGS/hg19_GATK1_1/indels_mills_devine.hg19.sites.vcf'

const.TruSeq ='database_NGS/hg19_bed/TruSeq.bed'
const.TruSeq150 ='database_NGS/hg19_bed/TruSeq150.bed'
const.TruSeq500 ='database_NGS/hg19_bed/TruSeq500.bed'
const.TruSeq_RefCoding = 'database_NGS/hg19_bed/TruSeq_RefCoding.bed'

#[platform_info]
const.Seq_Depth = '50'
const.Read_Length = '100'




#[pair_end]
# The minimum insert size for valid paired-end alignments.bowtie -I
const.Mininsert_Size = '20'
#The maximum insert size for valid paired-end alignments.bowtie -X
const.Maxinsert_Size = '100'



#[software]
const.bwa = 'software_NGS/bwa-0.5.9/bwa'
const.botwie = ''
const.fastqc = 'software_NGS/FastQC_v0.9.5/fastqc'
const.dynamictrim = 'software_NGS/DynamicTrim_v.1.10/DynamicTrim.pl'
const.picard_SamFormatConverter = 'software_NGS/picard-tools-1.50/SamFormatConverter.jar'
const.picard_AddOrReplaceReadGroups = 'software_NGS/picard-tools-1.50/AddOrReplaceReadGroups.jar'
const.picard_BuildBamIndex = 'software_NGS/picard-tools-1.50/BuildBamIndex.jar'
const.picard_MarkDuplicates = 'software_NGS/picard-tools-1.50/MarkDuplicates.jar'
const.picard_FixMateInformation = 'software_NGS/picard-tools-1.50/FixMateInformation.jar'
const.picard_BamIndexStats = 'software_NGS/picard-tools-1.50/BamIndexStats.jar'


const.GATK_last = 'software_NGS/GATK/GenomeAnalysisTK-1.1-36-g367bbee/GenomeAnalysisTK.jar'
const.GATK_1_1_36 = 'software_NGS/GATK/GenomeAnalysisTK-1.1-36-g367bbee/GenomeAnalysisTK.jar'
const.GATK_1_1 = 'software_NGS/GATK/GenomeAnalysisTK-1.1/GenomeAnalysisTK.jar'
const.GATK_1_0_5777 = 'software_NGS/GATK/GenomeAnalysisTK-1.0.5777/GenomeAnalysisTK.jar'
const.BEDTools = 'software_NGS/BEDTools-Version-2.13.1/bin/'


