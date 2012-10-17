__author__ = 'wanguan2000'
import sys
import re
import os.path
import os
from myscript import *

class Somatic:
    def __init__(self, config):
        self.const = config

    def getindex(self, line, name):
        line = line.rstrip()
        if line.startswith('#CHROM'):
            chrom = line.split('\t')
        return chrom.index(name)

    def getSampleName(self, filename):
        with open(filename, 'rU') as f:
            for line in f:
                line = line.rstrip()
                if not line:
                    break
                if line.startswith('#CHROM'):
                    spline = line.split('\t')
                    break
        return [[spline[9], spline[10]],[spline[10], spline[9]]]

    def Filter(self, headname, line, somatic_pair):
        spline = line.split('\t')
        Qual = float(spline[self.getindex(headname, 'QUAL')])
        FILTER = spline[self.getindex(headname, 'FILTER')]
        INFO = spline[self.getindex(headname, 'INFO')]

        result_somatic = []
        for num in somatic_pair:
            #headname = headname+ '\t'+'\t'.join([x + '-' + y for x, y in num])
            sampleN = spline[self.getindex(headname, num[0])]
            sampleT = spline[self.getindex(headname, num[1])]
            if not sampleN.startswith('./.') and not sampleT.startswith('./.'):
                sampleN_DP = int(sampleN.split(':')[2])
                sampleN_GQ = float(sampleN.split(':')[3])
                sampleN_GT = sampleN.split(':')[0]
                sampleT_DP = int(sampleT.split(':')[2])
                sampleT_GQ = float(sampleT.split(':')[3])
                sampleT_GT = sampleT.split(':')[0]

                #ALTrate = float(sampleN.split(':')[1].split(',')[1]) / sampleN_DP
                NALT = int(sampleN.split(':')[1].split(',')[1])
                NREF = int(sampleN.split(':')[1].split(',')[0])
                TALT = int(sampleT.split(':')[1].split(',')[1])
                TREF = int(sampleT.split(':')[1].split(',')[0])
                #0/0 0/1
                #0/0 1/1
                #0/1 1/1
                if (
                       NALT < 3 and Qual >= 50.0 and sampleN_DP >= 20 and sampleT_DP >= 15 and sampleN_GQ >= 40.0 and sampleT_GQ >= 40.0 and sampleN_GT == '0/0' and sampleT_GT == '0/1') or (
                    NALT < 4 and Qual >= 50.0 and sampleN_DP >= 20 and sampleT_DP >= 10 and sampleN_GQ >= 40.0 and sampleT_GQ >= 30.0 and sampleN_GT == '0/0' and sampleT_GT == '1/1'):
                    #print sampledict[num[0]]+'\t'+mykey+'\t'+line
                    result_somatic.append(1)
                elif TREF < 4 and Qual >= 50.0 and sampleN_DP >= 20 and sampleT_DP >= 15 and sampleN_GQ >= 40.0 and sampleT_GQ >= 35.0 and sampleN_GT == '0/1' and sampleT_GT == '1/1':
                    result_somatic.append(1)
                else:
                    result_somatic.append(0)
            else:
                result_somatic.append(0)
        if sum(result_somatic) >= 1:
            result_somatic = map(str, result_somatic)
            return result_somatic
        else:
            return None

    def pipeline(self, somatic_pair, snpfile):
        #snp
        snp_result = []
        with open(snpfile, 'rU') as f:
            for line in f:
                line = line.rstrip()
                if not line:
                    break
                if line.startswith('#CHROM'):
                    headname = line
                elif not line.startswith('#') and not 'TruthSensitivityTranche' in line and not 'LowQual' in line:
                    result = self.Filter(headname, line, somatic_pair)
                    if result:
                        snp_result.append(line + '\t' + '\t'.join(result))
        somatic_snp = '_'.join([x + '-' + y for x, y in somatic_pair]) + '_somatic_' + snpfile
        with open(somatic_snp, 'w') as input_all:
            input_all.write(headname + '\t' + '\t'.join([x + '-' + y for x, y in somatic_pair]) + '\n')
            input_all.write('\n'.join(snp_result))

'''
somatic_pair = [['D21', 'C21'],['D22', 'C22'],['C21', 'C22'],['C22', 'C21'],['D21', 'D22'],['D22', 'D21']]
Somatic('').pipeline(somatic_pair,'C21_ALLmerge_realign_mate_recal_raw_snp_filtered.vcf')
Somatic('').pipeline(somatic_pair,'C21_ALLmerge_realign_mate_recal_raw_indel_filtered.vcf')
'''

files = os.listdir('.')
for dirname in files:
    if not os.path.isdir(dirname) and not dirname.startswith('.'):
        if '_snp_filtered' in dirname:
            somatic_pair = Somatic('').getSampleName(dirname)
            Somatic('').pipeline(somatic_pair, dirname)
        if '_indel_filtered' in dirname:
            somatic_pair = Somatic('').getSampleName(dirname)
            Somatic('').pipeline(somatic_pair, dirname)


