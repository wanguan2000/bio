import urllib2, urllib
import re
import time


def araexpress(gene):
    data = {'dataSource' : 'Developmental_Map', 'modeInput' : 'Absolute', 'primaryGene' : gene}
    f = urllib2.urlopen(
            url     = 'http://bar.utoronto.ca/efp/cgi-bin/efpWeb.cgi',
            data    = urllib.urlencode(data)
    		)
    #print f.read()
    for a in f.readlines():
        if a.startswith(r"loadPopup('table1'"):
            #print a
            web='http://bar.utoronto.ca/efp/cgi-bin/'
            table = web + re.compile('''<a href="(.*?)">here''').findall(a)[0]
            #print table
            f = urllib2.urlopen(table)
            print '>>'+gene
            print f.read()
            print "!!"

    
with open('gene.txt', 'rU') as f:
     for line in f:
         line = line.rstrip()
         if not line:
             break
         araexpress(line)
         time.sleep(4)






