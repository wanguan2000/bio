__author__ = 'wanguan2000'



from SOAPpy import WSDL
from numpy import *
import pprint
import sys
import download_url
import random
#!/usr/bin/env python

from SOAPpy import WSDL

class Gene2pathway:
    def select_color(self,number,colors=['yellow','red','green','blue','#00FFFF']):
        try:
            number = int(number)
        except :
            print "you should input number value"
            raise SystemExit
        return colors[number]


    def openfile(self,filename,colors):
        mycolors={}
        with open(filename,'rU') as f:
            genelist=[]
            for line in f:
                line = line.rstrip()
                if not line:
                    break
                line = line.rstrip()
                spline = line.split('\t')
                genelist.append(spline[0])
                color = self.select_color(spline[1],colors)
                mycolors[spline[0]] = color
            return genelist,mycolors
        
    def gene2pathway(self,genelist):
        wsdl = 'http://soap.genome.jp/KEGG.wsdl'
        serv = WSDL.Proxy(wsdl)
        mypathway = {}
        for gene in genelist:
            pathway = serv.get_pathways_by_genes([gene.lower()])
            print gene
            print pathway
            for way in pathway:
                if way in mypathway:
                    print way
                    print mypathway
                    #mypathway[way].add(gene)
                    mypathway[way].append(gene)
                else:
                    #mypathway[way] = {gene}
                    mypathway[way] = [gene]
        return mypathway

    def down_url(self,mypathway,mycolors):
        wsdl = 'http://soap.genome.jp/KEGG.wsdl'
        serv = WSDL.Proxy(wsdl)
        result_url=[]
        print mypathway
        for pathway in mypathway:
            bg_list = []
            for gene in mypathway[pathway]:
                bg_list.append(mycolors[gene])
            fg_list = ['#000000']*len(mypathway[pathway])
            url=serv.color_pathway_by_objects(pathway, list(mypathway[pathway]), fg_list, bg_list)
            download_url.download(url)
            result_url.append(url)
        return result_url

    def pipeline(self,inputfile,outfile,colors):
        genelist,mycolors = self.openfile(inputfile,colors)
        mypathway = self.gene2pathway(genelist)
        result_url = self.down_url(mypathway,mycolors)
        with open(outfile,'w') as infile:
            for path in mypathway:
                infile.write(('%s\t%s\n') % (path,','.join(mypathway[path])))
        return result_url


###############
colors=['blue','red','blue','yellow','yellow']
inputfile = 'human.txt'
outfile = 'pathway_gene_2.txt'
Gene2pathway().pipeline(inputfile,outfile,colors)





