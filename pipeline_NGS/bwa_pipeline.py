#coding=utf-8
__author__ = 'wanguan2000'
import sys
import re
import os.path
import os
sys.path.insert(0,os.path.join(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0], 'programe_NGS'))
from python.myscript import *
from python.fastqc import *
from python.trim import *
from python.bwa_align import *
from python.sam2bamsortgroup import *
from python.bamindex import *
from python.GATKrealigned import *
from python.markduplicate import *
from python.fixmate import *
from python.GATKrecalibrate import *
from python.GATKunifiedGenotyper import *
from python.GATKselectvariant import *
from python.GATKvariantrecalibrate import *
from python.GATKvariantAnnotator import *


#########initialization###############
const = Init_Pipeline().doInit(sys.argv[1])


#Output_Folder check###
try:
    os.makedirs(const.Output_Folder)
    os.makedirs(const.Temp_Folder)
except OSError as inst:
    print inst.args
    print const.Output_Folder + " is exist, you should change the Output_Folder name!!!"
    raise SystemExit

###1. fastqc return none ##############
#Fastqc(const).doFastqc(const.Pair_File)
###2. DynamicTrim return list (.trimed)################
#my_trimed = Trim(const).DynamicTrim(const.Pair_File)

###3.bwa return list (.sam)################
my_sam = bwaMeth(const).bwaPairend(const.Pair_File)




