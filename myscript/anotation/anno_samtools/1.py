__author__ = 'wanguan2000'
import re

sample_size = 9

allresulr = []
with open('gene.txt', 'ru') as f:

    for line in f:
        result = []
        gene = line.rstrip()
        result.extend([gene] + sample_size * [''])
        with open('post.txt', 'rU') as p:
            for posi in p:
                posi = posi.rstrip()
                if not posi:
                    break
                if not posi.startswith('#'):
                    mutation = posi.split('\t')
                    posigene = mutation[7]
                    re.sub('(,|;).*$', '', posigene)
                    if posigene == gene:
                        #print posigene
                        Exon = mutation[9]
                        m = re.search('(p.*?),', Exon)
                        if m:
                            m.group(1)

                            for n in range(19, 19 + sample_size):
                                if mutation[n] == '0':
                                    pass
                                elif mutation[n] == '1':
                                    result[n - 18] = result[n - 18] + ' ' + m.group(1)
            print '\t'.join(result)


