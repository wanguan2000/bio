__author__ = 'wanguan2000'
# -*- coding: utf-8 -*-
import sys
import os
import locale
import codecs
import re

'''
const.Pair_File = [
#%%Pair_File    ['/home/wanguan2000/Project_fastq/763104N/763104N_R1.fastq', '/home/wanguan2000/Project_fastq/763104N/763104N_R2.fastq'],
                 ]

const.Pair_Info = [
#%%Pair_Info    ['RGID=763104N', 'RGLB=763104N', 'RGPL=illumina', 'RGPU=HWI-ST966-76', 'RGSM=N763104N', 'RGCN=wuxiapp', 'RGDS=exon-genome'],
                   ]


#[output_folder]
#%%Output_Folder  const.Output_Folder = 'result_763104N'
'''



mypath = os.getcwd()

n=[0]
#print 'const.Pair_File = ',a
def MakeConfig(dir,Outfold,pipeline):
    NGSToolkit_path='/gpfs2/home/wanguan2000/'
    Output_Folder = '/gpfs3/home/wanguan2000/result3_NGS/'
    config_NGS = '/gpfs3/home/wanguan2000/config3_NGS/'
    dir_sample = dir.replace('Sample_','')

    fastqR1 =  os.path.join(mypath, dir,dir_sample+'_R1.fastq')
    fastqR2 =  os.path.join(mypath, dir,dir_sample+'_R2.fastq')

    with open(Outfold+'/config_'+dir_sample+'.py','w') as infile:
       with open('config_depseq_turseq.py','rU') as f:
           for line in f:
               if not line:
                   break
               line = line.rstrip()
               if line.startswith('#%%Pair_File'):
                   infile.write("Pair_File = [['%s','%s'],]\n" % (fastqR1, fastqR2))
               elif line.startswith('#%%Pair_Info'):
                   infile.write("Pair_Info = [['RGID=%s', 'RGLB=%s', 'RGPL=illumina', 'RGPU=HWI-ST966', 'RGSM=%s', 'RGCN=GC', 'RGDS=exon-genome'],]\n" % (dir_sample, dir_sample, dir_sample))
               elif line.startswith('#%%Output_Folder'):
                   infile.write("Output_Folder = '%s%s/result_%s'\n" % (Output_Folder,Outfold,dir_sample))
                   #infile.write("Output_Folder = '/gpfs2/home/wanguan2000/result2_NGS/"+Outfold+"/result_%s'\n" % (dir))
               else:
                   infile.write(line+'\n')
#pipeline commad
    with open(Outfold+'/command.txt','a') as cmd:
        #cmd.write(("python "+NGSToolkit_path+"NGSToolkit/pipeline_NGS/"+pipeline+' '+config_NGS+Outfold+"/config_%s.py >"+Output_Folder+Outfold+"/nohup_%s.txt\n") % (dir_sample,dir_sample))
        cmd.write(("nohup python "+NGSToolkit_path+"NGSToolkit/pipeline_NGS/"+pipeline+' '+config_NGS+Outfold+"/config_%s.py >"+Output_Folder+Outfold+"/nohup_%s.txt 2>&1 &\n") % (dir_sample,dir_sample))

    return


#########initialization###############
#Output_Folder check###

Outfold = sys.argv[1]
pipeline = sys.argv[2]
try:
    os.makedirs(Outfold)
except OSError as inst:
    print inst.args
    print Outfold + " is exist, you should change the Output_Folder name!!!"
    raise SystemExit

files = os.listdir(mypath)
for dirname in files:
    if os.path.isdir(dirname) and not dirname == Outfold:
        MakeConfig(dirname,Outfold,pipeline)



