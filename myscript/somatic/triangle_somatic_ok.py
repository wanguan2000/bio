__author__ = 'wanguan2000'
import sys
import re
import os.path
import os
from myscript import *




def somatic(allvcf, somatic_samples, somatic_pair):
    sample_index = {}
    somatic_vcf_all = StringMeth().changeExtension(allvcf, '_somatic_all.vcf')
    somatic_vcf_het = StringMeth().changeExtension(allvcf, '_somaticSNP_het.vcf')
    somatic_vcf_hom = StringMeth().changeExtension(allvcf, '_somaticSNP_hom.vcf')
    #pattern2 = re.compile(r'.*MQ=(\d+\.\d+);')
    with open(somatic_vcf_all, 'w') as input_all:
        with open(somatic_vcf_het, 'w') as input_het:
            with open(somatic_vcf_hom, 'w') as input_hom:
                with open(allvcf, 'rU') as f:
                    for line in f:
                        if not line:
                            break
                        line = line.rstrip()
                        if not line.startswith('#') and not 'TruthSensitivityTranche' in line and not 'LowQual' in line:
                        #if not line.startswith('#') and not 'LowQual' in line:

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
                                           NALT < 3 and Qual >= 50.0 and sampleN_DP >= 20 and sampleT_DP >= 15 and sampleN_GQ >= 40.0 and sampleT_GQ >= 40.0 and sampleN_GT == '0/0' and sampleT_GT == '0/1') or (
                                        NALT < 4 and Qual >= 50.0 and sampleN_DP >= 20 and sampleT_DP >= 10 and sampleN_GQ >= 40.0 and sampleT_GQ >= 30.0 and sampleN_GT == '0/0' and sampleT_GT == '1/1'):
                                        #print sampledict[num[0]]+'\t'+mykey+'\t'+line
                                        result_somatic.append(1)
                                    elif TREF < 4 and Qual >= 50.0 and sampleN_DP >= 20 and sampleT_DP >= 15 and sampleN_GQ >= 40.0 and sampleT_GQ >= 35.0 and sampleN_GT == '0/1' and sampleT_GT == '1/1':
                                        result_somatic.append(1)
                                    else:
                                        result_somatic.append(0)
                                else:
                                    #pass
                                    result_somatic.append(0)
                            if sum(result_somatic) >= 1:
                                result_somatic = map(str, result_somatic)
                                if sampleN_GT == '0/0':

                                    if not spline[sample_index[somatic_pair[0][1]]].startswith('0/0'):
                                        input_hom.write(line + '\t' + '\t'.join(result_somatic) + '\n')
                                        input_all.write(line + '\t' + '\t'.join(result_somatic) + '\n')
                                elif sampleN_GT == '0/1':
                                    if not spline[sample_index[somatic_pair[0][1]]].startswith('0/0'):
                                        input_het.write(line + '\t' + '\t'.join(result_somatic) + '\n')
                                        input_all.write(line + '\t' + '\t'.join(result_somatic) + '\n')
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
                            input_all.write(line + '\t' + '\t'.join([x + '-' + y for x, y in somatic_pair]) + '\n')



