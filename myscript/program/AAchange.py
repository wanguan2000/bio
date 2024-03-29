__author__ = 'wanguan2000'
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq
from Bio.Seq import reverse_complement, transcribe, back_transcribe, translate
from Bio.Seq import MutableSeq


my_seq2 = Seq("TGATACAGACCTTACCACCCCAACTGAGACCACAGACTCGGGCCCCATCGTCGTGGATGATGCATCCGATGACGGATCTTATTCGTCAATGCCTCCACTAGAGGGGGAGCCCGGTGACCCGGACTTGACATCAGACTCTTGGTCCACTGTTAGCGGATCGGAGGACGTCGTGTGCTGCTCAATGTCATATTCATGGACTGGGGCGCTTGTAACACCTTGCGCGGCTGAAGAATCAAAGCTGCCAATTAGCCCCCTGAGCAATTCACTTTTGCGCCATCACAATATGGTGTATGCCACGACCACCCGTTCTGCTGTGACACGGCAGAAGAAGGTGACCTTCGACCGCCTGCAGGTGGTGGACAGTCACTACAATGAAGTGCTTAAGGAGATAAAGGCACGAGCATCCAGAGTGAAGGCACGCTTGCTTACCACAGAGGAAGCTTGCGACCTGACGCCCCCCCACTCAGCCAGATCAAAGTTCGGCTACGGGGCGAAGGATGTTCGGAGCCATTCCCGCAAGGCCATTAACCACATCAGCTCCGTGTGGAAGGACTTGCTGGACGACAACAATACCCCAATACCAACAACAATCATGGCCAAAAATGAGGTCTTCGCTGTGAACCCAGCGAAGGGAGGTCGGAAGCCTGCTCGCCTGATCGTGTATCCGGATCTCGGGGTCCGGGTTTGCGAGAAGAGAGCGCTTCACGACGTCATCAAAAAACTGCCTGAGGCCGTGATGGGAGCCGCTTATGGCTTCCAATACTCCCCAGCGCAGCGGGTGGAATTTCTTCTGACTGCTTGGAAGTCGAAGAAGACCCCAATGGGGTTCTCTTATGATACCCGCTGCTTTGACTCCACTGTAACCGAAAAGGACATCAGGGTCGAGGAAGAGGTCTATCAGTGTTGTGACCTGGAGCCCGAAGCCCGCAAAGTCATCACCGCCCTCACAGATAGACTCTATGTGGGCGGCCCTATGCACAACAGCAAGGGAGACCTTTGTGGGTATCGGAGATGTCGCGCAAGCGGCGTCTACACCACCAGCTTCGGGAACACGCTGACGTGCTATCTCAAAGCCACGGCCGCCATCAGGGCGGCGGGGCTGAGAGACTGCACTATGTTGGTTTGCGGTGATGACTTAGTCGTCATCGCTGAGAGCGACGGCGTAGAGGAGGACAACCGAGCCCTCCGAGCCTTCACGGAGGCTATGACGAGATACTCGGCTCCCCCAGGTGACGCCCCGCAGCCAGCATATGACCTGGAACTAATAACATCATGTTCATCCAACGTCTCAGTCGCGCACGACGTGACGGGTAAAAAGGTATATTACCTAACCCGAGACCCTGAAACTCCCTTGGCGCGAGCCGCATGGGAGACAGTCCGACACACTCCAGTCAATTCCTGGTTGGGAAACATCATAGTCTACGCTCCCACAATATGGGTGCGCATGATATTGATGACCCACTTTTTCTCAATACTCCAGAGCCAGGAAGCCCTTGAGAAAGCACTCGACTTCGATATGTACGGAGTCACCTACTCTATCACTCCGCTGGATTTACCGGCAATCATTCAAAGACTCCATGGCTTAAGCGCGTTCACGCTGCACGGATACTCTCCACACGAACTCAACCGGGTGGCCGGAGCCCTCAGAAAACTTGGGGTACCCCCGCTGAGAGCGTGGAGACATCGGGCCCGAGCAGTCCGCGCTAAGCTTATCGCCCAGGGAGGTAGAGCCAAAATATGTGGCATATACCTCTTTAACTGGGCGGTAAAAACCAAACTCAAACTCACTCCATTGCCTGCCGCTGCCAAACTCGATTTATCGGGTTGGTTTACGGTAGGCGCCGGCGGGGGAGACATTTATCACAGCATGTCTCATGCCCGACCCCGCTATTTACTCCTGTGCCTACTCCTACTTACAGTAGGGGTAGGCATCTTCCTGCTGCCTGCTCGGTAGGCAGCTTAACACTCCGACC", IUPAC.unambiguous_dna)

my_seq3 = Seq('TGATACAGACCTTACCACCCCAACTGAGACCACAGACTCGGGCCCCATCGTCGTGGATGATGCATCCGATGACGGATCTTATTCGTCAATGCCTCCACTAGAGGGGGAGCCCGGTGACCCGGACTTGACATCAGACTCTTGGTCCACTGTTAGCGGATCGGAGGACGTCGTGTGCTGC', IUPAC.unambiguous_dna)

