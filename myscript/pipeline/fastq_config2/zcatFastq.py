#coding=utf-8
import sys
import re
import os.path
import os


def doFastq(Name_Files,mydir):
    os.chdir(mydir)
    runzcatR1 = ' '.join([r'cat *_R1_*.fastq >', Name_Files+'_R1.fastq'])
    print runzcatR1
    os.system(runzcatR1)

    runzcatR2 = ' '.join([r'cat *_R2_*.fastq >', Name_Files+'_R2.fastq'])
    print runzcatR2
    os.system(runzcatR2)

    return None




mypath = os.getcwd()
files = os.listdir('.')
for dirname in files:
    if os.path.isdir(dirname) and not dirname.startswith('.'):
        mydir =  os.path.join(mypath, dirname)
        #out put file name and Project_fastq name
        Output_Folder = dirname.split('_')[-1]
        doFastq(Output_Folder,mydir)
        os.chdir(mypath)






