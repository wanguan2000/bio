__author__ = 'wanguan2000'
# -*- coding: utf-8 -*-
import sys
import os
import locale
import codecs
import re



class Stats_Exon_Position:
    def getindex(self, line, keyroot):
        line = line.rstrip()
        if line.startswith('#CHROM'):
            chrom = line.split('\t')
        return [chrom.index(a) for a in keyroot]

    def getSNP(self,filelist,keyroot,resultinfo,QUAL='QUAL'):
        mydict={}
        collist = []
        myresult={}
        for filename in filelist:
            filename2 = re.sub('_.*', '', filename)
            collist.append(filename2)

            with open(filename, 'rU') as f:
                for line in f:
                    line = line.rstrip()
                    if not line:
                        break
                    if line.startswith('#CHROM'):
                        keyroot_num = self.getindex(line,keyroot)
                        result_num = self.getindex(line,resultinfo)
                        QUAL_num = self.getindex(line,['QUAL'])[0]
                        Exon_num = self.getindex(line,['Exon_syno'])[0]
                    else:
                        spline = line.split('\t')
                        if not spline[Exon_num].startswith('NA'):# and float(spline[QUAL_num]) > 255.0:
                            mykey = '\t'.join([spline.__getitem__(elem) for elem in keyroot_num])
                            myresult[mykey]= '\t'.join([spline.__getitem__(elem) for elem in result_num])
                            if mykey in mydict.keys():
                                mydict[mykey].update({filename2:1})
                            else:
                                mydict[mykey]={filename2:1}
        return mydict,collist,myresult
    def writereult(self,resultinfo,redict,collist,myresult,name='snp'):
        result2 = []
        for a in redict.keys():
            result2.append(str(sum(redict[a].values()))+'\t'+myresult[a]+'\t'+'\t'.join([str(redict[a].get(b,0)) for b in collist]))
        result2 = sorted(result2,key=lambda x: int(x.split('\t')[0]),reverse=True)
        with open('position_'+name+'_allsamples.xls', 'w') as infile:
            infile.write('#Sum\t'+'\t'.join(resultinfo)+'\t'+'\t'.join(collist)+'\n')
            infile.write('\n'.join(result2))

    def pipeline(self,):
        resultinfo=['#CHROM','Start','End','REF','ALT','Gene_location','Gene','Exon_syno','Exon','dbSNP','1000G','GWAS','Visift','TFbs','Mirna','Mirnatarget','ConservedElements','cosmic']
        keyroot=['#CHROM','Start','End','REF','ALT',]

        QUAL='QUAL'
        Exon_syno='Exon_syno'
        #SNP
        filelist=[]
        for dirname in os.listdir('.'):
            if '_snp_filtered' in dirname and not dirname.startswith('.'):
                filelist.append(dirname)
        redict,collist,myresult = self.getSNP(filelist,keyroot,resultinfo,QUAL='QUAL')
        self.writereult(resultinfo,redict,collist,myresult,'SNP')
        #indel
        filelist=[]
        for dirname in os.listdir('.'):
            if '_indel_filtered' in dirname and not dirname.startswith('.'):
                filelist.append(dirname)
        redict,collist,myresult = self.getSNP(filelist,keyroot,resultinfo,QUAL='QUAL')
        self.writereult(resultinfo,redict,collist,myresult,'indel')



Stats_Exon_Position().pipeline()





