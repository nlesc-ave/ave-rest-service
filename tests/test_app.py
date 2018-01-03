import pytest
import simplejson

from avedata.app import app
from avedata.db import init_db
from avedata.commands import register_file
from avedata.api import genomes, species


def setup_database():
    init_db()
    register_file(species='Solanum Lycopersicum',
                  genome='SL.2.40',
                  datatype='2bit',
                  filename='tests/data/S_lycopersicum_chromosomes.2.40.chr6-0-100000.2bit')
    register_file(species='Solanum Lycopersicum',
                  genome='SL.2.40',
                  datatype='variants',
                  filename='tests/data/tomato_snps.chr6-0-100000.bcf')
    register_file(species='Solanum Lycopersicum',
                  genome='SL.2.40',
                  datatype='genes',
                  filename='tests/data/S_lycopersicum_May_2012.chr6-0-100000.bb')
    register_file(species='Solanum Lycopersicum',
                  genome='SL.2.40',
                  datatype='features',
                  filename='tests/data/A-AFFY-87.bb')


@pytest.fixture()
def myapp(tmpdir):
    app.config['WHOOSH_BASE_DIR'] = tmpdir.strpath
    app.config['DATABASE'] = ':memory:'
    return app


def test_get_species(myapp):
    with myapp.test_request_context():
        setup_database()
        response = species.search()
        assert response == [{'name': 'Solanum Lycopersicum', 'species_id': 'Solanum%20Lycopersicum'}]


@pytest.fixture()
def expected_genome():
    return {
        'accessions': ['RF_001_SZAXPI008746-45',
                       'RF_002_SZAXPI009284-57',
                       'RF_003_SZAXPI009285-62',
                       'RF_004_SZAXPI009286-74',
                       'RF_005_SZAXPI009287-75',
                       'RF_006_SZAXPI009288-79',
                       'RF_007_SZAXPI009289-84',
                       'RF_008_SZAXPI009290-87',
                       'RF_011_SZAXPI009291-88',
                       'RF_012_SZAXPI009292-89',
                       'RF_013_SZAXPI009293-90',
                       'RF_014_SZAXPI009294-93',
                       'RF_015_SZAXPI009295-94',
                       'RF_016_SZAXPI009296-95',
                       'RF_017_SZAXPI009297-102',
                       'RF_018_SZAXPI009298-108',
                       'RF_019_SZAXPI009299-109',
                       'RF_020_SZAXPI009300-113',
                       'RF_021_SZAXPI009301-123',
                       'RF_022_SZAXPI009302-129',
                       'RF_023_SZAXPI009303-133',
                       'RF_024_SZAXPI009304-136',
                       'RF_025_SZAXPI009305-140',
                       'RF_026_SZAXPI009306-142',
                       'RF_027_SZAXPI009307-158',
                       'RF_028_SZAXPI009308-166',
                       'RF_029_SZAXPI009309-169',
                       'RF_030_SZAXPI009310-62',
                       'RF_031_SZAXPI009311-74',
                       'RF_032_SZAXPI009312-75',
                       'RF_033_SZAXPI009313-79',
                       'RF_034_SZAXPI009314-84',
                       'RF_035_SZAXPI009315-87',
                       'RF_036_SZAXPI009316-88',
                       'RF_037_SZAXPI008747-46',
                       'RF_038_SZAXPI009317-89',
                       'RF_039_SZAXPI009318-90',
                       'RF_040_SZAXPI009319-93',
                       'RF_041_SZAXPI009320-94',
                       'RF_042_SZAXPI009321-95',
                       'RF_043_SZAXPI009322-102',
                       'RF_044_SZAXPI009323-108',
                       'RF_045_SZAXPI009324-109',
                       'RF_046_SZAXPI008748-47',
                       'RF_047_SZAXPI009326-113',
                       'RF_049_SZAXPI009327-123',
                       'RF_051_SZAXPI009328-129',
                       'RF_052_SZAXPI009329-133',
                       'RF_053_SZAXPI009330-136',
                       'RF_054_SZAXPI009331-140',
                       'RF_055_SZAXPI009332-142',
                       'RF_056_SZAXPI009333-158',
                       'RF_057_SZAXPI009334-166',
                       'RF_058_SZAXPI009359-46',
                       'RF_059_SZAXPI009335-169',
                       'RF_063_SZAXPI009338-16-2',
                       'RF_064_SZAXPI009339-17-2',
                       'RF_065_SZAXPI009340-18',
                       'RF_066_SZAXPI009341-19',
                       'RF_067_SZAXPI009342-21',
                       'RF_068_SZAXPI009343-22-2',
                       'RF_069_SZAXPI009344-23',
                       'RF_070_SZAXPI008749-56',
                       'RF_071_SZAXPI009345-24',
                       'RF_072_SZAXPI008752-75',
                       'RF_073_SZAXPI009346-25',
                       'RF_074_SZAXPI008753-79',
                       'RF_075_SZAXPI009347-26',
                       'RF_077_SZAXPI009348-27',
                       'RF_078_SZAXPI009349-30',
                       'RF_088_SZAXPI009350-31',
                       'RF_089_SZAXPI009351-32',
                       'RF_090_SZAXPI009352-35',
                       'RF_091_SZAXPI009325-56',
                       'RF_093_SZAXPI009353-36',
                       'RF_094_SZAXPI008750-57',
                       'RF_096_SZAXPI009354-37',
                       'RF_097_SZAXPI009355-39',
                       'RF_102_SZAXPI009356-41',
                       'RF_103_SZAXPI009357-44',
                       'RF_104_SZAXPI008751-74',
                       'RF_105_SZAXPI009358-45'],
        'chromosomes': [{'chrom_id': 'SL2.40ch06', 'length': 100000}],
        'feature_tracks': [{'label': 'A-AFFY-87', 'url': 'tests/data/A-AFFY-87.bb'}],
        'gene_track': 'tests/data/S_lycopersicum_May_2012.chr6-0-100000.bb',
        'genome_id': 'SL.2.40',
        'reference': 'tests/data/S_lycopersicum_chromosomes.2.40.chr6-0-100000.2bit',
        'species': {'name': 'Solanum Lycopersicum',
                    'species_id': 'Solanum%20Lycopersicum'},
        'variants_filename': 'tests/data/tomato_snps.chr6-0-100000.bcf'
    }


