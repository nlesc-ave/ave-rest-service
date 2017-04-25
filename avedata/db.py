import os
import click
from pyfaidx import Fasta
from pysam import TabixFile, asGTF
from cyvcf2 import VCF


def dict_from_attributes(attributes_string):
    """Convert a string with attributes to a dictionary"""
    attributes_dict = {}
    key_value_list = attributes_string.split(";")
    for key_value in key_value_list:
        key, value = key_value.split("=")
        attributes_dict[key] = value
    return attributes_dict


def validate_data(file_abs_path, datatype):
    """Validate datafile.
    Validation method depends on the datatype
    """

    if datatype == "sequence":
        is_valid_fasta(file_abs_path)
    elif datatype == "features":
        is_valid_gff(file_abs_path)
    elif datatype == "variants":
        is_valid_bcf(file_abs_path)


def is_valid_fasta(fasta_file):
    """Check if provided fasta file is in propper format"""

    # check if it is

    # try to open file with `pyfaidx`
    # check if there is an idex file
    index_file = os.path.join(fasta_file, '.fai')
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


def is_valid_gff(gff_file):
    """Check if provided gff file is in proper format"""

    try:
        gff = TabixFile(gff_file, parser=asGTF())
    except OSError as err:
        message = """Error while parsing gff file.\n
        Please ensure it is valid gff file, sorted, compressed with bgzip
        and indexed with tabix.
        """
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


def import_gff(db, meta_id, filename):
    """Import features from gff file into the sqlite database
    features table."""

    gff = TabixFile(filename, parser=asGTF())
    for feature in gff.fetch():
        if feature.feature == 'gene':
            # fetch attributes
            attributes = dict_from_attributes(feature.attributes)
            name = attributes['Name']
            chromosome = feature.contig
            start = feature.start
            end = feature.end

            # create a database query
            query = """INSERT INTO features (meta_id, name, chromosome, start, end)
                       VALUES (?,?,?,?,?)"""
            db.cursor().execute(query, (meta_id, name, chromosome, start, end))
            # commit database updates
            db.commit()
