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

Gene annotations (transcripts) are treated differently than other feature annotations. It has
to do with the fact that transcripts are displayed in separated track where
UTRs, CDSs, exons and introns are rendered differently within one track.
Gene annotations can be provided as bigBed files or gff3 files.

#### gff3 annotations
Information about annotations should be in [gff3](https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md)
format. You can validate gff files on [genome tools website](http://genometools.org/cgi-bin/gff3validator.cgi).

##### Sort features with [bedtools](https://bedtools.readthedocs.io/en/latest/)
```sh
bedtools sort -i TAIR10_genes.gff > TAIR10_genes.sorted.gff
```

##### Compress by [bgzip](http://www.htslib.org/doc/tabix.html) and index with [tabix](http://www.htslib.org/doc/tabix.html)
```sh
bgzip -i TAIR10_GFF3_genes.sorted.gff
tabix -p gff TAIR10_GFF3_genes.sorted.gff.gz
```

Service queries annotation with use of
[pysam.Tabixfile](https://pysam.readthedocs.io/en/latest/api.html#pysam.TabixFile).
```py
import pysam
from pysam import TabixFile
gff = TabixFile("gene_models.gff.gz", parser=pysam.asGTF())
for feature in gff.fetch("SL2.40ch06", 1, 5000):
    print(f.start)
```
Learn more about pysam.Tabixfile from
[pysam docs](https://pysam.readthedocs.io/en/latest/index.html)

#### bigBed annotations
Gene annotations are directly served from bigBed files (`*.bb`). To enable
serching by gene names or other annotations, those are also indexed and stored
in sqlite database. Indexing is done in python with use of `pybedtools`. To be
able to read `bigBed` files `bigBedToBed` tool available in the path and
executable is necessary. The tool can be dowloaded from
[USCS download page](http://hgdownload.cse.ucsc.edu/admin/exe/).

```py
import pybedtools
bed = pybedtools.contrib.bigbed.bigbed_to_bed("S_lycopersicum_May_2012.bb")
```

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

## INSTALL

Ave requires a [Anaconda3](https://www.continuum.io/downloads) or [miniconda3](https://conda.io/miniconda.html) installation.

To create a new Anaconda environment with all the ave dependencies installed.
```bash
conda env create -f environment.yml
```
For osx use `enviroment.osx.yml` instead of `environment.yml`.

Activate the environment
```bash
source activate ave2
```

Install ave for production with
```bash
python setup.py install
```

Install ave for development with
```bash
python setup.py develop
```

If dependencies are changed in `environment.yml` then update conda env by runnning
```
conda env update -f environment.yml
```

## importing data with command line interface

```sh
# initialise the database
avedata register --species 'Solanum Lycopersicum' \
                 --genome SL.2.40 \
                 --datatype sequence \
                 ./db/tomato/reference/S_lycopersicum_chromosomes.2.40.fa

avedata register --species 'Solanum Lycopersicum' \
                 --genome SL.2.40 \
                 --datatype features \
                 ./db/tomato/gene_models.gff.gz

avedata register --species 'Solanum Lycopersicum' \
                 --genome SL.2.40 \
                 --datatype variants \
                 ./db/tomato/tomato_snps.bcf

avedata register --species 'Solanum Lycopersicum' \
                 --genome SL.2.40 \
                 --datatype 2bit \
                 http://<dataserver>.S_lycopersicum_chromosomes.2.40.fa.2bit

avedata register --species 'Solanum Lycopersicum' \
                 --genome SL.2.40 \
                 --datatype bigbed \
                 http://<dataserver>.gene_models.bb
```
