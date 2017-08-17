from avedata.variants import get_variants, cluster_sequences, add_variants2haplotypes, add_sequence2haplotypes, \
    cluster_haplotypes

"""
Tests run on a filtered vcf file 
"""


class Test_get_variants__singleSNP_altInSingleAccession(object):
    """
    File contains following entry
    SL2.40ch02	38496	G	T	RF_001_SZAXPI008746-45=.	RF_002_SZAXPI009284-57=.	RF_003_SZAXPI009285-62=.	RF_004_SZAXPI009286-74=.	RF_005_SZAXPI009287-75=.	RF_006_SZAXPI009288-79=.	RF_007_SZAXPI009289-84=.	RF_008_SZAXPI009290-87=.	RF_011_SZAXPI009291-88=.	RF_012_SZAXPI009292-89=.	RF_013_SZAXPI009293-90=.	RF_014_SZAXPI009294-93=.	RF_015_SZAXPI009295-94=.	RF_016_SZAXPI009296-95=.	RF_017_SZAXPI009297-102=.	RF_018_SZAXPI009298-108=.	RF_019_SZAXPI009299-109=.	RF_020_SZAXPI009300-113=.	RF_021_SZAXPI009301-123=.	RF_022_SZAXPI009302-129=.	RF_023_SZAXPI009303-133=.	RF_024_SZAXPI009304-136=.	RF_025_SZAXPI009305-140=.	RF_026_SZAXPI009306-142=.	RF_027_SZAXPI009307-158=.	RF_028_SZAXPI009308-166=.	RF_029_SZAXPI009309-169=.	RF_030_SZAXPI009310-62=.	RF_031_SZAXPI009311-74=.	RF_032_SZAXPI009312-75=.	RF_033_SZAXPI009313-79=.	RF_034_SZAXPI009314-84=.	RF_035_SZAXPI009315-87=.	RF_036_SZAXPI009316-88=.	RF_037_SZAXPI008747-46=.	RF_038_SZAXPI009317-89=.	RF_039_SZAXPI009318-90=.	RF_040_SZAXPI009319-93=.	RF_041_SZAXPI009320-94=.	RF_042_SZAXPI009321-95=.	RF_043_SZAXPI009322-102=.	RF_044_SZAXPI009323-108=.	RF_045_SZAXPI009324-109=.	RF_046_SZAXPI008748-47=.	RF_047_SZAXPI009326-113=.	RF_049_SZAXPI009327-123=.	RF_051_SZAXPI009328-129=.	RF_052_SZAXPI009329-133=0/1	RF_053_SZAXPI009330-136=.	RF_054_SZAXPI009331-140=.	RF_055_SZAXPI009332-142=.	RF_056_SZAXPI009333-158=.	RF_057_SZAXPI009334-166=.	RF_058_SZAXPI009359-46=.	RF_059_SZAXPI009335-169=.	RF_063_SZAXPI009338-16-2=.	RF_064_SZAXPI009339-17-2=.	RF_065_SZAXPI009340-18=.	RF_066_SZAXPI009341-19=.	RF_067_SZAXPI009342-21=.	RF_068_SZAXPI009343-22-2=.	RF_069_SZAXPI009344-23=.	RF_070_SZAXPI008749-56=.	RF_071_SZAXPI009345-24=.	RF_072_SZAXPI008752-75=.	RF_073_SZAXPI009346-25=.	RF_074_SZAXPI008753-79=.	RF_075_SZAXPI009347-26=.	RF_077_SZAXPI009348-27=.	RF_078_SZAXPI009349-30=.	RF_088_SZAXPI009350-31=.	RF_089_SZAXPI009351-32=.	RF_090_SZAXPI009352-35=.	RF_091_SZAXPI009325-56=.	RF_093_SZAXPI009353-36=.	RF_094_SZAXPI008750-57=.	RF_096_SZAXPI009354-37=.	RF_097_SZAXPI009355-39=.	RF_102_SZAXPI009356-41=.	RF_103_SZAXPI009357-44=.	RF_104_SZAXPI008751-74=.	RF_105_SZAXPI009358-45=.
    """
    variant_file = 'tests/data/ave2-tomato-ch2-33497-38497.bcf'
    chrom_id = 'SL2.40ch02'
    start_position = 38490
    end_position = 38500

    def test_allAccessions(self):
        accessions = []

        (variants, sequences) = get_variants(self.variant_file, self.chrom_id, self.start_position, self.end_position, accessions)

        expected_sequences = {
            'RF_001_SZAXPI008746-45': 'G',
            'RF_002_SZAXPI009284-57': 'G',
            'RF_003_SZAXPI009285-62': 'G',
            'RF_004_SZAXPI009286-74': 'G',
            'RF_005_SZAXPI009287-75': 'G',
            'RF_006_SZAXPI009288-79': 'G',
            'RF_007_SZAXPI009289-84': 'G',
            'RF_008_SZAXPI009290-87': 'G',
            'RF_011_SZAXPI009291-88': 'G',
            'RF_012_SZAXPI009292-89': 'G',
            'RF_013_SZAXPI009293-90': 'G',
            'RF_014_SZAXPI009294-93': 'G',
            'RF_015_SZAXPI009295-94': 'G',
            'RF_016_SZAXPI009296-95': 'G',
            'RF_017_SZAXPI009297-102': 'G',
            'RF_018_SZAXPI009298-108': 'G',
            'RF_019_SZAXPI009299-109': 'G',
            'RF_020_SZAXPI009300-113': 'G',
            'RF_021_SZAXPI009301-123': 'G',
            'RF_022_SZAXPI009302-129': 'G',
            'RF_023_SZAXPI009303-133': 'G',
            'RF_024_SZAXPI009304-136': 'G',
            'RF_025_SZAXPI009305-140': 'G',
            'RF_026_SZAXPI009306-142': 'G',
            'RF_027_SZAXPI009307-158': 'G',
            'RF_028_SZAXPI009308-166': 'G',
            'RF_029_SZAXPI009309-169': 'G',
            'RF_030_SZAXPI009310-62': 'G',
            'RF_031_SZAXPI009311-74': 'G',
            'RF_032_SZAXPI009312-75': 'G',
            'RF_033_SZAXPI009313-79': 'G',
            'RF_034_SZAXPI009314-84': 'G',
            'RF_035_SZAXPI009315-87': 'G',
            'RF_036_SZAXPI009316-88': 'G',
            'RF_037_SZAXPI008747-46': 'G',
            'RF_038_SZAXPI009317-89': 'G',
            'RF_039_SZAXPI009318-90': 'G',
            'RF_040_SZAXPI009319-93': 'G',
            'RF_041_SZAXPI009320-94': 'G',
            'RF_042_SZAXPI009321-95': 'G',
            'RF_043_SZAXPI009322-102': 'G',
            'RF_044_SZAXPI009323-108': 'G',
            'RF_045_SZAXPI009324-109': 'G',
            'RF_046_SZAXPI008748-47': 'G',
            'RF_047_SZAXPI009326-113': 'G',
            'RF_049_SZAXPI009327-123': 'G',
            'RF_051_SZAXPI009328-129': 'G',
            'RF_052_SZAXPI009329-133': 'T',
            'RF_053_SZAXPI009330-136': 'G',
            'RF_054_SZAXPI009331-140': 'G',
            'RF_055_SZAXPI009332-142': 'G',
            'RF_056_SZAXPI009333-158': 'G',
            'RF_057_SZAXPI009334-166': 'G',
            'RF_058_SZAXPI009359-46': 'G',
            'RF_059_SZAXPI009335-169': 'G',
            'RF_063_SZAXPI009338-16-2': 'G',
            'RF_064_SZAXPI009339-17-2': 'G',
            'RF_065_SZAXPI009340-18': 'G',
            'RF_066_SZAXPI009341-19': 'G',
            'RF_067_SZAXPI009342-21': 'G',
            'RF_068_SZAXPI009343-22-2': 'G',
            'RF_069_SZAXPI009344-23': 'G',
            'RF_070_SZAXPI008749-56': 'G',
            'RF_071_SZAXPI009345-24': 'G',
            'RF_072_SZAXPI008752-75': 'G',
            'RF_073_SZAXPI009346-25': 'G',
            'RF_074_SZAXPI008753-79': 'G',
            'RF_075_SZAXPI009347-26': 'G',
            'RF_077_SZAXPI009348-27': 'G',
            'RF_078_SZAXPI009349-30': 'G',
            'RF_088_SZAXPI009350-31': 'G',
            'RF_089_SZAXPI009351-32': 'G',
            'RF_090_SZAXPI009352-35': 'G',
            'RF_091_SZAXPI009325-56': 'G',
            'RF_093_SZAXPI009353-36': 'G',
            'RF_094_SZAXPI008750-57': 'G',
            'RF_096_SZAXPI009354-37': 'G',
            'RF_097_SZAXPI009355-39': 'G',
            'RF_102_SZAXPI009356-41': 'G',
            'RF_103_SZAXPI009357-44': 'G',
            'RF_104_SZAXPI008751-74': 'G',
            'RF_105_SZAXPI009358-45': 'G',
        }
        assert expected_sequences == sequences
        variant = variants[0]
        assert variant['alt'] == ['T']
        assert variant['chrom'] == self.chrom_id
        assert variant['ref'] == 'G'
        assert len(variant['genotypes']) == 1
        genotype = variant['genotypes'][0]
        assert genotype['accession'] == 'RF_052_SZAXPI009329-133'

    def test_subsetAccessionsAreEqualToRef(self):
        accessions = ['RF_077_SZAXPI009348-27', 'RF_001_SZAXPI008746-45']

        (variants, sequences) = get_variants(self.variant_file, self.chrom_id, self.start_position, self.end_position, accessions)

        expected_sequences = {
            'RF_077_SZAXPI009348-27': 'G',
            'RF_001_SZAXPI008746-45': 'G'
        }
        assert expected_sequences == sequences
        assert len(variants) == 1
        variant = variants[0]
        assert variant['alt'] == ['T']
        assert variant['chrom'] == self.chrom_id
        assert variant['ref'] == 'G'
        assert variant['genotypes'] == []

    def test_subsetEvenRefAlf(self):
        accessions = ['RF_052_SZAXPI009329-133', 'RF_001_SZAXPI008746-45']

        (variants, sequences) = get_variants(self.variant_file, self.chrom_id, self.start_position, self.end_position, accessions)

        expected_sequences = {
            'RF_001_SZAXPI008746-45': 'G',
            'RF_052_SZAXPI009329-133': 'T'
        }
        assert expected_sequences == sequences
        assert len(variants) == 1
        variant = variants[0]
        assert variant['alt'] == ['T']
        assert variant['chrom'] == self.chrom_id
        assert variant['ref'] == 'G'
        assert len(variant['genotypes']) == 1
        genotype = variant['genotypes'][0]
        assert genotype['accession'] == 'RF_052_SZAXPI009329-133'


