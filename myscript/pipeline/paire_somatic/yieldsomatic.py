#!/usr/bin/env python
__author__ = 'wanguan2000'
# -*- coding: utf-8 -*-
import sys
import os
import locale
import codecs
import re




mypath = os.getcwd()

n=[0]
#print 'const.Pair_File = ',a
def MakeConfig(spline,Outfold,pipeline):
    config_file = 'config_somatic.py'
    NGSToolkit_path='/gpfs2/home/wanguan2000/'
    Output_Folder = '/gpfs3/home/wanguan2000/result3_NGS/'
    config_NGS = '/gpfs3/home/wanguan2000/config3_NGS/'
    bam1='/gpfs3/home/wanguan2000/result3_NGS/G3_1/result_Sample_%s/%s_R1_%s_R2_sort_realign_dedup_mate_recal.bam' %(spline[0],spline[0],spline[0])
    bam2 = '/gpfs3/home/wanguan2000/result3_NGS/G4_1/result_Sample_%s/%s_R1_%s_R2_sort_realign_dedup_mate_recal.bam' %(spline[1],spline[1],spline[1])


    with open(Outfold+'/config_somatic_'+spline[0]+'.py','w') as infile:
        with open(config_file,'rU') as f:
            for line in f:
                if not line:
                    break
                line = line.rstrip()
                if line.startswith('#%%somatic_samples'):
                    infile.write("somatic_samples = ['%s','%s',]\n" % (bam1, bam2))
                elif line.startswith('#%%Output_Folder'):
                    infile.write("Output_Folder = '%s%s/result_somatic_%s'\n" % (Output_Folder,Outfold,spline[0]))
                    #infile.write("Output_Folder = '/gpfs2/home/wanguan2000/result2_NGS/"+Outfold+"/result_%s'\n" % (dir))
                else:
                    infile.write(line+'\n')
                #pipeline commad
    with open(Outfold+'/command.txt','a') as cmd:
        #cmd.write(("nohup python "+NGSToolkit_path+"NGSToolkit/pipeline_NGS/"+pipeline+"config_NGS/"+Outfold+"/config_somatic_%s.py >"+NGSToolkit_path+"result2_NGS/"+Outfold+"/nohup_somatic_%s.txt 2>&1 &\n") % (spline[0],spline[0]))
        cmd.write(("nohup python "+NGSToolkit_path+"NGSToolkit/pipeline_NGS/"+pipeline+' '+config_NGS+Outfold+"/config_somatic_%s.py >"+Output_Folder+Outfold+"/nohup_%s.txt 2>&1 &\n") % (spline[0],spline[0]))
    return


#########initialization###############
#Output_Folder check###

#print (head1)%('a','s','asd')
#python yieldsomatic.py G4 somatic_family_calling.py
#'/gpfs/home/wanguan2000/NGSToolkit/pipeline_NGS/somatic_family_calling.py'
'''
Outfold = sys.argv[1]
pipeline = sys.argv[2]
'''

Outfold = 'G3_G4'
pipeline = 'somatic_family_calling.py'


try:
    os.makedirs(Outfold)
except OSError as inst:
    print inst.args
    print Outfold + " is exist, you should change the Output_Folder name!!!"
    raise SystemExit



filename='paire.txt'
with open(filename, 'rU') as f:
    for line in f:
        line = line.rstrip()
        if not line:
            break
        if not line.startswith('#'):
            spline = line.split('\t')
            MakeConfig(spline,Outfold,pipeline)




