#!/usr/bin/env python
__author__ = 'wanguan2000'
from Bio import SeqIO
from myscript import *

seq=['/gpfs2/home/luoqin/fastq/NVS10001/WUXI004/FQ/pe_1.fq',
     '/gpfs2/home/luoqin/fastq/NVS10001/WUXI004/FQ/pe_2.fq',
     '/gpfs2/home/luoqin/fastq/NVS10001/WUXI029/FQ/pe_1.fq',
     '/gpfs2/home/luoqin/fastq/NVS10001/WUXI029/FQ/pe_2.fq',
     '/gpfs2/home/luoqin/fastq/NVS10001/WUXI058/FQ/pe_1.fq',
     '/gpfs2/home/luoqin/fastq/NVS10001/WUXI058/FQ/pe_2.fq',
     '/gpfs2/home/luoqin/fastq/NVS10001/WUXI002/FQ/pe_1.fq',
     '/gpfs2/home/luoqin/fastq/NVS10001/WUXI002/FQ/pe_2.fq',
     '/gpfs2/home/luoqin/fastq/NVS10001/WUXI005/FQ/pe_1.fq',
     '/gpfs2/home/luoqin/fastq/NVS10001/WUXI005/FQ/pe_2.fq',
     '/gpfs2/home/luoqin/fastq/NVS10001/WUXI036/FQ/pe_1.fq',
     '/gpfs2/home/luoqin/fastq/NVS10001/WUXI036/FQ/pe_2.fq',
     '/gpfs2/home/luoqin/fastq/NVS10001/WUXI062/FQ/pe_1.fq',
     '/gpfs2/home/luoqin/fastq/NVS10001/WUXI062/FQ/pe_2.fq',
     '/gpfs2/home/luoqin/fastq/NVS10001/WUXI003/FQ/pe_1.fq',
     '/gpfs2/home/luoqin/fastq/NVS10001/WUXI003/FQ/pe_2.fq',
     '/gpfs2/home/luoqin/fastq/NVS10001/WUXI015/FQ/pe_1.fq',
     '/gpfs2/home/luoqin/fastq/NVS10001/WUXI015/FQ/pe_2.fq',
     '/gpfs2/home/luoqin/fastq/NVS10001/WUXI056/FQ/pe_1.fq',
     '/gpfs2/home/luoqin/fastq/NVS10001/WUXI056/FQ/pe_2.fq',
     ]


for a in seq:
    print a
    standard_fastq = StringMeth().changeExtension(a, '.fastq')
    print standard_fastq
    SeqIO.convert(a, "fastq-illumina", standard_fastq, "fastq")