def test_get_genomes_of_species(myapp, expected_genome):
    with myapp.test_request_context():
        setup_database()
        response = species.genomes('Solanum Lycopersicum')
        assert response == [expected_genome]


def test_get_genomes_of_species__wrongspecies__nogenomes(myapp):
    with myapp.test_request_context():
        setup_database()
        response = species.genomes('Wrong species')
        assert response == []


def test_get_genome(myapp, expected_genome):
    with myapp.test_request_context():
        setup_database()
        response = genomes.get('SL.2.40')
        assert response == expected_genome


def test_get_genome__wronggenome_notfound(myapp):
    with myapp.test_request_context():
        setup_database()
        response = genomes.get('Wrong genome')
        assert response.status_code == 404


def test_get_haplotypes(myapp):
    with myapp.test_request_context():
        setup_database()
        response = genomes.haplotypes(genome_id='SL.2.40', chrom_id='SL2.40ch06', start_position=2010,
                                      end_position=3000)
        data = simplejson.loads(response.get_data())
        assert len(data['haplotypes']) == 29
        assert len(data['hierarchy']['children']) == 1
        # Content of response is better tests in test_variants.py


def test_get_haplotypes__wronggenome_notfound(myapp):
    with myapp.test_request_context():
        setup_database()
        response = genomes.haplotypes(genome_id='Wrong genome', chrom_id='SL2.40ch06', start_position=2000,
                                      end_position=3000)
        assert response.status_code == 404


def test_get_haplotypes__wrongchrom_notfound(myapp):
    with myapp.test_request_context():
        setup_database()
        response = genomes.haplotypes(genome_id='SL.2.40', chrom_id='Wrong chromosome', start_position=2000,
                                      end_position=3000)
        assert response.status_code == 404


def test_get_haplotypes_aboverange__notacceptable(myapp):
    with myapp.test_request_context():
        setup_database()
        response = genomes.haplotypes(genome_id='SL.2.40', chrom_id='SL2.40ch06', start_position=2000,
                                      end_position=30000000)
        assert response.status_code == 406


def test_gene_search(myapp):
    with myapp.test_request_context():
        setup_database()
        response = genomes.gene_search(genome_id='SL.2.40', query='IPR007810')
        expected = [{'chrom': 'SL2.40ch06',
                     'end': 96654,
                     'gene_id': 'Solyc06g005080.2',
                     'id': 'Solyc06g005080.2.1',
                     'name': 'Vacuolar protein sorting-associated protein 18 (AHRD V1 ***- '
                             'D0MR96_PHYIN)%3B contains Interpro domain(s)  IPR007810  '
                             'Pep3/Vps18/deep orange ',
                     'start': 59969}]
        assert response == expected


def test_gene_search__wronggenome_notfound(myapp):
    with myapp.test_request_context():
        setup_database()
        response = genomes.gene_search(genome_id='Wrong genome', query='IPR007810')

        assert response.status_code == 404


def test_feature_search(myapp):
    with myapp.test_request_context():
        setup_database()
        response = genomes.feature_search(genome_id='SL.2.40', query='Les.3342.1.S1_at.126.409')
        expected = [{'attributes': 'ID=Les.3342.1.S1_at.126.409;Note="Affymetrix Tomato GeneChip '
                                   'Array Probe"',
                     'chrom': 'SL2.40ch06',
                     'end': 86383,
                     'name': 'Les.3342.1.S1_at.126.409',
                     'start': 86357,
                     'track': 'A-AFFY-87'}]
        assert response == expected


def test_feature_search__wronggenome_notfound(myapp):
    with myapp.test_request_context():
        setup_database()
        response = genomes.feature_search(genome_id='Wrong genome', query='Les.3342.1.S1_at.126.409')
        assert response.status_code == 404