'''
somatic_samples = ['A3', 'B3']
somatic_pair = [['B3', 'A3'],]
somatic('jieguo/a/A3_ALLmerge_realign_mate_recal_raw_indel_filtered.vcf',
        somatic_samples, somatic_pair)
somatic('jieguo/a/A3_ALLmerge_realign_mate_recal_raw_snp_filtered.vcf',
        somatic_samples, somatic_pair)

somatic_samples = ['A8', 'B8']
somatic_pair = [['B8', 'A8'],]
somatic('jieguo/a/A8_ALLmerge_realign_mate_recal_raw_indel_filtered.vcf',
        somatic_samples, somatic_pair)
somatic('jieguo/a/A8_ALLmerge_realign_mate_recal_raw_snp_filtered.vcf',
        somatic_samples, somatic_pair)

somatic_samples = ['A9', 'B9']
somatic_pair = [['B9', 'A9'],]
somatic('jieguo/a/A9_ALLmerge_realign_mate_recal_raw_indel_filtered.vcf',
        somatic_samples, somatic_pair)
somatic('jieguo/a/A9_ALLmerge_realign_mate_recal_raw_snp_filtered.vcf',
        somatic_samples, somatic_pair)

somatic_samples = ['A10', 'B10']
somatic_pair = [['B10', 'A10'],]
somatic('jieguo/a/A10_ALLmerge_realign_mate_recal_raw_indel_filtered.vcf',
        somatic_samples, somatic_pair)
somatic('jieguo/a/A10_ALLmerge_realign_mate_recal_raw_snp_filtered.vcf',
        somatic_samples, somatic_pair)

somatic_samples = ['A12', 'B12']
somatic_pair = [['B12', 'A12'],]
somatic('jieguo/a/A12_ALLmerge_realign_mate_recal_raw_indel_filtered.vcf',
        somatic_samples, somatic_pair)
somatic('jieguo/a/A12_ALLmerge_realign_mate_recal_raw_snp_filtered.vcf',
        somatic_samples, somatic_pair)


somatic_samples = ['A14', 'B14']
somatic_pair = [['B14', 'A14'],]
somatic('jieguo/a/A14_ALLmerge_realign_mate_recal_raw_indel_filtered.vcf',
        somatic_samples, somatic_pair)
somatic('jieguo/a/A14_ALLmerge_realign_mate_recal_raw_snp_filtered.vcf',
        somatic_samples, somatic_pair)


somatic_samples = ['A26', 'B26']
somatic_pair = [['B26', 'A26'],]
somatic('jieguo/a/A26_ALLmerge_realign_mate_recal_raw_indel_filtered.vcf',
        somatic_samples, somatic_pair)
somatic('jieguo/a/A26_ALLmerge_realign_mate_recal_raw_snp_filtered.vcf',
        somatic_samples, somatic_pair)


somatic_samples = ['A27', 'B27']
somatic_pair = [['B27', 'A27'],]
somatic('jieguo/a/A27_ALLmerge_realign_mate_recal_raw_indel_filtered.vcf',
        somatic_samples, somatic_pair)
somatic('jieguo/a/A27_ALLmerge_realign_mate_recal_raw_snp_filtered.vcf',
        somatic_samples, somatic_pair)


'''
somatic_samples = ['C3', 'C4','D3', 'D4']
somatic_pair = [['D3', 'C3'],['D4', 'C4'],['C3', 'C4'],['C4', 'C3'],['D3', 'D4'],['D4', 'D3']]
somatic('C3_ALLmerge_realign_mate_recal_raw_indel_filtered.vcf',
        somatic_samples, somatic_pair)
somatic('C3_ALLmerge_realign_mate_recal_raw_snp_filtered.vcf',
        somatic_samples, somatic_pair)



somatic_samples = ['C21', 'C22','D21', 'D22']
somatic_pair = [['D21', 'C21'],['D22', 'C22'],['C21', 'C22'],['C22', 'C21'],['D21', 'D22'],['D22', 'D21']]
somatic('C21_ALLmerge_realign_mate_recal_raw_indel_filtered.vcf',
        somatic_samples, somatic_pair)
somatic('C21_ALLmerge_realign_mate_recal_raw_snp_filtered.vcf',
        somatic_samples, somatic_pair)




somatic_samples = ['C23', 'C24','D23', 'D24']
somatic_pair = [['D23', 'C23'],['D24', 'C24'],['C23', 'C24'],['C24', 'C23'],['D23', 'D24'],['D24', 'D23']]
somatic('C23_ALLmerge_realign_mate_recal_raw_indel_filtered.vcf',
        somatic_samples, somatic_pair)
somatic('C23_ALLmerge_realign_mate_recal_raw_snp_filtered.vcf',
        somatic_samples, somatic_pair)



somatic_samples = ['C27', 'C28','D27', 'D28']
somatic_pair = [['D27', 'C27'],['D28', 'C28'],['C27', 'C28'],['C28', 'C27'],['D27', 'D28'],['D28', 'D27']]
somatic('C27_ALLmerge_realign_mate_recal_raw_indel_filtered.vcf',
        somatic_samples, somatic_pair)
somatic('C27_ALLmerge_realign_mate_recal_raw_snp_filtered.vcf',
        somatic_samples, somatic_pair)


somatic_samples = ['C9','C10', 'D9', 'D10']
somatic_pair = [['D9', 'C9'],['D10', 'C10'],['C9', 'C10'],['C10', 'C9'],['D9', 'D10'],['D10', 'D9']]
somatic('C9_ALLmerge_realign_mate_recal_raw_indel_filtered.vcf',
        somatic_samples, somatic_pair)
somatic('C9_ALLmerge_realign_mate_recal_raw_snp_filtered.vcf',
        somatic_samples, somatic_pair)


#C10	C9	D10	D9


