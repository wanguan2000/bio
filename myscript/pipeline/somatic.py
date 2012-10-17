__author__ = 'wanguan2000'
import sys
import re
import os.path
import os
from myscript import *




def somatic(allvcf, somatic_samples, somatic_pair):
    sample_index = {}
    somatic_vcf_het = StringMeth().changeExtension(allvcf, '_somaticSNP_het.vcf')
    somatic_vcf_hom = StringMeth().changeExtension(allvcf, '_somaticSNP_hom.vcf')
    #pattern2 = re.compile(r'.*MQ=(\d+\.\d+);')
    with open(somatic_vcf_het, 'w') as input_het:
        with open(somatic_vcf_hom, 'w') as input_hom:
            with open(allvcf, 'rU') as f:
                for line in f:
                    if not line:
                        break
                    line = line.rstrip()
                    if not line.startswith('#') and not 'TruthSensitivityTranche' in line and not 'LowQual' in line:
                        spline = line.split('\t')

                        Qual = float(spline[5])
                        #match = re.search(pattern2, spline[7])
                        #MQ = float(match.group(1))

                        ##T-N
                        result_somatic = []
                        for num in somatic_pair:
                            sampleN = spline[sample_index[num[0]]]
                            sampleT = spline[sample_index[num[1]]]
                            if not sampleN.startswith('./.') and not sampleT.startswith('./.'):
                                sampleN_DP = int(sampleN.split(':')[2])
                                sampleN_GQ = float(sampleN.split(':')[3])
                                sampleN_GT = sampleN.split(':')[0]
                                #ALTrate = float(sampleN.split(':')[1].split(',')[1]) / sampleN_DP
                                NALT = int(sampleN.split(':')[1].split(',')[1])
                                NREF = int(sampleN.split(':')[1].split(',')[0])

                                TALT = int(sampleT.split(':')[1].split(',')[1])
                                TREF = int(sampleT.split(':')[1].split(',')[0])

                                #print sampleT

                                sampleT_DP = int(sampleT.split(':')[2])
                                sampleT_GQ = float(sampleT.split(':')[3])
                                sampleT_GT = sampleT.split(':')[0]
                                if (
                                       NALT < 3 and Qual >= 100.0 and sampleN_DP >= 20 and sampleT_DP >= 15 and sampleN_GQ >= 40.0 and sampleT_GQ >= 40.0 and sampleN_GT == '0/0' and sampleT_GT == '0/1') or (
                                    NALT < 4 and Qual >= 100.0 and sampleN_DP >= 20 and sampleT_DP >= 10 and sampleN_GQ >= 40.0 and sampleT_GQ >= 30.0 and sampleN_GT == '0/0' and sampleT_GT == '1/1'):
                                    #print sampledict[num[0]]+'\t'+mykey+'\t'+line
                                    result_somatic.append(1)
                                elif TREF < 4 and Qual >= 100.0 and sampleN_DP >= 20 and sampleT_DP >= 15 and sampleN_GQ >= 40.0 and sampleT_GQ >= 35.0 and sampleN_GT == '0/1' and sampleT_GT == '1/1':
                                    result_somatic.append(1)
                                else:
                                    result_somatic.append(0)
                        if sum(result_somatic) >= 1:
                            result_somatic = map(str, result_somatic)
                            if sampleN_GT == '0/0':
                                input_hom.write(line + '\t' + '\t'.join(result_somatic) + '\n')
                            elif sampleN_GT == '0/1':
                                input_het.write(line + '\t' + '\t'.join(result_somatic) + '\n')
                    elif line.startswith('#CHROM'):
                        chrom = line.split('\t')
                        for sample in somatic_samples:
                            try:
                                sample_index[sample] = chrom.index(sample)
                            except:
                                print 'sample name RGSM not exist'
                                raise SystemExit
                        input_het.write(line + '\t' + '\t'.join([x + '-' + y for x, y in somatic_pair]) + '\n')
                        input_hom.write(line + '\t' + '\t'.join([x + '-' + y for x, y in somatic_pair]) + '\n')



somatic_samples = ['951681B', '951681PA', '951681P3']
somatic_pair = [['951681B', '951681PA'], ['951681B', '951681P3']]

'''
somatic_samples = ['965756B', '965756PA', '965756P2']
somatic_pair = [['965756B', '965756PA'], ['965756B', '965756P2']]
'''
somatic('/home/wanguan2000/programe/NGSToolkit/xenograft/951681/i951681P3_ALLmerge_realign_mate_recal_raw_snp_filtered.vcf',
        somatic_samples, somatic_pair)