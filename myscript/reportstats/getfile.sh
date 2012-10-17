#!/bin/sh
mydir="re_G3"
echo $mydir
mkdir $mydir
mkdir $mydir/QC
mkdir $mydir/CSV
mkdir $mydir/stats
mkdir $mydir/VCF

cp */*_QCtbale.txt $mydir/QC
cp */*_filtered_Hqual.csv $mydir/CSV
cp */*_Hqual_stats.txt $mydir/stats
cp */*_filtered_Hqual.vcf $mydir/VCF







