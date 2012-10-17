__author__ = 'wanguan2000'
#coding=utf-8
import sys
import re
import os.path
import os

'''
#!/bin/sh
WEBROOT="/home/wanguan2000/django/ucsc"
rsync -avP rsync://hgdownload.cse.ucsc.edu/htdocs/ $WEBROOT/
mkdir -p $WEBROOT/goldenPath/hg19/database/
rsync -avP --delete --max-delete=20 rsync://hgdownload.cse.ucsc.edu/genome/goldenPath/hg19/database/ $WEBROOT/goldenPath/hg19/database/
rsync -avP --delete --max-delete=20 rsync://hgdownload.cse.ucsc.edu/gbdb/ ./gbdb/
'''

myWEBROOT = "/home/wanguan2000/django/ucsc"
os.system('rsync -avP rsync://hgdownload.cse.ucsc.edu/htdocs/ '+myWEBROOT+'/')
os.system('mkdir -p '+myWEBROOT+'/goldenPath/hg19/database/')
os.system('rsync -avP --delete --max-delete=20 rsync://hgdownload.cse.ucsc.edu/genome/goldenPath/hg19/database/ '+myWEBROOT+'/goldenPath/hg19/database/')
os.system('rsync -avP --delete --max-delete=20 rsync://hgdownload.cse.ucsc.edu/gbdb/hg19 ./gbdb/')