class Test_get_variants__singleSNP_altInMultiAccession(object):
    """
    File contains following entry
    SL2.40ch02	38489	A	T,G	RF_001_SZAXPI008746-45=.	RF_002_SZAXPI009284-57=.	RF_003_SZAXPI009285-62=.	RF_004_SZAXPI009286-74=.	RF_005_SZAXPI009287-75=.	RF_006_SZAXPI009288-79=.	RF_007_SZAXPI009289-84=.	RF_008_SZAXPI009290-87=.	RF_011_SZAXPI009291-88=.	RF_012_SZAXPI009292-89=.	RF_013_SZAXPI009293-90=.	RF_014_SZAXPI009294-93=.	RF_015_SZAXPI009295-94=.	RF_016_SZAXPI009296-95=.	RF_017_SZAXPI009297-102=.	RF_018_SZAXPI009298-108=.	RF_019_SZAXPI009299-109=.	RF_020_SZAXPI009300-113=.	RF_021_SZAXPI009301-123=.	RF_022_SZAXPI009302-129=.	RF_023_SZAXPI009303-133=.	RF_024_SZAXPI009304-136=.	RF_025_SZAXPI009305-140=2/2	RF_026_SZAXPI009306-142=.	RF_027_SZAXPI009307-158=.	RF_028_SZAXPI009308-166=.	RF_029_SZAXPI009309-169=.	RF_030_SZAXPI009310-62=.	RF_031_SZAXPI009311-74=.	RF_032_SZAXPI009312-75=.	RF_033_SZAXPI009313-79=.	RF_034_SZAXPI009314-84=.	RF_035_SZAXPI009315-87=.	RF_036_SZAXPI009316-88=.	RF_037_SZAXPI008747-46=.	RF_038_SZAXPI009317-89=.	RF_039_SZAXPI009318-90=.	RF_040_SZAXPI009319-93=.	RF_041_SZAXPI009320-94=.	RF_042_SZAXPI009321-95=.	RF_043_SZAXPI009322-102=.	RF_044_SZAXPI009323-108=.	RF_045_SZAXPI009324-109=.	RF_046_SZAXPI008748-47=.	RF_047_SZAXPI009326-113=.	RF_049_SZAXPI009327-123=2/2	RF_051_SZAXPI009328-129=.	RF_052_SZAXPI009329-133=.	RF_053_SZAXPI009330-136=.	RF_054_SZAXPI009331-140=.	RF_055_SZAXPI009332-142=.	RF_056_SZAXPI009333-158=.	RF_057_SZAXPI009334-166=.	RF_058_SZAXPI009359-46=.	RF_059_SZAXPI009335-169=.	RF_063_SZAXPI009338-16-2=0/2	RF_064_SZAXPI009339-17-2=2/2	RF_065_SZAXPI009340-18=2/2	RF_066_SZAXPI009341-19=1/1	RF_067_SZAXPI009342-21=1/1	RF_068_SZAXPI009343-22-2=1/1	RF_069_SZAXPI009344-23=1/1	RF_070_SZAXPI008749-56=1/1	RF_071_SZAXPI009345-24=1/1	RF_072_SZAXPI008752-75=1/1	RF_073_SZAXPI009346-25=2/2	RF_074_SZAXPI008753-79=.	RF_075_SZAXPI009347-26=2/2	RF_077_SZAXPI009348-27=.	RF_078_SZAXPI009349-30=.	RF_088_SZAXPI009350-31=.	RF_089_SZAXPI009351-32=.	RF_090_SZAXPI009352-35=.	RF_091_SZAXPI009325-56=.	RF_093_SZAXPI009353-36=.	RF_094_SZAXPI008750-57=.	RF_096_SZAXPI009354-37=.	RF_097_SZAXPI009355-39=.	RF_102_SZAXPI009356-41=.	RF_103_SZAXPI009357-44=.	RF_104_SZAXPI008751-74=.	RF_105_SZAXPI009358-45=.
    """
    variant_file = 'tests/data/ave2-tomato-ch2-33497-38497.bcf'
    chrom_id = 'SL2.40ch02'
    start_position = 38486
    end_position = 38492

    def test_allAccession(self):
        accessions = []

        (variants, sequences) = get_variants(self.variant_file, self.chrom_id, self.start_position, self.end_position, accessions)

        expected_sequences = {
            'RF_001_SZAXPI008746-45': 'A',
            'RF_002_SZAXPI009284-57': 'A',
            'RF_003_SZAXPI009285-62': 'A',
            'RF_004_SZAXPI009286-74': 'A',
            'RF_005_SZAXPI009287-75': 'A',
            'RF_006_SZAXPI009288-79': 'A',
            'RF_007_SZAXPI009289-84': 'A',
            'RF_008_SZAXPI009290-87': 'A',
            'RF_011_SZAXPI009291-88': 'A',
            'RF_012_SZAXPI009292-89': 'A',
            'RF_013_SZAXPI009293-90': 'A',
            'RF_014_SZAXPI009294-93': 'A',
            'RF_015_SZAXPI009295-94': 'A',
            'RF_016_SZAXPI009296-95': 'A',
            'RF_017_SZAXPI009297-102': 'A',
            'RF_018_SZAXPI009298-108': 'A',
            'RF_019_SZAXPI009299-109': 'A',
            'RF_020_SZAXPI009300-113': 'A',
            'RF_021_SZAXPI009301-123': 'A',
            'RF_022_SZAXPI009302-129': 'A',
            'RF_023_SZAXPI009303-133': 'A',
            'RF_024_SZAXPI009304-136': 'A',
            'RF_025_SZAXPI009305-140': 'T',
            'RF_026_SZAXPI009306-142': 'A',
            'RF_027_SZAXPI009307-158': 'A',
            'RF_028_SZAXPI009308-166': 'A',
            'RF_029_SZAXPI009309-169': 'A',
            'RF_030_SZAXPI009310-62': 'A',
            'RF_031_SZAXPI009311-74': 'A',
            'RF_032_SZAXPI009312-75': 'A',
            'RF_033_SZAXPI009313-79': 'A',
            'RF_034_SZAXPI009314-84': 'A',
            'RF_035_SZAXPI009315-87': 'A',
            'RF_036_SZAXPI009316-88': 'A',
            'RF_037_SZAXPI008747-46': 'A',
            'RF_038_SZAXPI009317-89': 'A',
            'RF_039_SZAXPI009318-90': 'A',
            'RF_040_SZAXPI009319-93': 'A',
            'RF_041_SZAXPI009320-94': 'A',
            'RF_042_SZAXPI009321-95': 'A',
            'RF_043_SZAXPI009322-102': 'A',
            'RF_044_SZAXPI009323-108': 'A',
            'RF_045_SZAXPI009324-109': 'A',
            'RF_046_SZAXPI008748-47': 'A',
            'RF_047_SZAXPI009326-113': 'A',
            'RF_049_SZAXPI009327-123': 'T',
            'RF_051_SZAXPI009328-129': 'A',
            'RF_052_SZAXPI009329-133': 'A',
            'RF_053_SZAXPI009330-136': 'A',
            'RF_054_SZAXPI009331-140': 'A',
            'RF_055_SZAXPI009332-142': 'A',
            'RF_056_SZAXPI009333-158': 'A',
            'RF_057_SZAXPI009334-166': 'A',
            'RF_058_SZAXPI009359-46': 'A',
            'RF_059_SZAXPI009335-169': 'A',
            'RF_063_SZAXPI009338-16-2': 'T',
            'RF_064_SZAXPI009339-17-2': 'T',
            'RF_065_SZAXPI009340-18': 'T',
            'RF_066_SZAXPI009341-19': 'T',
            'RF_067_SZAXPI009342-21': 'T',
            'RF_068_SZAXPI009343-22-2': 'T',
            'RF_069_SZAXPI009344-23': 'T',
            'RF_070_SZAXPI008749-56': 'T',
            'RF_071_SZAXPI009345-24': 'T',
            'RF_072_SZAXPI008752-75': 'T',
            'RF_073_SZAXPI009346-25': 'T',
            'RF_074_SZAXPI008753-79': 'A',
            'RF_075_SZAXPI009347-26': 'T',
            'RF_077_SZAXPI009348-27': 'A',
            'RF_078_SZAXPI009349-30': 'A',
            'RF_088_SZAXPI009350-31': 'A',
            'RF_089_SZAXPI009351-32': 'A',
            'RF_090_SZAXPI009352-35': 'A',
            'RF_091_SZAXPI009325-56': 'A',
            'RF_093_SZAXPI009353-36': 'A',
            'RF_094_SZAXPI008750-57': 'A',
            'RF_096_SZAXPI009354-37': 'A',
            'RF_097_SZAXPI009355-39': 'A',
            'RF_102_SZAXPI009356-41': 'A',
            'RF_103_SZAXPI009357-44': 'A',
            'RF_104_SZAXPI008751-74': 'A',
            'RF_105_SZAXPI009358-45': 'A',
        }
        assert expected_sequences == sequences
        assert len(variants) == 1
        variant = variants[0]
        assert variant['alt'] == ['T', 'G']
        assert variant['chrom'] == self.chrom_id
        assert variant['ref'] == 'A'
        assert len(variant['genotypes']) == 14
        genotype_accessions = [g['accession'] for g in variant['genotypes']]
        expected_genotype_accessions = [
            'RF_025_SZAXPI009305-140',
            'RF_049_SZAXPI009327-123',
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
            'RF_075_SZAXPI009347-26',
        ]
        assert expected_genotype_accessions == genotype_accessions


