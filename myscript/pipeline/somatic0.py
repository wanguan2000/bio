__author__ = 'wanguan2000'
import sys
import re
import os.path
import os
#from myscript import *


'''
n=0
range(1,len(a)-2)
n=len(a)-1
'''


def qusomatic(filename):
    mylist=[]
    with open(filename, 'rU') as f:
        for line in f:
            line = line.rstrip()
            if not line:
                break
            if line.startswith('#'):
                print line
            else:
                mylist.append(line)

    #n=0
    spline_now = mylist[0].split('\t')
    spline_next = mylist[0+1].split('\t')
    if int(spline_now[12]) == 0 and int(spline_now[13]) == 1:
        if (spline_now[0] == spline_next[0] and int(spline_now[1]) > int(spline_next[1])-500):
            print mylist[0]+'\tqu'
    else:
            print mylist[0]

    #range(1,len(a)-1)
    for n in  range(1,len(mylist)-1):
        spline_previous = mylist[n-1].split('\t')
        spline_now = mylist[n].split('\t')
        spline_next = mylist[n+1].split('\t')
        if int(spline_now[12]) == 0 and int(spline_now[13]) == 1:
            if (spline_now[0] == spline_previous[0] and int(spline_now[1]) < int(spline_previous[1])+500) or (spline_now[0] == spline_next[0] and int(spline_now[1]) > int(spline_next[1])-500):
                print mylist[n]+'\tqu'
            else:
                print mylist[n]

        else:
                print mylist[n]


    #n=len(mylist)
    spline_previous = mylist[len(mylist)-2].split('\t')
    spline_now = mylist[len(mylist)-1].split('\t')
    if int(spline_now[12]) == 0 and int(spline_now[13]) == 1:
        if (spline_now[0] == spline_previous[0] and int(spline_now[1]) < int(spline_previous[1])+500):
            print mylist[len(mylist)-1]+'\tqu'
    else:
            print mylist[len(mylist)-1]







qusomatic('/home/wanguan2000/programe/NGSToolkit/xenograft/2/i951681P3_ALLmerge_realign_mate_recal_raw_snp_filtered_somaticSNP_t1.vcf')









