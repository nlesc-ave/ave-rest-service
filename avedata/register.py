import os
import click
from pyfaidx import Fasta
from cyvcf2 import VCF


def validate_data(file_abs_path, datatype):
    """Validate datafile.
    Validation method depends on the datatype
    """
    if datatype == "sequence":
        is_valid_fasta(file_abs_path)
    elif datatype == "variants":
        is_valid_bcf(file_abs_path)
    # TODO add validate for genes/features bigbed urls


def is_valid_fasta(fasta_file):
    """Check if provided fasta file is in propper format"""

    # check if it is

    # try to open file with `pyfaidx`
    # check if there is an idex file
    index_file = ".".join([fasta_file, 'fai'])
    if not os.path.isfile(index_file):
        message = "Fasta index not found. The index will be created"
        click.echo(click.style(message, fg='green'))

    try:
        fasta = Fasta(fasta_file)
        print(fasta)
    except UnicodeDecodeError as err:
        message = """Error while accessing fasta file.\n
        Please ensure it is a valid fasta file."""
        click.echo(click.style(message, fg='red'))
        click.echo(err)


def is_valid_bcf(vcf_file):
    """Check if provided bcf file is in proper format"""

    try:
        vcf = VCF(vcf_file)
    except OSError as error:
        message = "Error while parsing bcf file with cyvcf2"
        click.echo(click.style(message, fg='red'))
        click.echo(error)

