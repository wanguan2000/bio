__author__ = 'wanguan2000'
import sys
import re
import os.path
import os
from myscript import *


#1.blood 0/0
#2.blood 0/1
#3.blood 1/1 NO
#DP >10

def somatic_00(line, allname_dict, samples_triangle):
    result = ['0']
    result = result * len(samples_triangle)
    line = line.rstrip()
    spline = line.split('\t')
    Qual = float(spline[5])

    pattern = re.compile(r'.*DP=(\d+);')
    match = re.search(pattern, spline[7])
    DP = float(match.group(1))

    if Qual >= 100 and DP >= 15 * len(allname_dict):
        for i in range(0, len(result)):
            blood_index = allname_dict[samples_triangle[i][0]]
            cancer_index = allname_dict[samples_triangle[i][1]]
            xeno_index = allname_dict[samples_triangle[i][2]]

            blood = spline[blood_index]
            cancer = spline[cancer_index]
            xeno = spline[xeno_index]

            if blood.startswith('0/0') and not cancer.startswith('0/0') and not cancer.startswith(
                './.') and not xeno.startswith('0/0') and not xeno.startswith('./.'):
                result[i] = '1'
    if '1' in result:
        return result
    else:
        return None


def somatic_01(allvcf, somatic_samples, somatic_pair):
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


def somatic_11(allvcf, somatic_samples, somatic_pair):
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


def normalsam(line, normal_dict):
    result = 0
    chrom = line.split('\t')
    for normal in normal_dict:
        if chrom[normal_dict[normal]].startswith('0/0'):
            result = result + 0
        else:
            result = result + 1
    return result


############################################################
def getindex(line, somatic_samples):
    sample_index = {}
    line = line.rstrip()
    if line.startswith('#CHROM'):
        chrom = line.split('\t')
        for sample in somatic_samples:
            try:
                sample_index[sample] = chrom.index(sample)
            except:
                print sample, 'sample name RGSM not exist'
                raise SystemExit
    return sample_index


def family(line, fam_model, allname, allname_dict):
    result = 0
    line = line.rstrip()
    spline = line.split('\t')

    pattern = re.compile(r'.*DP=(\d+);')
    match = re.search(pattern, spline[7])
    DP = float(match.group(1))
    Qual = float(spline[5])

    if Qual >= 30 and DP >= 20 * len(allname_dict):
        for name in allname:
            if spline[allname_dict[name]].startswith(fam_model[name]):
                sample_GQ = float(spline[allname_dict[name]].split(':')[3])
                if sample_GQ >= 40.0:
                    result += 0
                else:
                    result += 1
            else:
                result += 1

        if not result > 0:
            return line
        else:
            return None



def callfamily_snp(allvcf,allname,family_model):
    result=[]
    with open(allvcf, 'rU') as f:
        for line in f:
            if not line:
                break
            line = line.rstrip()
            if line.startswith('#CHROM'):
                result.append(line)
                allname_dict = getindex(line, allname)
           # elif line.startswith('##'):
            #    print line

            #elif not line.startswith('#') and not 'TruthSensitivityTranche' in line and not 'LowQual' in line:
            elif not line.startswith('#') and not 'LowQual' in line:
                myresult = family(line, family_model, allname, allname_dict)
                #myresult = family(line,family_model_recessive,allname,allname_dict)
                '''
                result = normalsam(line,normal_dict)
                #0/0
                if result == 0:
                    result_00 = somatic_00(line, allname_dict, samples_triangle)
                    if result_00:
                        spline = line.split('\t')
                       # print line
                        print '\t'.join([spline.__getitem__(elem) for elem in rootkey]) +'\t'+'\t'.join(result_00)
                #0/0
                '''
                if myresult:
                    result.append(myresult)
        return result

def callfamily_indel(allvcf,allname,family_model):
    result=[]
    with open(allvcf, 'rU') as f:
        for line in f:
            if not line:
                break
            line = line.rstrip()
            if line.startswith('#CHROM'):
                result.append(line)
                allname_dict = getindex(line, allname)
           # elif line.startswith('##'):
            #    print line

            #elif not line.startswith('#') and not 'TruthSensitivityTranche' in line and not 'LowQual' in line:
            elif not line.startswith('#') and not 'LowQual' in line:
                myresult = family(line, family_model, allname, allname_dict)
                #myresult = family(line,family_model_recessive,allname,allname_dict)
                '''
                result = normalsam(line,normal_dict)
                #0/0
                if result == 0:
                    result_00 = somatic_00(line, allname_dict, samples_triangle)
                    if result_00:
                        spline = line.split('\t')
                       # print line
                        print '\t'.join([spline.__getitem__(elem) for elem in rootkey]) +'\t'+'\t'.join(result_00)
                #0/0
                '''
                if myresult:
                    result.append(myresult)
        return result



###j21
'''
allname = ['J21', 'J22', 'J23', 'J24']
family_model_dominant = {'J21': '0/1', 'J22': '0/0', 'J23': '0/1', 'J24': '0/1'}
family_model_recessive = {'J21': '1/1', 'J22': '0/1', 'J23': '1/1', 'J24': '1/1'}

#dominant: J21:0/1 J22:0/0 J23:0/1 J24:0/1
#recessive:J21:1/1 J22:0/1 J23:1/1 J24:1/1

vcf_SNP = 'J21_ALLmerge_realign_mate_recal_raw_snp_filtered.vcf'
vcf_Indel = 'J21_ALLmerge_realign_mate_recal_raw_indel_filtered.vcf'

resultSNP = callfamily_snp(vcf_SNP,allname,family_model_dominant)
print '\n'.join(resultSNP)

resultSNP = callfamily_indel(vcf_Indel,allname,family_model_dominant)
print '\n'.join(resultSNP)
'''
####
'''
###D804 D804_1	D804_4
allname = ['D804_1', 'D804_4']
family_model_recessive = {'D804_1': '1/1', 'D804_4': '1/1'}

vcf_SNP = '/home/wanguan2000/project/family/family/D804/D804_ALLmerge_realign_mate_recal_raw_snp_filtered.vcf'
vcf_Indel = '/home/wanguan2000/project/family/family/D804/D804_ALLmerge_realign_mate_recal_raw_indel_filtered.vcf'

resultSNP = callfamily_snp(vcf_SNP,allname,family_model_recessive)
#print '\n'.join(resultSNP)

resultSNP = callfamily_indel(vcf_Indel,allname,family_model_recessive)
print '\n'.join(resultSNP)
'''

###s7	S7_2	S7_4
allname = ['S7_2', 'S7_4']
family_model_recessive = {'S7_2': '1/1', 'S7_4': '1/1'}

vcf_SNP = '/home/wanguan2000/project/family/family/s7/S7_ALLmerge_realign_mate_recal_raw_snp_filtered.vcf'
vcf_Indel = '/home/wanguan2000/project/family/family/s7/S7_ALLmerge_realign_mate_recal_raw_indel_filtered.vcf'

resultSNP = callfamily_snp(vcf_SNP,allname,family_model_recessive)
#print '\n'.join(resultSNP)

resultSNP = callfamily_indel(vcf_Indel,allname,family_model_recessive)
print '\n'.join(resultSNP)


