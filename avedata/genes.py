import os

from whoosh.index import create_in, open_dir
from whoosh import analysis
import whoosh.fields as wf
from whoosh.qparser import MultifieldParser
from pybedtools.contrib.bigbed import bigbed_to_bed

analyzer = analysis.NgramWordAnalyzer(minsize=3)
schema = wf.Schema(chrom=wf.ID(stored=True),
                   start=wf.ID(stored=True),
                   end=wf.ID(stored=True),
                   id=wf.TEXT(analyzer=analyzer, stored=True),
                   gene_id=wf.TEXT(analyzer=analyzer, stored=True),
                   name=wf.TEXT(analyzer=analyzer, stored=True))


def genes_2_whoosh(filename, whoosh_dir):
    os.mkdir(whoosh_dir)
    ix = create_in(whoosh_dir, schema)
    writer = ix.writer()
    bed = bigbed_to_bed(filename)
    for transcript in bed:
        fields = transcript.fields
        writer.add_document(chrom=fields[0],
                            start=fields[1],
                            end=fields[2],
                            id=fields[3],
                            gene_id=fields[12],
                            name=fields[13])
    writer.commit()
    ix.close()


def map_hit(r):
    h = dict(r)
    h['start'] = int(h['start'])
    h['end'] = int(h['end'])
    return h


def find_genes(whoosh_dir, query):
    ix = open_dir(whoosh_dir, readonly=True)
    with ix.searcher() as searcher:
        whoosh_query = MultifieldParser(["gene_id", "id", "name"], ix.schema).parse(query)
        whoosh_results = searcher.search(whoosh_query)
        ix.close()
        return [map_hit(r) for r in whoosh_results]
