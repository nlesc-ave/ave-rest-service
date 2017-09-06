table bed
"Gff3 converted with ggf2bed and bedToBigBed"
(
   string chrom;       "Reference sequence chromosome or scaffold"
   uint   chromStart;  "Start position in chromosome"
   uint   chromEnd;    "End position in chromosome"
   string name;        "Name of item."
   uint score;          "Score (0-1000)"
   char[1] strand;     "+ or - for strand"
   lstring source;	"Source of feature"
   lstring type;	"Type of feature"
   lstring phase;	"Phase of CDS feature"
   lstring attributes;	"Feature attributes"
)

