# -*- coding: utf-8 -*-
import sys
import re
import os.path
import os
from SOAPpy import WSDL
from numpy import *

def select_color(number):
    try:
        number = int(number)
    except :
        print "you should input number value"
        raise SystemExit
    colors=['#A73800','#FF6600','#FF981F','FFA500','04477C','#065FB9','#049FF1','#4499EE','#BEC0C2','#712704',
       '#BD7803','#FE9D01','#FFBB1C','#EED205','#FF8C05','#FDD283','#43A102','#A2B700','#C5DA01','#4C4C4C','#D4D4D4','#036803',
       '#3F813F','#55A255','#74A474','#DA891E','F6BF1C']

    return colors[number]

wsdl = 'http://soap.genome.jp/KEGG.wsdl'
serv = WSDL.Proxy(wsdl)

ec=open("Table_submit_kegg.EntreID.txt")

path2ec={}
ec_no=ec.readlines()
print ec_no
for i in ec_no:
   #print i
   obj_list=i.replace('\n','')
   #print obj_list.type()
   path=serv.get_pathways_by_genes([obj_list.lower()])
   if len(path)>=1:
      for j in path:
          if (j in path2ec.keys())==0 :        
              path2ec[j]=[obj_list.lower()]
          elif (j in path2ec.keys())==True:
              path2ec[j].extend([obj_list.lower()])
print path2ec
'''
import pprint
import sys
import download_url
## Usage: download(r'你要下载的python文件的url地址')

import random
colors={'#000000':['#A73800','#FF6600','#FF981F','FFA500','04477C','#065FB9','#049FF1','#4499EE','#BEC0C2','#712704',
       '#BD7803','#FE9D01','#FFBB1C','#EED205','#FF8C05','#FDD283','#43A102','#A2B700','#C5DA01','#4C4C4C','#D4D4D4','#036803',
       '#3F813F','#55A255','#74A474','#DA891E','F6BF1C']}


for i in path2ec.keys(): 
    bg=[random.choice(colors['#000000'])]
    fg=['#000000']
    for j in range(len(path2ec[i])):
        bg.append(random.choice(colors['#000000']))
        
        fg.append('#000000')
    url=serv.color_pathway_by_objects(i, path2ec[i], fg, bg)
    download_url.download(url)




#### wirte out path-> EC.no tables ; and No genes in pathways.

out = open("Table_path2ec_keys_list.txt","w")
sample_list = [line+'\n' for line in path2ec.keys()]
out.writelines(sample_list)



sample_list = [line+'\n' for line in path2ec.values()]
out.writelines(path2ec.values())


file = open("Table_path2ec_keys_list.txt","w")
file.writelines(["%s\n" % item for item in path2ec.keys()])

for item in path2ec.keys():
  file.write("%s\n" % item)


file = open("Table_path2ec_values_list.txt","w")
file.writelines(["%s\n" % item for item in path2ec.values()])
'''
'''

#################  R code

## to creat a table from path2ec table generated from python 
## input:
## (1) Table_path2ec_values_list
## (2) Table_path2ec_keys_list
## to remove [ ' ] chars by hand and then :

keys<-readLines("Table_path2ec_keys_list.txt")
values<-readLines("Table_path2ec_values_list.txt")

## creat path2ec redandunt table in 2 columns : format pathmap \t ec.no



for i in range(1,len(values)):
    {
      k=strsplit(values[i],",")[[1]]
      for (j in 1:length(k))
         {
            write.table(cbind(k[j],keys[i],strsplit(keys[i],"path:map")[[1]][2]),"Table_path2ec_redudant_list.txt",row.names=F,col.names=F,quote=F,append=T,sep="\t")

         }

    }


#### to annotate EC enzyme names
##  from ftp://ftp.expasy.org/databases/enzyme/


###############################################################################
## stat pathway and KEGG EC enzymes frequency in seq2pathway tables


##############################################

seq2ec=read.table("Sample1_annotation_Seq2EC.annot",sep="\t")
seq2ec=as.matrix(seq2ec)
ec=read.csv("Table_EC_names.csv",sep="\t")
ec=as.matrix(ec)

ec2path=read.table("Table_path2ec_redudant_list.txt",sep="\t")
ec2path=as.matrix(ec2path)

path2name=read.table("keggMapDesc.txt",sep="\t")
path2name=as.matrix(path2name)
## make a full seq2ec2path2name in a table
useq=unique(seq2ec[,1])


for (i in 1:length(useq))
    {      
      uec=seq2ec[which(seq2ec[,1]==useq[i]),2]
      for (j in 1:length(uec))
          {
            if (uec[j] %in% ec2path[,1]){
            ec.name=ec[which(ec[,1]==strsplit(uec[j],"EC:")[[1]][2]),2]
            path.id=ec2path[which(ec2path[,1]==uec[j]),2]

            if(length(path.id)>0){
            seq2ec2ecname=cbind(t(seq2ec[i,]),ec.name)
            for (k in 1:length(path.id))
                {
                  #pathid=paste("has",strsplit(path.id[k],"path:map")[[1]][2],sep="")
                  path.name=path2name[which(path2name[,1]==path.id[k]),3]
                  if(length(path.name)>0)
                     {
                       write.table(cbind(seq2ec2ecname,path.id[k],path.name),"Table_seq2ec2path_desc_all.txt",sep="\t",row.names=F,col.names=F,quote=F,append=T)
                     }

                  if(length(path.name)==0)
                     {
                       write.table(pathid,"Table_missing_pathid.txt",sep="\t",row.names=F,col.names=F,quote=F,append=T)
                     }
              
                }
             }

            if(length(path.id)==0){
               write.table(seq2ec[i,2],"Table_missing_ECID.txt",sep="\t",row.names=F,col.names=F,quote=F,append=T)

              }
          }
         }
    }


##############################################

seq2ec2path<-read.csv("Table_seq2ec2path_desc_all.csv")

path<-unique(seq2ec2path[,c(5,6)])


fre.ec<-data.frame(table(seq2ec2path[,3]))
tbl.ec<-cbind(ec[match(fre.ec[,1],ec[,1]),],fre.ec[,2])
write.table(tbl.ec,"Table_seq2ec_EC_Frequency.txt",row.names=F,col.names=F,quote=F,sep="\t")

fre.path<-data.frame(table(seq2ec2path[,5]))
tbl.path<-cbind(path[match(fre.path[,1],path[,1]),],fre.path[,2])
write.table(tbl.path,"Table_seq2ec_Path_Frequency.txt",row.names=F,col.names=F,quote=F,sep="\t")


######### isoform stat

'''


