class Test_get_variants__twoSNP(object):
    """
    File contains following entry
    SL2.40ch02	38489	A	T,G	RF_001_SZAXPI008746-45=.	RF_002_SZAXPI009284-57=.	RF_003_SZAXPI009285-62=.	RF_004_SZAXPI009286-74=.	RF_005_SZAXPI009287-75=.	RF_006_SZAXPI009288-79=.	RF_007_SZAXPI009289-84=.	RF_008_SZAXPI009290-87=.	RF_011_SZAXPI009291-88=.	RF_012_SZAXPI009292-89=.	RF_013_SZAXPI009293-90=.	RF_014_SZAXPI009294-93=.	RF_015_SZAXPI009295-94=.	RF_016_SZAXPI009296-95=.	RF_017_SZAXPI009297-102=.	RF_018_SZAXPI009298-108=.	RF_019_SZAXPI009299-109=.	RF_020_SZAXPI009300-113=.	RF_021_SZAXPI009301-123=.	RF_022_SZAXPI009302-129=.	RF_023_SZAXPI009303-133=.	RF_024_SZAXPI009304-136=.	RF_025_SZAXPI009305-140=2/2	RF_026_SZAXPI009306-142=.	RF_027_SZAXPI009307-158=.	RF_028_SZAXPI009308-166=.	RF_029_SZAXPI009309-169=.	RF_030_SZAXPI009310-62=.	RF_031_SZAXPI009311-74=.	RF_032_SZAXPI009312-75=.	RF_033_SZAXPI009313-79=.	RF_034_SZAXPI009314-84=.	RF_035_SZAXPI009315-87=.	RF_036_SZAXPI009316-88=.	RF_037_SZAXPI008747-46=.	RF_038_SZAXPI009317-89=.	RF_039_SZAXPI009318-90=.	RF_040_SZAXPI009319-93=.	RF_041_SZAXPI009320-94=.	RF_042_SZAXPI009321-95=.	RF_043_SZAXPI009322-102=.	RF_044_SZAXPI009323-108=.	RF_045_SZAXPI009324-109=.	RF_046_SZAXPI008748-47=.	RF_047_SZAXPI009326-113=.	RF_049_SZAXPI009327-123=2/2	RF_051_SZAXPI009328-129=.	RF_052_SZAXPI009329-133=.	RF_053_SZAXPI009330-136=.	RF_054_SZAXPI009331-140=.	RF_055_SZAXPI009332-142=.	RF_056_SZAXPI009333-158=.	RF_057_SZAXPI009334-166=.	RF_058_SZAXPI009359-46=.	RF_059_SZAXPI009335-169=.	RF_063_SZAXPI009338-16-2=0/2	RF_064_SZAXPI009339-17-2=2/2	RF_065_SZAXPI009340-18=2/2	RF_066_SZAXPI009341-19=1/1	RF_067_SZAXPI009342-21=1/1	RF_068_SZAXPI009343-22-2=1/1	RF_069_SZAXPI009344-23=1/1	RF_070_SZAXPI008749-56=1/1	RF_071_SZAXPI009345-24=1/1	RF_072_SZAXPI008752-75=1/1	RF_073_SZAXPI009346-25=2/2	RF_074_SZAXPI008753-79=.	RF_075_SZAXPI009347-26=2/2	RF_077_SZAXPI009348-27=.	RF_078_SZAXPI009349-30=.	RF_088_SZAXPI009350-31=.	RF_089_SZAXPI009351-32=.	RF_090_SZAXPI009352-35=.	RF_091_SZAXPI009325-56=.	RF_093_SZAXPI009353-36=.	RF_094_SZAXPI008750-57=.	RF_096_SZAXPI009354-37=.	RF_097_SZAXPI009355-39=.	RF_102_SZAXPI009356-41=.	RF_103_SZAXPI009357-44=.	RF_104_SZAXPI008751-74=.	RF_105_SZAXPI009358-45=.
    SL2.40ch02	38496	G	T	RF_001_SZAXPI008746-45=.	RF_002_SZAXPI009284-57=.	RF_003_SZAXPI009285-62=.	RF_004_SZAXPI009286-74=.	RF_005_SZAXPI009287-75=.	RF_006_SZAXPI009288-79=.	RF_007_SZAXPI009289-84=.	RF_008_SZAXPI009290-87=.	RF_011_SZAXPI009291-88=.	RF_012_SZAXPI009292-89=.	RF_013_SZAXPI009293-90=.	RF_014_SZAXPI009294-93=.	RF_015_SZAXPI009295-94=.	RF_016_SZAXPI009296-95=.	RF_017_SZAXPI009297-102=.	RF_018_SZAXPI009298-108=.	RF_019_SZAXPI009299-109=.	RF_020_SZAXPI009300-113=.	RF_021_SZAXPI009301-123=.	RF_022_SZAXPI009302-129=.	RF_023_SZAXPI009303-133=.	RF_024_SZAXPI009304-136=.	RF_025_SZAXPI009305-140=.	RF_026_SZAXPI009306-142=.	RF_027_SZAXPI009307-158=.	RF_028_SZAXPI009308-166=.	RF_029_SZAXPI009309-169=.	RF_030_SZAXPI009310-62=.	RF_031_SZAXPI009311-74=.	RF_032_SZAXPI009312-75=.	RF_033_SZAXPI009313-79=.	RF_034_SZAXPI009314-84=.	RF_035_SZAXPI009315-87=.	RF_036_SZAXPI009316-88=.	RF_037_SZAXPI008747-46=.	RF_038_SZAXPI009317-89=.	RF_039_SZAXPI009318-90=.	RF_040_SZAXPI009319-93=.	RF_041_SZAXPI009320-94=.	RF_042_SZAXPI009321-95=.	RF_043_SZAXPI009322-102=.	RF_044_SZAXPI009323-108=.	RF_045_SZAXPI009324-109=.	RF_046_SZAXPI008748-47=.	RF_047_SZAXPI009326-113=.	RF_049_SZAXPI009327-123=.	RF_051_SZAXPI009328-129=.	RF_052_SZAXPI009329-133=0/1	RF_053_SZAXPI009330-136=.	RF_054_SZAXPI009331-140=.	RF_055_SZAXPI009332-142=.	RF_056_SZAXPI009333-158=.	RF_057_SZAXPI009334-166=.	RF_058_SZAXPI009359-46=.	RF_059_SZAXPI009335-169=.	RF_063_SZAXPI009338-16-2=.	RF_064_SZAXPI009339-17-2=.	RF_065_SZAXPI009340-18=.	RF_066_SZAXPI009341-19=.	RF_067_SZAXPI009342-21=.	RF_068_SZAXPI009343-22-2=.	RF_069_SZAXPI009344-23=.	RF_070_SZAXPI008749-56=.	RF_071_SZAXPI009345-24=.	RF_072_SZAXPI008752-75=.	RF_073_SZAXPI009346-25=.	RF_074_SZAXPI008753-79=.	RF_075_SZAXPI009347-26=.	RF_077_SZAXPI009348-27=.	RF_078_SZAXPI009349-30=.	RF_088_SZAXPI009350-31=.	RF_089_SZAXPI009351-32=.	RF_090_SZAXPI009352-35=.	RF_091_SZAXPI009325-56=.	RF_093_SZAXPI009353-36=.	RF_094_SZAXPI008750-57=.	RF_096_SZAXPI009354-37=.	RF_097_SZAXPI009355-39=.	RF_102_SZAXPI009356-41=.	RF_103_SZAXPI009357-44=.	RF_104_SZAXPI008751-74=.	RF_105_SZAXPI009358-45=.
    """
    variant_file = 'tests/data/ave2-tomato-ch2-33497-38497.bcf'
    chrom_id = 'SL2.40ch02'
    start_position = 38486
    end_position = 38500

    def test_allAccession(self):
        accessions = []

        (variants, sequences) = get_variants(self.variant_file, self.chrom_id, self.start_position, self.end_position, accessions)

        expected_sequences = {
            'RF_001_SZAXPI008746-45': 'AG',
            'RF_002_SZAXPI009284-57': 'AG',
            'RF_003_SZAXPI009285-62': 'AG',
            'RF_004_SZAXPI009286-74': 'AG',
            'RF_005_SZAXPI009287-75': 'AG',
            'RF_006_SZAXPI009288-79': 'AG',
            'RF_007_SZAXPI009289-84': 'AG',
            'RF_008_SZAXPI009290-87': 'AG',
            'RF_011_SZAXPI009291-88': 'AG',
            'RF_012_SZAXPI009292-89': 'AG',
            'RF_013_SZAXPI009293-90': 'AG',
            'RF_014_SZAXPI009294-93': 'AG',
            'RF_015_SZAXPI009295-94': 'AG',
            'RF_016_SZAXPI009296-95': 'AG',
            'RF_017_SZAXPI009297-102': 'AG',
            'RF_018_SZAXPI009298-108': 'AG',
            'RF_019_SZAXPI009299-109': 'AG',
            'RF_020_SZAXPI009300-113': 'AG',
            'RF_021_SZAXPI009301-123': 'AG',
            'RF_022_SZAXPI009302-129': 'AG',
            'RF_023_SZAXPI009303-133': 'AG',
            'RF_024_SZAXPI009304-136': 'AG',
            'RF_025_SZAXPI009305-140': 'TG',
            'RF_026_SZAXPI009306-142': 'AG',
            'RF_027_SZAXPI009307-158': 'AG',
            'RF_028_SZAXPI009308-166': 'AG',
            'RF_029_SZAXPI009309-169': 'AG',
            'RF_030_SZAXPI009310-62': 'AG',
            'RF_031_SZAXPI009311-74': 'AG',
            'RF_032_SZAXPI009312-75': 'AG',
            'RF_033_SZAXPI009313-79': 'AG',
            'RF_034_SZAXPI009314-84': 'AG',
            'RF_035_SZAXPI009315-87': 'AG',
            'RF_036_SZAXPI009316-88': 'AG',
            'RF_037_SZAXPI008747-46': 'AG',
            'RF_038_SZAXPI009317-89': 'AG',
            'RF_039_SZAXPI009318-90': 'AG',
            'RF_040_SZAXPI009319-93': 'AG',
            'RF_041_SZAXPI009320-94': 'AG',
            'RF_042_SZAXPI009321-95': 'AG',
            'RF_043_SZAXPI009322-102': 'AG',
            'RF_044_SZAXPI009323-108': 'AG',
            'RF_045_SZAXPI009324-109': 'AG',
            'RF_046_SZAXPI008748-47': 'AG',
            'RF_047_SZAXPI009326-113': 'AG',
            'RF_049_SZAXPI009327-123': 'TG',
            'RF_051_SZAXPI009328-129': 'AG',
            'RF_052_SZAXPI009329-133': 'AT',
            'RF_053_SZAXPI009330-136': 'AG',
            'RF_054_SZAXPI009331-140': 'AG',
            'RF_055_SZAXPI009332-142': 'AG',
            'RF_056_SZAXPI009333-158': 'AG',
            'RF_057_SZAXPI009334-166': 'AG',
            'RF_058_SZAXPI009359-46': 'AG',
            'RF_059_SZAXPI009335-169': 'AG',
            'RF_063_SZAXPI009338-16-2': 'TG',
            'RF_064_SZAXPI009339-17-2': 'TG',
            'RF_065_SZAXPI009340-18': 'TG',
            'RF_066_SZAXPI009341-19': 'TG',
            'RF_067_SZAXPI009342-21': 'TG',
            'RF_068_SZAXPI009343-22-2': 'TG',
            'RF_069_SZAXPI009344-23': 'TG',
            'RF_070_SZAXPI008749-56': 'TG',
            'RF_071_SZAXPI009345-24': 'TG',
            'RF_072_SZAXPI008752-75': 'TG',
            'RF_073_SZAXPI009346-25': 'TG',
            'RF_074_SZAXPI008753-79': 'AG',
            'RF_075_SZAXPI009347-26': 'TG',
            'RF_077_SZAXPI009348-27': 'AG',
            'RF_078_SZAXPI009349-30': 'AG',
            'RF_088_SZAXPI009350-31': 'AG',
            'RF_089_SZAXPI009351-32': 'AG',
            'RF_090_SZAXPI009352-35': 'AG',
            'RF_091_SZAXPI009325-56': 'AG',
            'RF_093_SZAXPI009353-36': 'AG',
            'RF_094_SZAXPI008750-57': 'AG',
            'RF_096_SZAXPI009354-37': 'AG',
            'RF_097_SZAXPI009355-39': 'AG',
            'RF_102_SZAXPI009356-41': 'AG',
            'RF_103_SZAXPI009357-44': 'AG',
            'RF_104_SZAXPI008751-74': 'AG',
            'RF_105_SZAXPI009358-45': 'AG',
        }
        assert expected_sequences == sequences
        assert len(variants) == 2
        variant1 = variants[0]
        assert variant1['alt'] == ['T', 'G']
        assert variant1['chrom'] == self.chrom_id
        assert variant1['ref'] == 'A'
        assert len(variant1['genotypes']) == 14
        genotype_accessions = [g['accession'] for g in variant1['genotypes']]
        expected_genotype_accessions = [
            'RF_025_SZAXPI009305-140',
            'RF_049_SZAXPI009327-123',
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
            'RF_075_SZAXPI009347-26',
        ]
        assert expected_genotype_accessions == genotype_accessions

        variant2 = variants[1]
        assert variant2['alt'] == ['T']
        assert variant2['chrom'] == self.chrom_id
        assert variant2['ref'] == 'G'
        assert len(variant2['genotypes']) == 1
        genotype = variant2['genotypes'][0]
        assert genotype['accession'] == 'RF_052_SZAXPI009329-133'


