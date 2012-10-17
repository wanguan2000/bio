__author__ = 'wanguan2000'
from Bio import SeqIO

'''
trimmed_primer_reads = (rec[11:] for rec in SeqIO.parse("SRR020192.fastq", "fastq") if rec.seq.startswith("GATGACGGTGT"))
count = SeqIO.write(trimmed_primer_reads, "with_primer_trimmed.fastq", "fastq")
print "Saved %i reads" % count

def trim_primer(record, primer):
    if record.seq.startswith(primer):
        return record[len(primer):]
    else:
        return record

trimmed_reads = (trim_primer(record, "GATGACGGTGT") for record in SeqIO.parse("SRR020192.fastq", "fastq"))
count = SeqIO.write(trimmed_reads, "trimmed.fastq", "fastq")
print "Saved %i reads" % count
'''




'WGC000650_combined_filtered_R1.fastq'

trimmed_reads = (record[:75] for record in SeqIO.parse("WGC000650_combined_filtered_R1.fastq", "fastq"))
count = SeqIO.write(trimmed_reads, "trimmed.fastq", "fastq")
print "Saved %i reads" % count






