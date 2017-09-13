# ave-rest-service

[![Build Status](https://travis-ci.org/nlesc-ave/ave-rest-service.svg?branch=master)](https://travis-ci.org/nlesc-ave/ave-rest-service)
[![SonarCloud Gate](https://sonarcloud.io/api/badges/gate?key=ave-rest-service)](https://sonarcloud.io/dashboard?id=ave-rest-service)
[![SonarCloud Coverage](https://sonarcloud.io/api/badges/measure?key=ave-rest-service&metric=coverage)](https://sonarcloud.io/component_measures/domain/Coverage?id=ave-rest-service)
[![Docker Automated buil](https://img.shields.io/docker/automated/ave2/allelic-variation-explorer.svg)](https://hub.docker.com/r/ave2/allelic-variation-explorer/)

Serving variant, annotation and genome data for AVE visualisation.

## REST API
[swagger UI](http://petstore.swagger.io/?url=https://raw.githubusercontent.com/nlesc-ave/ave-rest-service/master/avedata/swagger.yml)

## INSTALL

Ave requires a [Anaconda3](https://www.continuum.io/downloads) or [miniconda3](https://conda.io/miniconda.html) installation.

To create a new Anaconda environment with all the ave dependencies installed.
```bash
conda env create -f environment.yml
```
On osx use `enviroment.osx.yml` instead of `environment.yml`.

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

## Configure

The directory in which `avadata` is run should contain a `settings.cfg` configuration file.

The repo contains an example config file called `settings.example.cfg`.

Make sure the `WHOOSH_BASE_DIR` directory exists.

## Data pre processing

Before data can be served it has to be preprocessed in following way.

### Genome sequence

Genome sequence in [2bit](https://genome.ucsc.edu/goldenpath/help/twoBit.html) format is used.

When you have a genome sequence in [FASTA](https://en.wikipedia.org/wiki/FASTA_format) format, where each chromosome is a sequence in the file.

The FASTA file can be converted to 2bit using:

```sh
faToTwoBit genome.fa genome.2bit
```

The (chromosome) sequence identifiers should match the ones in corresponding gff and bcf files.

### Genomic features annotations

Gene annotations (transcripts) are treated differently than other feature annotations. It has
to do with the fact that transcripts are displayed in separated track where
UTRs, CDSs, exons and introns are rendered differently within one track.

Gene or feature annotations must be provided as [bigBed](http://genome.ucsc.edu/goldenPath/help/bigBed.html) files.

Some gene bed files can be downloaded from http://bioviz.org/quickload/
To convert a gene bed file to bigbed use:
```bash
# Fetch chrom sizes
twoBitInfo genome.2bit chrom.sizes
# the version for mac os is available also available http://hgdownload.cse.ucsc.edu/admin/exe/macOSX.x86_64/bedToBigBed
chmod +x bedToBigBed
# description field is too long for bedToBigBed so it must be trimmed
gunzip -c S_lycopersicum_May_2012.bed.gz | perl -n -e 'chomp;@F=split(/\t/);$F[13] = substr($F[13],0,255); print join("\t", @F),"\n";'  > S_lycopersicum_May_2012.bed.trimmed
bedToBigBed -tab -type=bed12+2 S_lycopersicum_May_2012.bed.trimmed genome.txt S_lycopersicum_May_2012.bb
```

To convert a gff feature file to bigbed use:

```bash
# Download a gff file
wget ftp://ftp.solgenomics.net/tomato_genome/microarrays_mapping/A-AFFY-87_AffyGeneChipTomatoGenome.probes_ITAG2.3genome_mapping.gff
# Sort gff
bedtools sort -i A-AFFY-87_AffyGeneChipTomatoGenome.probes_ITAG2.3genome_mapping.gff > A-AFFY-87_AffyGeneChipTomatoGenome.probes_ITAG2.3genome_mapping.sorted.gff
# Convert gff to bed
gff2bed < A-AFFY-87_AffyGeneChipTomatoGenome.probes_ITAG2.3genome_mapping.sorted.gff > A-AFFY-87_AffyGeneChipTomatoGenome.probes_ITAG2.3genome_mapping.bed
# Fetch chrom sizes
twoBitInfo genome.2bit chrom.sizes
# Convert bed to bigbed
bedToBigBed -tab -type=bed6+4 -as=gff3.as A-AFFY-87_AffyGeneChipTomatoGenome.probes_ITAG2.3genome_mapping.bed chrom.sizes A-AFFY-87_AffyGeneChipTomatoGenome.probes_ITAG2.3genome_mapping.bb
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

## Register data

Register data with command line interface

```sh
# initialise the database
avedata register --species 'Solanum Lycopersicum' \
                 --genome SL.2.40 \
                 --datatype 2bit \
                 http://<dataserver>/S_lycopersicum_chromosomes.2.40.fa.2bit

avedata register --species 'Solanum Lycopersicum' \
                 --genome SL.2.40 \
                 --datatype variants \
                 ./db/tomato/tomato_snps.bcf

avedata register --species 'Solanum Lycopersicum' \
                 --genome SL.2.40 \
                 --datatype genes \
                 http://<dataserver>/gene_models.bb

avedata register --species 'Solanum Lycopersicum' \
                 --genome SL.2.40 \
                 --datatype features \
                 http://<dataserver>/A-AFFY-87.bb
# `A-AFFY-87` will be used as track label
```

## Run service

```bash
avadata run
```
It will print the `<url>` it is hosting at.

The api endpoint is at `<url>/api/`.
The Swagger UI is at `<url>/api/ui`.

The above command will run a single threaded low performance web server.

Use [gunicorn](http://gunicorn.org/) to run in production with
```bash
gunicorn -w 4 --threads 2 -t 60 avedata.avedata:app
```

## Deploy using Docker

A Docker image is available on [Docker Hub](https://hub.docker.com/r/ave2/allelic-variation-explorer/).

The Docker image contains the [ave-app](https://github.com/nlesc-ave/ave-app) as the web-based user interface.

The Docker image contains no data it must be supplied using volumes. It expects the following volumes:

* /data, location for 2bit, bcf and bigbed files. Hosted as http://&lt;aveserver&gt;/data
* /whoosh, full text indices for genes and features
* /meta, directory in which ave meta database is stored

### Run service

```bash
mkdir data
mkdir whoosh
mkdir meta
docker run -d \
  -v $PWD/data:/data -v $PWD/whoosh:/whoosh -v $PWD/meta:/meta \
  -e EXTERNAL_URL=http://$(hostname) -p 80:80 \
  --name ave ave2/allelic-variation-explorer
```

Command above will run web server on port 80 of host machine.

To make Swagger UI api calls the EXTERNAL_URL environment variable is needed,
because the Python web service is behind NGINX reverse proxy, causing the url where the api is available on to change,
the EXTERNAL_URL allows Swagger UI to use the externally available api endpoint.

### Register data

Example commands using files for tomato in `data/tomato/SL.2.40` directory, namely:
* genome.2bit
* tomato_snps.bcf
* gene_models.bb
* A-AFFY-87.bb

```bash
docker exec ave \
    avedata register \
    --species 'Solanum Lycopersicum' \
    --genome SL.2.40 \
    --datatype 2bit \
    http://<aveserver>/data/tomato/SL.2.40/genome.2bit

docker exec ave \
    avedata register \
    --species 'Solanum Lycopersicum' \
    --genome SL.2.40 \
    --datatype variants \
    /data/tomato/SL.2.40/tomato_snps.bcf

docker exec ave \
    avedata register \
    --species 'Solanum Lycopersicum' \
    --genome SL.2.40 \
    --datatype genes \
    http://<aveserver>/data/tomato/SL.2.40/gene_models.bb

docker exec ave \
    avedata register \
    --species 'Solanum Lycopersicum' \
    --genome SL.2.40 \
    --datatype features \
    http://<aveserver>/data/tomato/SL.2.40/A-AFFY-87.bb
# `A-AFFY-87` will be used as track label
```
