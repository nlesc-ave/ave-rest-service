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
bgzip -i TAIR10_GFF3_genes.sorted.gff 
tabix -p gff TAIR10_GFF3_genes.sorted.gff.gz
```

Service queries annotation with use of `pysam.Tabixfile`.
```py
gff.fetch("Chr2", 1, 5000, parser=pysam.asGTF())
```
Learn more about pysam.Tabixfile from
[pysam docs](https://pysam.readthedocs.io/en/latest/index.html)

### SNPs
SNPs need to be provided in single file in [VCF](https://samtools.github.io/hts-specs/VCFv4.3.pdf)
They also need to be preprocessed in following way.

#### Sort by chromosome with [VCFtools](http://vcftools.sourceforge.net/perl_module.html)
```sh
vcf-sort -c variants.vcf > variants.sorted.vcf
```

#### Compress by [bgzip](http://www.htslib.org/doc/tabix.html) and index with [tabix](http://www.htslib.org/doc/tabix.html)
```sh
bgzip -c variants.sorted.vcf
tabix -p vcf variants.sorted.vcf.gz
```

### Convert to [BCF](https://samtools.github.io/hts-specs/BCFv2_qref.pdf) with [bcftools](https://samtools.github.io/bcftools/bcftools.html)
```sh
bcftools view -O b variants.sorted.vcf.gz > variants.sorted.bcf
```

### Index with [bcftools](https://samtools.github.io/bcftools/bcftools.html)
```sh
bcftools index variants.sorted.bcf
```

## REST API
[swagger UI](http://petstore.swagger.io/?url=https://raw.githubusercontent.com/nlesc-ave/ave-rest-service/master/swagger.yml)

## importing data with command line interface



```sh
# add database location
flask initdb './db/sqlite'

flask import -species 'Solanum Lycopersicum' \
             -genome SL.2.40 \
             -type sequence
             -file ./db/tomato/reference/S_lycopersicum_chromosomes.2.40.fa
```