class Test_cluster_sequences(object):

    def drop_id(self, clusters):
        # ignore keys as they are random
        for h in clusters:
            del (h['haplotype_id'])

    def test_single_sequence(self):
        seqs = {
            'seqid1': 'ACTG'
        }

        clusters = cluster_sequences(seqs)

        expected_clusters = [{
                'accessions': ['seqid1']
        }]
        self.drop_id(clusters)
        assert clusters == expected_clusters

    def test_2seqs_singlecluster(self):
        seqs = {
            'seqid1': 'ACTG',
            'seqid2': 'ACTG'
        }

        clusters = cluster_sequences(seqs)

        expected_accessions = {'seqid1', 'seqid2'}
        # ignore keys as they are random
        assert len(clusters) == 1
        cluster = list(clusters)[0]
        accessions = set(cluster['accessions'])
        assert accessions == expected_accessions

    def test_2seqs_2clusters(self):
        seqs = {
            'seqid1': 'A',
            'seqid2': 'T'
        }

        clusters = cluster_sequences(seqs)

        assert len(clusters) == 2
        accessions_by_cluster = {frozenset(c['accessions']) for c in clusters}
        expected_accessions_by_cluster = {frozenset({'seqid1'}), frozenset({'seqid2'})}
        assert expected_accessions_by_cluster == accessions_by_cluster

    def test_3seqs_2clusters(self):
        seqs = {
            'seqid1': 'A',
            'seqid2': 'T',
            'seqid3': 'A'
        }

        clusters = cluster_sequences(seqs)

        assert len(clusters) == 2
        accessions_by_cluster = {frozenset(c['accessions']) for c in clusters}
        expected_accessions_by_cluster = {frozenset({'seqid1', 'seqid3'}), frozenset({'seqid2'})}
        assert expected_accessions_by_cluster == accessions_by_cluster


