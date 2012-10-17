#coding=utf-8
import sys
import re
import os.path
import os


def doFastq(Name_Files,mydir):
    os.chdir(mydir)
    runzcatR1 = ' '.join([r'zcat *combined_filtered_R1.fastq.gz >', Name_Files+'_R1.fastq'])
    print runzcatR1
    os.system(runzcatR1)

    runzcatR2 = ' '.join([r'zcat *combined_filtered_R2.fastq.gz >', Name_Files+'_R2.fastq'])
    print runzcatR2
    os.system(runzcatR2)

    try:
       os.makedirs('/gpfs/home/wanguan2000/Project_fastq/'+Output_Folder)
    except OSError as inst:
        print inst.args
        print Output_Folder + " is exist, you should change the Output_Folder name!!!"
        raise SystemExit
    os.system('mv ' + Name_Files + '_R*.fastq /gpfs/home/wanguan2000/Project_fastq/' + Name_Files + '/')
    os.system('chmod 777 /gpfs/home/wanguan2000/Project_fastq/' + Name_Files + ' -R')
    print "all ok"
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






