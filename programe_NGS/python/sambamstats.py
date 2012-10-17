__author__ = 'wanguan2000'
#coding=utf-8
import os.path
import os
import sys
import re
import commands



'''

##计算base覆盖率
 coverageBed -abam sort.bam  -b sureselect.bed -hist >base.txt

##计算reads个数
 coverageBed -abam sort.bam  -b sureselect.bed >resulr.txt


print commands.getstatusoutput('coverageBed -abam sort.bam  -b sureselect.bed >resulr.txt')


pdf("cumsum2.pdf",width=8)
read.table("okpc3.txt",sep="\t") -> mydata
1 - cumsum(c(0,mydata[,5])) -> mydata4
y<- mydata4*100
x<- 1:length(mydata4)
plot(x,y,cex=0,xlim=c(0,300),bty="n",xaxt="n",ylab="Fraction of target bases(%)",xlab="Cumulative Sequencing depth")
axis(1,at=c(seq(0, 300, by=20)))
lines(x,y,col="red",lwd=2)
abline(v=20,col="blue",lty=2)
dev.off()


'''

class SamBamStats:

    def SamStats(self,filename):
        total_read = 0
        base_mismatch = 0.0
        base_all = 0.0
        read_NOmismatch = 0.0
        total_unique = 0.0
        result_list = []
        p = re.compile(r'\tXM:i:(\d+)')

        with open(filename, 'rU') as f:
            for line in f:
                line = line.rstrip()
                if not line:
                    break
                if not line.startswith('@'):
                    total_read += 1
                    if 'XT:A:U' in line:
                        total_unique += 1
                    if 'XM:i:0' in line:
                        read_NOmismatch += 1
                    if p.findall(line):
                        base_mismatch += int(p.findall(line)[0])
                        spline = line.split('\t')
                        base_all += len(spline[9])

        result_list.append('Total effective data yield(Mb):\t%0.2f' % (total_read*100.0/1000000))
        result_list.append('Total effective reads:\t%d' % total_read)
        result_list.append(('Uniquely mapping reads rate:\t%0.2f%%' % (total_unique * 100 / total_read)))
        result_list.append(('No-mismatch mapping reads rate:\t%0.2f%%' % (read_NOmismatch * 100 / total_read)))
        result_list.append(('Mismatch alignment bases rate:\t%0.2f%%' % (base_mismatch * 100 / base_all)))
        return result_list

    def Align_PF(self,filename):
        all_read = 0.0
        aligned_read = 0.0
        result_list = []
        with open(filename, 'rU') as f:
            for line in f:
                line = line.rstrip()
                if not line:
                    break
                if line.startswith('NoCoordinateCount'):
                    line = float(line.replace('NoCoordinateCount= ', ''))
                    all_read += line
                else:
                    spline = line.split('\t')
                    all_read += float(spline[-1].replace('Unaligned= ', ''))
                    all_read += float(spline[-2].replace('Aligned= ', ''))
                    aligned_read += float(spline[-2].replace('Aligned= ', ''))
            result_list.append(str(all_read))
            result_list.append('Total reads  alignment to reference genome:\t%0.0f' % (aligned_read))
            result_list.append(('The ratio of reads alignment to reference genome:\t%0.2f%%' % (aligned_read * 100 / all_read)))
        return result_list

    def ReadsCover(self,filename, totalreads=44394028 * 2):
        number_region = 0.0
        sequenced_region = 0.0
        target_reads = 0.0
        result_list = []
        with open(filename, 'rU') as f:

            for line in f:
                line = line.rstrip()
                if not line:
                    break
                number_region += 1
                spline = line.split('\t')
                target_reads += float(spline[-4])
                if float(spline[-4]) > 1:
                    sequenced_region += 1
            #Reads on target regions rate
            result_list.append(('%0.2f%%' % (target_reads * 100.0 / totalreads)))
            #Fraction of target covered by reads
            result_list.append(('%0.2f%%' % (sequenced_region * 100.0 / number_region)))
        return result_list


    def BaseCover(self,filename, total_Base=0):
        map_Base = 0.0
        result_list = []
        cover_list = []
        with open(filename, 'rU') as f:

            for line in f:
                line = line.rstrip()
                if not line:
                    break
                if line.startswith('all'):
                    spline = line.split('\t')
                    #print spline[2]
                    total_Base = int(spline[-2])
                    map_Base = map_Base + int(spline[1]) * int(spline[2])
                    cover_list.append(float(spline[-1]))
        cover4 = sum(cover_list[0:4])
        cover10 = sum(cover_list[0:10])
        cover20 = sum(cover_list[0:20])


        #print map_Base/total_Base

        #Mean coverage sequencing depth on target
        result_list.append(('%0.0f' % (map_Base / total_Base)))
        #Fraction of target bases covered
        result_list.append(('%0.2f%%' % ((1 - cover_list[0]) * 100)))
        #>=4X coverage
        result_list.append(('%0.2f%%' % ((1 - cover4) * 100)))
        #>=10X coverage
        result_list.append(('%0.2f%%' % ((1 - cover10) * 100)))
        #>=20X coverage
        result_list.append(('%0.2f%%' % ((1 - cover20) * 100)))
        #total bases
        result_list.append(('%s' % (str(total_Base))))
        return result_list

    def Whole_BaseCover(self,filename, total_Base=0):
        map_Base = 0.0
        result_list = []
        cover_list = []
        with open(filename, 'rU') as f:

            for line in f:
                line = line.rstrip()
                if not line:
                    break
                if line.startswith('genome'):
                    spline = line.split('\t')
                    #print spline[2]
                    total_Base = int(spline[-2])
                    map_Base = map_Base + int(spline[1]) * int(spline[2])
                    cover_list.append(float(spline[-1]))
        cover4 = sum(cover_list[0:4])
        cover10 = sum(cover_list[0:10])
        cover20 = sum(cover_list[0:20])


        #print map_Base/total_Base

        #Mean coverage sequencing depth on target
        result_list.append(('%0.0f' % (map_Base / total_Base)))
        #Fraction of target bases covered
        result_list.append(('%0.2f%%' % ((1 - cover_list[0]) * 100)))
        #>=4X coverage
        result_list.append(('%0.2f%%' % ((1 - cover4) * 100)))
        #>=10X coverage
        result_list.append(('%0.2f%%' % ((1 - cover10) * 100)))
        #>=20X coverage
        result_list.append(('%0.2f%%' % ((1 - cover20) * 100)))
        #total bases
        result_list.append(('%s' % (str(total_Base))))
        return result_list


#print SamBamStats().ReadsCover('ReadsCove.txt')
#print SamBamStats().BaseCover('BaseCove.txt')

'''
print Align_PF('A549_R1_A549_R2_sort.bam_stats.txt')
print ReadsCover('resulr.txt')
print BaseCover('/home/wanguan2000/桌面/Pfalciparum3D7/bam/gene_2.txt')
print SamStats('/home/wanguan2000/programe/myNGS/myscript/A549_R1_A549_R2.sam')

'''