class Test_add_variants2haplotypes(object):

    def test_noVariants(self):
        haplotypes = [{
            'haplotype_id': 'hap1',
            'accessions': ['acc1']
        }]
        variants = []

        add_variants2haplotypes(haplotypes, variants)

        expected = [{
            'haplotype_id': 'hap1',
            'accessions': ['acc1'],
            'variants': []
        }]
        assert haplotypes == expected

    def test_otherAccVariant(self):
        haplotypes = [{
            'haplotype_id': 'hap1',
            'accessions': ['acc1']
        }]
        variants = [{
            'genotypes': [{
                'accession': 'acc2'
            }]
        }]

        add_variants2haplotypes(haplotypes, variants)

        expected = [{
            'haplotype_id': 'hap1',
            'accessions': ['acc1'],
            'variants': []
        }]
        assert haplotypes == expected

    def test_myVariantOnly(self):
        haplotypes = [{
            'haplotype_id': 'hap1',
            'accessions': ['acc1']
        }]
        variants = [{
            'genotypes': [{
                'accession': 'acc1',
                'genotype': '[1, 1]'
            }],
            'pos': 38496,
            'ref': 'G',
            'alt': 'T'
        }]

        add_variants2haplotypes(haplotypes, variants)

        expected = [{
            'haplotype_id': 'hap1',
            'accessions': ['acc1'],
            'variants': [{
                'genotypes': [{
                    'accession': 'acc1',
                    'genotype': '[1, 1]'
                }],
                'pos': 38496,
                'ref': 'G',
                'alt': 'T'
            }]
        }]
        assert haplotypes == expected

    def test_myVariantAndOther(self):
        haplotypes = [{
            'haplotype_id': 'hap1',
            'accessions': ['acc1']
        }]
        variants = [{
            'genotypes': [{
                'accession': 'acc1',
                'genotype': '[1, 1]'
            }, {
                'accession': 'acc2',
                'genotype': '[1, 1]'
            }],
            'pos': 38496,
            'ref': 'G',
            'alt': 'T'
        }]

        add_variants2haplotypes(haplotypes, variants)

        expected = [{
            'haplotype_id': 'hap1',
            'accessions': ['acc1'],
            'variants': [{
                'genotypes': [{
                    'accession': 'acc1',
                    'genotype': '[1, 1]'
                }],
                'pos': 38496,
                'ref': 'G',
                'alt': 'T'
            }]
        }]
        assert haplotypes == expected

    def test_2accessionsInSameVariant(self):
        haplotypes = [{
            'haplotype_id': 'hap1',
            'accessions': ['acc1', 'acc2']
        }]
        variants = [{
            'genotypes': [{
                'accession': 'acc1',
                'genotype': '[1, 1]'
            }, {
                'accession': 'acc2',
                'genotype': '[0, 1]'
            }],
            'pos': 38496,
            'ref': 'G',
            'alt': 'T'
        }]

        add_variants2haplotypes(haplotypes, variants)

        expected = [{
            'haplotype_id': 'hap1',
            'accessions': ['acc1', 'acc2'],
            'variants': [{
                'genotypes': [{
                    'accession': 'acc1',
                    'genotype': '[1, 1]'
                }, {
                    'accession': 'acc2',
                    'genotype': '[0, 1]'
                }],
                'pos': 38496,
                'ref': 'G',
                'alt': 'T'
            }]
        }]
        assert haplotypes == expected

    def test_2variants(self):
        haplotypes = [{
            'haplotype_id': 'hap1',
            'accessions': ['acc1']
        }]
        variants = [{
            'genotypes': [{
                'accession': 'acc1',
                'genotype': '[0, 1]'
            }],
            'pos': 38489,
            'ref': 'A',
            'alt': 'T'
        }, {
            'genotypes': [{
                'accession': 'acc1',
                'genotype': '[1, 1]'
            }],
            'pos': 38496,
            'ref': 'G',
            'alt': 'T'
        }]

        add_variants2haplotypes(haplotypes, variants)

        expected = [{
            'haplotype_id': 'hap1',
            'accessions': ['acc1'],
            'variants': [{
                'genotypes': [{
                    'accession': 'acc1',
                    'genotype': '[0, 1]'
                }],
                'pos': 38489,
                'ref': 'A',
                'alt': 'T'
            }, {
                'genotypes': [{
                    'accession': 'acc1',
                    'genotype': '[1, 1]'
                }],
                'pos': 38496,
                'ref': 'G',
                'alt': 'T'
            }]
        }]
        assert haplotypes == expected


