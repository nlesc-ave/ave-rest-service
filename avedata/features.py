import os
from urllib.parse import urlparse

from whoosh.index import create_in, open_dir
from whoosh import analysis
import whoosh.fields as wf
from whoosh.qparser import MultifieldParser
from pybedtools.contrib.bigbed import bigbed_to_bed

analyzer = analysis.NgramWordAnalyzer(minsize=3)
schema = wf.Schema(chrom=wf.ID(stored=True),
                   start=wf.NUMERIC(int, stored=True, signed=False),
                   end=wf.NUMERIC(int, stored=True, signed=False),
                   track=wf.ID(stored=True),
                   attributes=wf.TEXT(analyzer=analyzer, stored=True),
                   name=wf.TEXT(analyzer=analyzer, stored=True))


def featurebb2label(url):
    return os.path.splitext(os.path.split(urlparse(url).path)[-1])[0]


def features_2_whoosh(url, whoosh_dir):
    try:
        os.mkdir(whoosh_dir)
    except FileExistsError:
        pass
    ix = create_in(whoosh_dir, schema)
    writer = ix.writer()
    bed = bigbed_to_bed(url)

    track = featurebb2label(url)
    for feature in bed:
        fields = feature.fields
        writer.add_document(chrom=fields[0],
                            start=fields[1],
                            end=fields[2],
                            name=fields[3],
                            track=track,
                            attributes=fields[9])
    writer.commit()
    ix.close()


def map_hit(r):
    h = dict(r)
    h['start'] = int(h['start'])
    h['end'] = int(h['end'])
    return h


def find_features(whoosh_dir, query):
    ix = open_dir(whoosh_dir)
    with ix.searcher() as searcher:
        whoosh_query = MultifieldParser(["name", "attributes"], ix.schema).parse(query)
        whoosh_results = searcher.search(whoosh_query)
        ix.close()
        return [map_hit(r) for r in whoosh_results]
