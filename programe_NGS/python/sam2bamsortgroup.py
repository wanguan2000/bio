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

'''

class Sam2BamSortGroup:
    def __init__(self,config):
        self.const=config
    def picardAddOrReplaceReadGroups(self,Input_Sam,Pair_Info):
        ######data, software ,path  initialization#########
        const = self.const


        picard = const.picard_AddOrReplaceReadGroups
        picard_BamIndexStats = const.picard_BamIndexStats
        BEDTools = const.BEDTools

        TruSeq =  const.TruSeq
        TruSeq150 = const.TruSeq150
        TruSeq500 = const.TruSeq500
        TruSeq_RefCoding = const.TruSeq_RefCoding

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

            result_Align_PF = SamBamStats().Align_PF(Align_PF)
            print result_Align_PF
            total_reads = int(float(result_Align_PF[0]))

            ##TruSeq ReadsCover###
            TruSeq_cover = StringMeth().changeExtension(sam,'_TruSeqcover.txt')
            cmd2 = ' '.join([BEDTools+'coverageBed','-abam',outbam,'-b',TruSeq,'>',TruSeq_cover])
            os.system(cmd2)
            ###TruSeq150 ReadsCover##########
            TruSeq150_cover = StringMeth().changeExtension(sam,'_TruSeq150cover.txt')
            cmd3 = ' '.join([BEDTools+'coverageBed','-abam',outbam,'-b',TruSeq150,'>',TruSeq150_cover])
            os.system(cmd3)
            ###TruSeq500 ReadsCover##########
            TruSeq500_cover = StringMeth().changeExtension(sam,'_TruSeq500cover.txt')
            cmd3 = ' '.join([BEDTools+'coverageBed','-abam',outbam,'-b',TruSeq500,'>',TruSeq500_cover])
            os.system(cmd3)

            ###TruSeq BaseCover##########
            TruSeq_BaseCover = StringMeth().changeExtension(sam,'_TruSeqBaseCover.txt')
            cmd4 = ' '.join([BEDTools+'coverageBed','-abam',outbam,'-b',TruSeq,'-hist','>',TruSeq_BaseCover])
            os.system(cmd4)
            ###CodingExons BaseCover##########
            CodingExons_BaseCover = StringMeth().changeExtension(sam,'_CodingExonsBaseCover.txt')
            cmd5 = ' '.join([BEDTools+'coverageBed','-abam',outbam,'-b',TruSeq_RefCoding,'-hist','>',CodingExons_BaseCover])
            os.system(cmd5)

            with open(samstats,'w') as f:
                f.write('QC Statistics Items\t'+re.sub('_R1.*', '', StringMeth().getPathName(sam))+'\n')
                f.write('\n'.join(SamBamStats().SamStats(sam))+'\n')
                f.write(result_Align_PF[2]+'\n')

                capture_effiency = SamBamStats().ReadsCover(TruSeq_cover, total_reads)
                capture_effiency150 = SamBamStats().ReadsCover(TruSeq150_cover, total_reads)
                capture_effiency500 = SamBamStats().ReadsCover(TruSeq500_cover, total_reads)
                f.write('Capture efficiency rate on target regions:\t'+capture_effiency[0]+'\n')
                f.write('Capture efficiency rate on or near +-150 target regions:\t'+capture_effiency150[0]+'\n')
                f.write('Capture efficiency rate on or near +-500 target regions:\t'+capture_effiency500[0]+'\n')

                base_covered = SamBamStats().BaseCover(TruSeq_BaseCover)
                coding_covered = SamBamStats().BaseCover(CodingExons_BaseCover)
                f.write('Mean coverage sequencing depth on official target:\t'+base_covered[0]+'\n')
                f.write('Fraction of official target covered:\t'+base_covered[1]+'\n')
                f.write('Fraction of official target covered with at least 4X:\t'+base_covered[2]+'\n')
                f.write('Fraction of official target covered with at least 10X:\t'+base_covered[3]+'\n')
                f.write('Fraction of official target covered with at least 20X:\t'+base_covered[4]+'\n')
                


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




