class Test_add_sequence2haplotypes(object):
    def test_empty(self):
        haplotypes = {}
        ref_seq = 'ACTGACTG'
        start_position = 2

        add_sequence2haplotypes(haplotypes, ref_seq, start_position)

        assert haplotypes == {}

    def test_singleHaplotypeWith2Variants(self):
        haplotypes = [{
            'haplotype_id': 'hap1',
            'accessions': ['acc1'],
            'variants': [{
                'genotypes': [{
                    'accession': 'acc1',
                    'genotype': '[0, 1]'
                }],
                'pos': 38489,
                'ref': 'A',
                'alt': 'T'
            }, {
                'genotypes': [{
                    'accession': 'acc1',
                    'genotype': '[1, 1]'
                }],
                'pos': 38496,
                'ref': 'G',
                'alt': 'T'
            }]
        }]
        ref_seq = 'CCCCCCCCCCCC'
        start_position = 38486

        add_sequence2haplotypes(haplotypes, ref_seq, start_position)

        expected = [{
            'haplotype_id': 'hap1',
            'accessions': ['acc1'],
            'sequence': 'CCCTCCCCCCTC',
            'variants': [{
                'genotypes': [{
                    'accession': 'acc1',
                    'genotype': '[0, 1]'
                }],
                'pos': 38489,
                'ref': 'A',
                'alt': 'T'
            }, {
                'genotypes': [{
                    'accession': 'acc1',
                    'genotype': '[1, 1]'
                }],
                'pos': 38496,
                'ref': 'G',
                'alt': 'T'
            }]
        }]
        assert haplotypes == expected

    def test_singleHaplotypeWithNoVariants(self):
        haplotypes = [{
            'haplotype_id': 'hap1',
            'accessions': ['acc1'],
            'variants': []
        }]
        ref_seq = 'CCCCCCCCCCCC'
        start_position = 38486

        add_sequence2haplotypes(haplotypes, ref_seq, start_position)

        expected = [{
            'haplotype_id': 'hap1',
            'accessions': ['acc1'],
            'sequence': 'CCCCCCCCCCCC',
            'variants': []
        }]
        assert haplotypes == expected


