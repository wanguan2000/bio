__author__ = 'wanguan2000'
#coding=utf-8
import sys
import re
import os.path
import os
'''
do DynamicTrim for pair-end list and single-end list
####input####
input list fastq files
#######
perl DynamicTrim.pl test1-6_1.fq -p 0.05
##run###
a = Trim('config')
a.DynamicTrim(Sin_Files)
a.DynamicTrim(mPair_File)
####return###
return list (.trimed)

'''
class Trim:
    def __init__(self, config):
        self.const=config
    def DynamicTrim(self, Input_Files):
        const = self.const

        DyTrim = const.dynamictrim
        Output_Folder = const.Output_Folder

        filename = []
        for a in Input_Files:
            if isinstance(a, list):
                filename.append([os.path.join(Output_Folder, re.compile(r'.*/').sub('', a[0])+'.trimmed'),os.path.join(Output_Folder, re.compile(r'.*/').sub('', a[1])+'.trimmed')])
                runDyTrim = ' '.join(['cd',Output_Folder+';','perl',DyTrim,a[0],'-p 0.001'])
                print runDyTrim
                os.system(runDyTrim)
                runDyTrim = ' '.join(['cd',Output_Folder+';','perl',DyTrim,a[1],'-p 0.001'])
                print runDyTrim
                os.system(runDyTrim)
            else:
                filename.append(os.path.join(Output_Folder, re.compile(r'.*/').sub('', a)+'.trimmed'))
                runDyTrim = ' '.join(['cd',Output_Folder+';','perl', a,'-p 0.05'])
                print runDyTrim
                os.system(runDyTrim)
        return filename




   
'''

mPair_File = [
    ['inputfile_NGS/s1/s1_1m.fq', 'inputfile_NGS/s1/s1_2m.fq'],
    ['inputfile_NGS/s2/cm.fastq', 'inputfile_NGS/s2/dm.fastq']
]
Sin_Files = ['inputfile_NGS/s1/s1_1.fq', 'inputfile_NGS/s1/s1_2.fq']
a = Trim('config')
print a.DynamicTrim(mPair_File)
print re.compile(r'.*/').sub('', Sin_Files[0])
'''