mutable_seq = MutableSeq("TGATACAGACCTTACCACCCCAACTGAGACCACAGACTCGGGCCCCATCGTCGTGGATGATGCATCCGATGACGGATCTTATTCGTCAATGCCTCCACTAGAGGGGGAGCCCGGTGACCCGGACTTGACATCAGACTCTTGGTCCACTGTTAGCGGATCGGAGGACGTCGTGTGCTGCTCAATGTCATATTCATGGACTGGGGCGCTTGTAACACCTTGCGCGGCTGAAGAATCAAAGCTGCCAATTAGCCCCCTGAGCAATTCACTTTTGCGCCATCACAATATGGTGTATGCCACGACCACCCGTTCTGCTGTGACACGGCAGAAGAAGGTGACCTTCGACCGCCTGCAGGTGGTGGACAGTCACTACAATGAAGTGCTTAAGGAGATAAAGGCACGAGCATCCAGAGTGAAGGCACGCTTGCTTACCACAGAGGAAGCTTGCGACCTGACGCCCCCCCACTCAGCCAGATCAAAGTTCGGCTACGGGGCGAAGGATGTTCGGAGCCATTCCCGCAAGGCCATTAACCACATCAGCTCCGTGTGGAAGGACTTGCTGGACGACAACAATACCCCAATACCAACAACAATCATGGCCAAAAATGAGGTCTTCGCTGTGAACCCAGCGAAGGGAGGTCGGAAGCCTGCTCGCCTGATCGTGTATCCGGATCTCGGGGTCCGGGTTTGCGAGAAGAGAGCGCTTCACGACGTCATCAAAAAACTGCCTGAGGCCGTGATGGGAGCCGCTTATGGCTTCCAATACTCCCCAGCGCAGCGGGTGGAATTTCTTCTGACTGCTTGGAAGTCGAAGAAGACCCCAATGGGGTTCTCTTATGATACCCGCTGCTTTGACTCCACTGTAACCGAAAAGGACATCAGGGTCGAGGAAGAGGTCTATCAGTGTTGTGACCTGGAGCCCGAAGCCCGCAAAGTCATCACCGCCCTCACAGATAGACTCTATGTGGGCGGCCCTATGCACAACAGCAAGGGAGACCTTTGTGGGTATCGGAGATGTCGCGCAAGCGGCGTCTACACCACCAGCTTCGGGAACACGCTGACGTGCTATCTCAAAGCCACGGCCGCCATCAGGGCGGCGGGGCTGAGAGACTGCACTATGTTGGTTTGCGGTGATGACTTAGTCGTCATCGCTGAGAGCGACGGCGTAGAGGAGGACAACCGAGCCCTCCGAGCCTTCACGGAGGCTATGACGAGATACTCGGCTCCCCCAGGTGACGCCCCGCAGCCAGCATATGACCTGGAACTAATAACATCATGTTCATCCAACGTCTCAGTCGCGCACGACGTGACGGGTAAAAAGGTATATTACCTAACCCGAGACCCTGAAACTCCCTTGGCGCGAGCCGCATGGGAGACAGTCCGACACACTCCAGTCAATTCCTGGTTGGGAAACATCATAGTCTACGCTCCCACAATATGGGTGCGCATGATATTGATGACCCACTTTTTCTCAATACTCCAGAGCCAGGAAGCCCTTGAGAAAGCACTCGACTTCGATATGTACGGAGTCACCTACTCTATCACTCCGCTGGATTTACCGGCAATCATTCAAAGACTCCATGGCTTAAGCGCGTTCACGCTGCACGGATACTCTCCACACGAACTCAACCGGGTGGCCGGAGCCCTCAGAAAACTTGGGGTACCCCCGCTGAGAGCGTGGAGACATCGGGCCCGAGCAGTCCGCGCTAAGCTTATCGCCCAGGGAGGTAGAGCCAAAATATGTGGCATATACCTCTTTAACTGGGCGGTAAAAACCAAACTCAAACTCACTCCATTGCCTGCCGCTGCCAAACTCGATTTATCGGGTTGGTTTACGGTAGGCGCCGGCGGGGGAGACATTTATCACAGCATGTCTCATGCCCGACCCCGCTATTTACTCCTGTGCCTACTCCTACTTACAGTAGGGGTAGGCATCTTCCTGCTGCCTGCTCGGTAGGCAGCTTAACACTCCGACC", IUPAC.unambiguous_dna)

ableng = 378
mutable_seq[ableng] = 'C'

print ableng-len(my_seq3)

if not ableng < len(my_seq3):
   if (ableng-len(my_seq3))%3 == 0:
       print (my_seq2[ableng:ableng+3])
       print (mutable_seq[ableng:ableng+3])
       print translate(my_seq2[ableng:ableng+3])
       print translate(mutable_seq[ableng:ableng+3])
       print (ableng-len(my_seq3))/3


   elif (ableng-len(my_seq3))%3 == 1:
       print (my_seq2[ableng-1:ableng+2])
       print (mutable_seq[ableng-1:ableng+2])
       print translate(my_seq2[ableng-1:ableng+2])
       print translate(mutable_seq[ableng-1:ableng+2])
       print (ableng-len(my_seq3))/3 + 1

   elif (ableng-len(my_seq3))%3 == 2:
       print my_seq2[ableng-2:ableng+1]
       print (mutable_seq[ableng-2:ableng+1])
       print translate(my_seq2[ableng-2:ableng+1])
       print translate(mutable_seq[ableng-2:ableng+1])
       print (ableng-len(my_seq3))/3 +1
else:
    print 'Vector'

