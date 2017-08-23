from whoosh.index import create_in
import whoosh.fields as wf
from pybedtools.contrib.bigbed import bigbed_to_bed
import os

schema = wf.Schema(chrom=wf.ID(stored=True),
                   start=wf.ID(stored=True),
                   end=wf.ID(stored=True),
                   id=wf.TEXT(stored=True),
                   gene_id=wf.TEXT(stored=True),
                   name=wf.TEXT(stored=True))

def big_bed_2_whoosh(filename, whoosh_dir):
    os.mkdir(whoosh_dir)
    ix = create_in(whoosh_dir, schema)
    writer = ix.writer()
    bed = bigbed_to_bed(filename)
    for transcript in bed:
        fields = transcript.fields
        writer.add_document(chrom = fields[0],
                            start = fields[1],
                            end = fields[2],
                            id = fields[3],
                            gene_id = fields[12],
                            name = fields[13])
    writer.commit()
    ix.close()
