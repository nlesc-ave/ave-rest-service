from subprocess import check_call, CalledProcessError, DEVNULL

from click import ClickException
from cyvcf2 import VCF


def validate_data(file_abs_path, datatype):
    """Validate datafile.
    Validation method depends on the datatype
    """
    if datatype == '2bit':
        is_valid_2bit(file_abs_path)
    elif datatype in ('genes', 'features'):
        is_valid_bigbed(file_abs_path)
    elif datatype == 'variants':
        is_valid_bcf(file_abs_path)


def is_valid_2bit(url):
    """Check if provided 2bit url is in proper format"""
    args = (
        'twoBitInfo',
        url,
        'stdout'
    )
    try:
        check_call(args, stdout=DEVNULL)
    except CalledProcessError:
        raise ClickException('2bit url could not be opened')


def is_valid_bcf(bcf_file):
    """Check if provided bcf file is in proper format"""

    try:
        VCF(bcf_file)
    except OSError:
        raise ClickException("Error while opening bcf file with cyvcf2")


def is_valid_bigbed(url):
    """Check if provided bigbed url is in proper format"""
    args = (
        'bigBedInfo',
        url
    )
    try:
        check_call(args, stdout=DEVNULL)
    except CalledProcessError:
        raise ClickException("Error opening bigbed url")
