# ave-rest-service
Serving variant, annotation and genome data for AVE visualisation.

## Data preprocessing.
Before data can be served it has to be preprocessed in following way.

### Genome sequence
Genome sequence in [FASTA](https://en.wikipedia.org/wiki/FASTA_format) format is used. It is idexed and accessed by
[pyfaidx](https://github.com/mdshw5/pyfaidx). All chromosome
sequences should be in single FASTA file with `.fa` extension.
`SeqID`'s shoould match once in coresponding gff and bcf files.

### Genomic features annotations
Information about annotations should be in [gff3](https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md)
format. You can validate gff files on [genome tools website](http://genometools.org/cgi-bin/gff3validator.cgi).

#### Sort features with [bedtools](https://bedtools.readthedocs.io/en/latest/)
```sh
bedtools sort -i TAIR10_genes.gff > TAIR10_genes.sorted.gff
```

#### Compress by [bgzip](http://www.htslib.org/doc/tabix.html) and index with [tabix](http://www.htslib.org/doc/tabix.html)
```sh
bgzip TAIR10_GFF3_genes.sorted.gff 
tabix -p gff TAIR10_GFF3_genes.sorted.gff.gz
```

Service queries annotation with use of `pysam.Tabixfile`.
```py
gff.fetch("Chr2", 1, 5000, parser=pysam.asGTF())
```
Learn more about pysam.Tabixfile from
[pysam docs](https://pysam.readthedocs.io/en/latest/index.html)
