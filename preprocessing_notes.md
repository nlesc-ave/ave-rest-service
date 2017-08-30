# Data Processing

## preprocessing
generate compressed bcf file from vcf file:
```
bcftools view -O b 1001genomes_snp-short-indel_with_tair10_only_ACGTN.vcf.gz > 1001genomes_snp-short-indel_with_tair10_only_ACGTN.bcf

gunzip: ./ERZ020502/RF_060_SZAXPI009336-14.vcf.gz: unexpected end of file
gunzip: ./ERZ020502/RF_060_SZAXPI009336-14.vcf.gz: uncompress failed
gunzip: ./ERZ020503/RF_062_SZAXPI009337-15.vcf.gz: unexpected end of file
gunzip: ./ERZ020503/RF_062_SZAXPI009337-15.vcf.gz: uncompress failed
```

~~concatenating vcf files:
`vcf-concat myvcfs/*.vcf.gz | gzip > out.vcf.gz`~~

files come from sra here:
ftp.sra.ebi.ac.uk
and the directory _vol1_
directories: ERZ020447 - ERZ020530


* ungzip vcf files
* each file compress with bgzip
`bgzip sample.vcf`
* index with tabix
`tabix -p vcf sample.vcf.gzip`
* merge into one variant file
`vcf-merge *.vcf.gz > all-snps.vcf`


## random access to fasta sequence
use pyfaidx
[GitHub - mdshw5/pyfaidx: Efficient pythonic random access to fasta subsequences](https://github.com/mdshw5/pyfaidx)
```py
from pyfaidx import Fasta
genome = Fasta('TAIR10.ga')

```

## random access to gff (gene annotatins)
* first need to sort the gff file by chrom/start
```sh
# doing it with bedtools
bedtools sort -i TAIR10_GFF3_genes.gff > TAIR10_GFF3_genes.sorted.gff
```

* then index with tabix
```sh
bgzip TAIR10_GFF3_genes.sorted.gff 
tabix -p gff TAIR10_GFF3_genes.sorted.gff.gz
```

* use `pysam.Tabixfile` to read the file, then iterate over it
```py
gff.fetch("Chr2", 1, 5000, parser=pysam.asGTF())
```

## random access to vcf
* fetch vcf or vcf.gz file
* sort by chromosome
```sh
 vcf-sort -t /mnt/disks/variant-store/tmp/ -c 1001genomes_snp-short-indel_with_tair10_only_ACGTN.vcf.gz > variants_sorted.vcf
```
* block gzip
```sh
bgzip -c variants_sorted.vcf variants_sorted.vcf.gz
```
* index with tabix
```sh
tabix -p vcf variants_sorted.vcf.gz
```
* convert vcf to bcf
```sh
bcftools view -O b variants_sorted.vcf.gz > variants_sorted.bcf
```

## queries
1. region of 50 kB 
	* reference sequence
	* all variants
	* all annotations
2. find the gene of interest
there is no good way to do it based on gff file
one solution is to put genes names and their location in the sqlite db (will it be fast enough?)