class Test_cluster_haplotypes(object):

    def test_1HaplotypeWithoutVariants(self):
        haplotypes = [{
            'haplotype_id': 'hap1',
            'accessions': ['acc1'],
            'sequence': 'CCCCCCCCCCCC',
            'variants': []
        }]
        (hierarchy, ordered_haplotypes) = cluster_haplotypes(haplotypes)

        assert ordered_haplotypes == haplotypes
        expected_hierarchy = {
            'haplotype_id': 'hap1'
        }
        assert hierarchy == expected_hierarchy

    def test_1haplotypeWithoutVariantsAnd1HaplotyeWithVariant(self):
        haplotypes = [{
            'haplotype_id': 'hap1',
            'accessions': ['acc1'],
            'sequence': 'CCCCCCCCCCCC',
            'variants': []
        }, {
            'haplotype_id': 'hap2',
            'accessions': ['acc2'],
            'sequence': 'CCCTCCCCCCTC',
            'variants': [{
                'genotypes': [{
                    'accession': 'acc2',
                    'genotype': '[0, 1]'
                }],
                'pos': 38489,
                'ref': 'A',
                'alt': 'T'
            }, {
                'genotypes': [{
                    'accession': 'acc2',
                    'genotype': '[1, 1]'
                }],
                'pos': 38496,
                'ref': 'G',
                'alt': 'T'
            }]
        }]
        (hierarchy, ordered_haplotypes) = cluster_haplotypes(haplotypes)

        assert ordered_haplotypes == haplotypes
        expected_hierarchy = {
            'children': [{
                'children': [{
                    'haplotype_id': 'hap1'
                }, {
                    'haplotype_id': 'hap2'
                }]
            }]
        }
        assert hierarchy == expected_hierarchy
