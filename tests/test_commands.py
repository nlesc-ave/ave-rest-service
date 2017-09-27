import pytest
from click.testing import CliRunner
from whoosh.index import open_dir

from avedata.commands import cli
from avedata.app import app

app.config['DATABASE'] = ':memory:'


def test_list__emptydb():
    cli_runner = CliRunner()

    result = cli_runner.invoke(cli, ['list'])

    assert result.exit_code == 0
    assert 'species\tgenome\tdatatype\tfilename' in result.output


def test_drop_db__noexistingdb(tmpdir):
    app.config['DATABASE'] = tmpdir.join('ave.db').strpath
    cli_runner = CliRunner()

    result = cli_runner.invoke(cli, ['drop_db'])

    assert result.exit_code == -1
    with pytest.raises(FileNotFoundError):
        raise result.exception


def test_register_2bit(tmpdir):
    app.config['DATABASE'] = tmpdir.join('ave.db').strpath
    cli_runner = CliRunner()
    fn = 'tests/data/S_lycopersicum_chromosomes.2.40.chr6-0-100000.2bit'

    result = cli_runner.invoke(cli, [
        'register',
        '--species', 'Solanum Lycopersicum',
        '--genome', 'SL.2.40',
        '--datatype', '2bit',
        fn
    ])

    assert result.exit_code == 0
    assert 'New datafile has been registered.' in result.output
    list_result = cli_runner.invoke(cli, ['list'])
    assert fn in list_result.output


def test_register_2bit__usebcf_invalid():
    cli_runner = CliRunner()

    result = cli_runner.invoke(cli, [
        'register',
        '--species', 'Solanum Lycopersicum',
        '--genome', 'SL.2.40',
        '--datatype', '2bit',
        'tests/data/tomato_snps.chr6-0-100000.bcf'
    ])

    assert result.exit_code == 1
    assert 'Error: 2bit url could not be opened' in result.output


def test_register_variants(tmpdir):
    app.config['DATABASE'] = tmpdir.join('ave.db').strpath
    cli_runner = CliRunner()
    fn = 'tests/data/tomato_snps.chr6-0-100000.bcf'

    result = cli_runner.invoke(cli, [
        'register',
        '--species', 'Solanum Lycopersicum',
        '--genome', 'SL.2.40',
        '--datatype', 'variants',
        fn
    ])

    assert 'New datafile has been registered.' in result.output
    assert result.exit_code == 0
    list_result = cli_runner.invoke(cli, ['list'])
    assert fn in list_result.output


def test_register_variants__use2bit_invalid():
    cli_runner = CliRunner()

    result = cli_runner.invoke(cli, [
        'register',
        '--species', 'Solanum Lycopersicum',
        '--genome', 'SL.2.40',
        '--datatype', 'variants',
        'tests/data/S_lycopersicum_chromosomes.2.40.chr6-0-100000.2bit'
    ])

    assert 'Error while opening bcf file with cyvcf2' in result.output
    assert result.exit_code == 1


def test_deregister_2bit(tmpdir):
    app.config['DATABASE'] = tmpdir.join('ave.db').strpath
    cli_runner = CliRunner()
    fn = 'tests/data/S_lycopersicum_chromosomes.2.40.chr6-0-100000.2bit'
    cli_runner.invoke(cli, [
        'register',
        '--species', 'Solanum Lycopersicum',
        '--genome', 'SL.2.40',
        '--datatype', '2bit',
        fn
    ])

    result = cli_runner.invoke(cli, [
        'deregister',
        fn
    ])

    assert 'Deregistered entry' in result.output
    assert result.exit_code == 0


def test_register_genes(tmpdir):
    app.config['DATABASE'] = tmpdir.join('ave.db').strpath
    app.config['WHOOSH_BASE_DIR'] = tmpdir.strpath
    cli_runner = CliRunner()
    fn = 'tests/data/S_lycopersicum_May_2012.chr6-0-100000.bb'

    result = cli_runner.invoke(cli, [
        'register',
        '--species', 'Solanum Lycopersicum',
        '--genome', 'SL.2.40',
        '--datatype', 'genes',
        fn
    ])

    assert 'New datafile has been registered.' in result.output
    assert result.exit_code == 0
    whoosh_dir = tmpdir.join('S_lycopersicum_May_2012.chr6-0-100000.bb').strpath
    assert whoosh_doc_count(whoosh_dir) == 9
    list_result = cli_runner.invoke(cli, ['list'])
    assert fn in list_result.output


def test_register_features(tmpdir):
    app.config['DATABASE'] = tmpdir.join('ave.db').strpath
    app.config['WHOOSH_BASE_DIR'] = tmpdir.strpath
    cli_runner = CliRunner()
    fn = 'tests/data/A-AFFY-87.bb'

    result = cli_runner.invoke(cli, [
        'register',
        '--species', 'Solanum Lycopersicum',
        '--genome', 'SL.2.40',
        '--datatype', 'features',
        fn
    ])

    assert 'New datafile has been registered.' in result.output
    assert result.exit_code == 0
    whoosh_dir = tmpdir.join('SL.2.40-features').strpath
    assert whoosh_doc_count(whoosh_dir) == 81
    list_result = cli_runner.invoke(cli, ['list'])
    assert fn in list_result.output


def test_deregister_genes(tmpdir):
    app.config['DATABASE'] = tmpdir.join('ave.db').strpath
    app.config['WHOOSH_BASE_DIR'] = tmpdir.strpath
    cli_runner = CliRunner()
    fn = 'tests/data/S_lycopersicum_May_2012.chr6-0-100000.bb'
    cli_runner.invoke(cli, [
        'register',
        '--species', 'Solanum Lycopersicum',
        '--genome', 'SL.2.40',
        '--datatype', 'genes',
        fn
    ])

    result = cli_runner.invoke(cli, [
        'deregister',
        fn
    ])

    assert 'Deregistered entry' in result.output
    assert result.exit_code == 0
    whoosh_dir_is_removed = 'S_lycopersicum_May_2012.chr6-0-100000.bb' not in set(tmpdir.listdir())
    assert whoosh_dir_is_removed


def test_deregister_features(tmpdir):
    app.config['DATABASE'] = tmpdir.join('ave.db').strpath
    app.config['WHOOSH_BASE_DIR'] = tmpdir.strpath
    cli_runner = CliRunner()
    fn = 'tests/data/A-AFFY-87.bb'
    cli_runner.invoke(cli, [
        'register',
        '--species', 'Solanum Lycopersicum',
        '--genome', 'SL.2.40',
        '--datatype', 'features',
        fn
    ])

    result = cli_runner.invoke(cli, [
        'deregister',
        fn
    ])

    assert 'Deregistered entry' in result.output
    assert result.exit_code == 0
    whoosh_dir = tmpdir.join('SL.2.40-features').strpath
    assert whoosh_doc_count(whoosh_dir) == 0


def whoosh_doc_count(whoosh_dir):
    ix = open_dir(whoosh_dir)
    with ix.searcher() as searcher:
        doc_count = searcher.doc_count()
    ix.close()
    return doc_count
