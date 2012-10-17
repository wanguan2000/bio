__author__ = 'wanguan2000'
f = open('SymbolAnntation.html','rU')
SymbolAnnotation = {}
try:
    while True:
        line = f.readline().rstrip()
        if not line:
            break
        classSymbol = line
        aafSymbol = "<td class=\"aafSymbol\">"
        if aafSymbol in line:
            line = line.replace(aafSymbol,'').replace('</td>','')
            SymbolAnnotation[line] = '<tr>\n'+classSymbol+'\n'+f.readline()+f.readline()+f.readline()+f.readline()+f.readline()+f.readline()+f.readline()+'</tr>\n'

finally:
    f.close


g = open('cha.txt','rU')

print('<html> \n\
<head> \n\
<title> \n\
Symbol Annotation \n\
</title> \n\
<meta http-equiv="Content-Style-Type" content="text/css"> \n\
<style type="text/css"> \n\
td.aafPubMed { text-align: center } \n\
p.aafGOItem { margin-top: 1px; margin-bottom: 1px; padding-left: 10px; text-indent: -10px } \n\
p.aafPathwayItem { margin-top: 1px; margin-bottom: 1px; padding-left: 10px; text-indent: -10px } \n\
</style> \n\
<script language="JavaScript"> \n\
</script> \n\
</head> \n\
<body bgcolor="#FFFFFF"> \n\
<h1 align="center"> \n\
Symbol Annotation Listing \n\
</h1> \n\
<table border="2"> \n\
<tr> \n\
<th>Symbol</th> \n\
<th>Description</th> \n\
<th>GenBank</th> \n\
<th>Gene</th> \n\
<th>UniGene</th> \n\
<th>PubMed</th> \n\
<th>Gene Ontology</th> \n\
<th>Pathway</th> \n\
</tr>')

try:
    while True:
        line = g.readline().rstrip()
        if not line:
            break
        if line in SymbolAnnotation:
            pass
            print(SymbolAnnotation.get(line))
        else:
            print('<tr>')
            print('<td class="aafSymbol">'+line+'</td>')
            print('<td class="aafDescription">&nbsp;</td>\n<td class="aafGenBank">&nbsp;</td>\n<td class="aafLocusLink">&nbsp;</td>\n<td class="aafUniGene">&nbsp;</td>\n<td class="aafPubMed">&nbsp;</td>\n<td class="aafGO">&nbsp;</td>\n<td class="aafPathway">&nbsp;</td>')
            print('</tr>')
finally:
    f.close
print('</table>\n</body>\n</html>')


'''
<tr>
<td class="aafSymbol">PNOC</td>
<td class="aafDescription">prepronociceptin</td>
<td class="aafGenBank"><a href="http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&db=nucleotide&term=NM_006228%5BACCN%5D&doptcmdl=GenBank">NM_006228</a></td>
<td class="aafLocusLink"><a href="http://www.ncbi.nlm.nih.gov/sites/entrez?Db=gene&Cmd=DetailsSearch&Term=5368">5368</a></td>
<td class="aafUniGene"><a href="http://www.ncbi.nlm.nih.gov/UniGene/clust.cgi?ORG=Hs&CID=88218">Hs.88218</a></td>
<td class="aafPubMed"><a href="http://www.ncbi.nih.gov/entrez/query.fcgi?tool=bioconductor&cmd=Retrieve&db=PubMed&list_uids=8710928%2c8710930%2c9168905%2c9521323%2c10101606%2c10419552%2c10692489%2c11097863%2c11214319%2c11331401%2c11436130%2c11501941%2c12477932%2c12812047%2c12950177%2c15489334%2c16043263%2c16344560%2c17910740%2c18240029%2c18292431%2c18577758%2c19058789%2c19501074%2c19560501%2c19573600%2c19874574%2c20100531%2c20379614%2c20888736">30</a></td>
<td class="aafGO"><p class="aafGOItem"><a href="http://amigo.geneontology.org/cgi-bin/amigo/go.cgi?view=details&query=GO:0001515" title="Molecular Function (IEA)">opioid peptide activity</a></p> <p class="aafGOItem"><a href="http://amigo.geneontology.org/cgi-bin/amigo/go.cgi?view=details&query=GO:0005184" title="Molecular Function (TAS)">neuropeptide hormone activity</a></p> <p class="aafGOItem"><a href="http://amigo.geneontology.org/cgi-bin/amigo/go.cgi?view=details&query=GO:0005576" title="Cellular Component (EXP)">extracellular region</a></p> <p class="aafGOItem"><a href="http://amigo.geneontology.org/cgi-bin/amigo/go.cgi?view=details&query=GO:0005576" title="Cellular Component (TAS)">extracellular region</a></p> <p class="aafGOItem"><a href="http://amigo.geneontology.org/cgi-bin/amigo/go.cgi?view=details&query=GO:0007165" title="Biological Process (TAS)">signal transduction</a></p> <p class="aafGOItem"><a href="http://amigo.geneontology.org/cgi-bin/amigo/go.cgi?view=details&query=GO:0007218" title="Biological Process (IEA)">neuropeptide signaling pathway</a></p> <p class="aafGOItem"><a href="http://amigo.geneontology.org/cgi-bin/amigo/go.cgi?view=details&query=GO:0007268" title="Biological Process (IEA)">synaptic transmission</a></p> <p class="aafGOItem"><a href="http://amigo.geneontology.org/cgi-bin/amigo/go.cgi?view=details&query=GO:0007600" title="Biological Process (TAS)">sensory perception</a></p></td>
<td class="aafPathway">&nbsp;</td>
</tr>
'''
