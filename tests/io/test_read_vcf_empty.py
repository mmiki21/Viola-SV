import viola
import pandas as pd
from io import StringIO

MANTA = """##fileformat=VCFv4.1
##variantcaller=manta
##contig=<ID=chr1,length=195471971>
##contig=<ID=chr2,length=182113224>
##contig=<ID=chr11,length=122082543>
##INFO=<ID=IMPRECISE,Number=0,Type=Flag,Description="Imprecise structural variation">
##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">
##INFO=<ID=SVLEN,Number=.,Type=Integer,Description="Difference in length between REF and ALT alleles">
##INFO=<ID=END,Number=1,Type=Integer,Description="End position of the variant described in this record">
##INFO=<ID=CIPOS,Number=2,Type=Integer,Description="Confidence interval around POS">
##INFO=<ID=CIEND,Number=2,Type=Integer,Description="Confidence interval around END">
##INFO=<ID=CIGAR,Number=A,Type=String,Description="CIGAR alignment for each alternate indel allele">
##INFO=<ID=MATEID,Number=.,Type=String,Description="ID of mate breakend">
##INFO=<ID=EVENT,Number=1,Type=String,Description="ID of event associated to breakend">
##INFO=<ID=HOMLEN,Number=.,Type=Integer,Description="Length of base pair identical homology at event breakpoints">
##INFO=<ID=HOMSEQ,Number=.,Type=String,Description="Sequence of base pair identical homology at event breakpoints">
##INFO=<ID=SVINSLEN,Number=.,Type=Integer,Description="Length of insertion">
##INFO=<ID=SVINSSEQ,Number=.,Type=String,Description="Sequence of insertion">
##INFO=<ID=LEFT_SVINSSEQ,Number=.,Type=String,Description="Known left side of insertion for an insertion of unknown length">
##INFO=<ID=RIGHT_SVINSSEQ,Number=.,Type=String,Description="Known right side of insertion for an insertion of unknown length">
##INFO=<ID=CONTIG,Number=1,Type=String,Description="Assembled contig sequence">
##INFO=<ID=BND_DEPTH,Number=1,Type=Integer,Description="Read depth at local translocation breakend">
##INFO=<ID=MATE_BND_DEPTH,Number=1,Type=Integer,Description="Read depth at remote translocation mate breakend">
##INFO=<ID=SOMATIC,Number=0,Type=Flag,Description="Somatic mutation">
##INFO=<ID=SOMATICSCORE,Number=1,Type=Integer,Description="Somatic variant quality score">
##INFO=<ID=JUNCTION_SOMATICSCORE,Number=1,Type=Integer,Description="If the SV junctino is part of an EVENT (ie. a multi-adjacency variant), this field provides the SOMATICSCORE value for the adjacency in question only">
##INFO=<ID=INV3,Number=0,Type=Flag,Description="Inversion breakends open 3' of reported location">
##INFO=<ID=INV5,Number=0,Type=Flag,Description="Inversion breakends open 5' of reported location">
##FORMAT=<ID=PR,Number=.,Type=Integer,Description="Spanning paired-read support for the ref and alt alleles in the order listed">
##FORMAT=<ID=SR,Number=.,Type=Integer,Description="Split reads for the ref and alt alleles in the order listed, for reads where P(allele|read)>0.999">
##FILTER=<ID=MaxDepth,Description="Normal sample site depth is greater than 3x the median chromosome depth near one or both variant breakends">
##FILTER=<ID=MinSomaticScore,Description="Somatic score is less than 30">
##FILTER=<ID=MaxMQ0Frac,Description="For a small variant (<1000 bases) in the normal sample, the fraction of reads with MAPQ0 around either breakend exceeds 0.4">
##ALT=<ID=INV,Description="Inversion">
##ALT=<ID=DEL,Description="Deletion">
##ALT=<ID=INS,Description="Insertion">
##ALT=<ID=DUP:TANDEM,Description="Tandem Duplication">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	sample1_N	sample1_T
"""
DELLY = """##fileformat=VCFv4.2
##FILTER=<ID=PASS,Description="All filters passed">
##fileDate=20201013
##ALT=<ID=DEL,Description="Deletion">
##ALT=<ID=DUP,Description="Duplication">
##ALT=<ID=INV,Description="Inversion">
##ALT=<ID=BND,Description="Translocation">
##ALT=<ID=INS,Description="Insertion">
##FILTER=<ID=LowQual,Description="Poor quality and insufficient number of PEs and SRs.">
##INFO=<ID=PRECISE,Number=0,Type=Flag,Description="Precise structural variation">
##INFO=<ID=IMPRECISE,Number=0,Type=Flag,Description="Imprecise structural variation">
##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">
##INFO=<ID=SVMETHOD,Number=1,Type=String,Description="Type of approach used to detect SV">
##INFO=<ID=END,Number=1,Type=Integer,Description="End position of the structural variant">
##INFO=<ID=CHR2,Number=1,Type=String,Description="Chromosome for POS2 coordinate in case of an inter-chromosomal translocation">
##INFO=<ID=POS2,Number=1,Type=Integer,Description="Genomic position for CHR2 in case of an inter-chromosomal translocation">
##INFO=<ID=PE,Number=1,Type=Integer,Description="Paired-end support of the structural variant">
##INFO=<ID=MAPQ,Number=1,Type=Integer,Description="Median mapping quality of paired-ends">
##INFO=<ID=CT,Number=1,Type=String,Description="Paired-end signature induced connection type">
##INFO=<ID=CIPOS,Number=2,Type=Integer,Description="PE confidence interval around POS">
##INFO=<ID=CIEND,Number=2,Type=Integer,Description="PE confidence interval around END">
##INFO=<ID=SRMAPQ,Number=1,Type=Integer,Description="Median mapping quality of split-reads">
##INFO=<ID=INSLEN,Number=1,Type=Integer,Description="Predicted length of the insertion">
##INFO=<ID=HOMLEN,Number=1,Type=Integer,Description="Predicted microhomology length using a max. edit distance of 2">
##INFO=<ID=SR,Number=1,Type=Integer,Description="Split-read support">
##INFO=<ID=SRQ,Number=1,Type=Float,Description="Split-read consensus alignment quality">
##INFO=<ID=CONSENSUS,Number=1,Type=String,Description="Split-read consensus sequence">
##INFO=<ID=CE,Number=1,Type=Float,Description="Consensus sequence entropy">
##INFO=<ID=RDRATIO,Number=1,Type=Float,Description="Read-depth ratio of tumor vs. normal.">
##INFO=<ID=SVLEN,Number=1,Type=Integer,Description="Insertion length for SVTYPE=INS.">
##INFO=<ID=SOMATIC,Number=0,Type=Flag,Description="Somatic structural variant.">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=GL,Number=G,Type=Float,Description="Log10-scaled genotype likelihoods for RR,RA,AA genotypes">
##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype Quality">
##FORMAT=<ID=FT,Number=1,Type=String,Description="Per-sample genotype filter">
##FORMAT=<ID=RC,Number=1,Type=Integer,Description="Raw high-quality read counts or base counts for the SV">
##FORMAT=<ID=RCL,Number=1,Type=Integer,Description="Raw high-quality read counts or base counts for the left control region">
##FORMAT=<ID=RCR,Number=1,Type=Integer,Description="Raw high-quality read counts or base counts for the right control region">
##FORMAT=<ID=CN,Number=1,Type=Integer,Description="Read-depth based copy-number estimate for autosomal sites">
##FORMAT=<ID=DR,Number=1,Type=Integer,Description="# high-quality reference pairs">
##FORMAT=<ID=DV,Number=1,Type=Integer,Description="# high-quality variant pairs">
##FORMAT=<ID=RR,Number=1,Type=Integer,Description="# high-quality reference junction reads">
##FORMAT=<ID=RV,Number=1,Type=Integer,Description="# high-quality variant junction reads">
##contig=<ID=chr10,length=130694993>
##contig=<ID=chr11,length=122082543>
##bcftools_viewVersion=1.8+htslib-1.8
##bcftools_viewCommand=view mouse1_filtered.bcf; Date=Wed Oct 14 15:37:56 2020
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	mouse01_T	mouse01_N
"""
LUMPY = """##fileformat=VCFv4.2
##source=LUMPY
##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">
##INFO=<ID=STRANDS,Number=.,Type=String,Description="Strand orientation of the adjacency in BEDPE format (DEL:+-, DUP:-+, INV:++/--)">
##INFO=<ID=SECONDARY,Number=0,Type=Flag,Description="Secondary breakend in a multi-line variants">
##INFO=<ID=EVENT,Number=1,Type=String,Description="ID of event associated to breakend">
##INFO=<ID=MATEID,Number=.,Type=String,Description="ID of mate breakends">
##INFO=<ID=SVLEN,Number=.,Type=Integer,Description="Difference in length between REF and ALT alleles">
##INFO=<ID=END,Number=1,Type=Integer,Description="End position of the variant described in this record">
##INFO=<ID=CIPOS,Number=2,Type=Integer,Description="Confidence interval around POS for imprecise variants">
##INFO=<ID=CIEND,Number=2,Type=Integer,Description="Confidence interval around END for imprecise variants">
##INFO=<ID=CIPOS95,Number=2,Type=Integer,Description="Confidence interval (95%) around POS for imprecise variants">
##INFO=<ID=CIEND95,Number=2,Type=Integer,Description="Confidence interval (95%) around END for imprecise variants">
##INFO=<ID=SU,Number=.,Type=Integer,Description="Number of pieces of evidence supporting the variant across all samples">
##INFO=<ID=PE,Number=.,Type=Integer,Description="Number of paired-end reads supporting the variant across all samples">
##INFO=<ID=SR,Number=.,Type=Integer,Description="Number of split reads supporting the variant across all samples">
##INFO=<ID=BD,Number=.,Type=Integer,Description="Amount of BED evidence supporting the variant across all samples">
##INFO=<ID=EV,Number=.,Type=String,Description="Type of LUMPY evidence contributing to the variant call">
##INFO=<ID=PRPOS,Number=.,Type=String,Description="LUMPY probability curve of the POS breakend">
##INFO=<ID=PREND,Number=.,Type=String,Description="LUMPY probability curve of the END breakend">
##ALT=<ID=DEL,Description="Deletion">
##ALT=<ID=DUP,Description="Duplication">
##ALT=<ID=INV,Description="Inversion">
##ALT=<ID=DUP:TANDEM,Description="Tandem duplication">
##ALT=<ID=INS,Description="Insertion of novel sequence">
##ALT=<ID=CNV,Description="Copy number variable region">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=SU,Number=1,Type=Integer,Description="Number of pieces of evidence supporting the variant">
##FORMAT=<ID=PE,Number=1,Type=Integer,Description="Number of paired-end reads supporting the variant">
##FORMAT=<ID=SR,Number=1,Type=Integer,Description="Number of split reads supporting the variant">
##FORMAT=<ID=BD,Number=1,Type=Integer,Description="Amount of BED evidence supporting the variant">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	1T	1N
"""
GRIDSS = """##fileformat=VCFv4.2
##gridssVersion=2.10.2-gridss
##contig=<ID=chr10,length=130694993>
##contig=<ID=chr11,length=122082543>
##contig=<ID=chr12,length=120129022>
##contig=<ID=chr13,length=120421639>
##contig=<ID=chr14,length=124902244>
##contig=<ID=chr15,length=104043685>
##contig=<ID=chr16,length=98207768>
##contig=<ID=chr17,length=94987271>
##contig=<ID=chr18,length=90702639>
##contig=<ID=chr19,length=61431566>
##contig=<ID=chr1,length=195471971>
##contig=<ID=chr2,length=182113224>
##contig=<ID=chr3,length=160039680>
##contig=<ID=chr4,length=156508116>
##contig=<ID=chr5,length=151834684>
##contig=<ID=chr6,length=149736546>
##contig=<ID=chr7,length=145441459>
##contig=<ID=chr8,length=129401213>
##contig=<ID=chr9,length=124595110>
##contig=<ID=chrM,length=16299>
##contig=<ID=chrX,length=171031299>
##contig=<ID=chrY,length=91744698>
##INFO=<ID=AS,Number=1,Type=Integer,Description="Count of assemblies supporting breakpoint">
##INFO=<ID=ASC,Number=1,Type=String,Description="CIGAR encoding assembly contig anchoring alignments. Local assemblies are excluded due to https://github.com/PapenfussLab/gridss/issues/213.">
##INFO=<ID=ASQ,Number=1,Type=Float,Description="Quality score of assemblies supporting breakpoint">
##INFO=<ID=ASRP,Number=1,Type=Integer,Description="Count of read pairs incorporated into any breakpoint assembly">
##INFO=<ID=ASSR,Number=1,Type=Integer,Description="Count of split, soft clipped or indel-containing reads incorporated into any breakpoint assemblies">
##INFO=<ID=BA,Number=1,Type=Integer,Description="Count of assemblies supporting just local breakend">
##INFO=<ID=BANRP,Number=1,Type=Integer,Description="Count of read pairs at this breakend assembled into a contig that does not support the breakpoint.">
##INFO=<ID=BANRPQ,Number=1,Type=Float,Description="Quality score of read pairs at this breakend assembled into a contig that does not support the breakpoint.">
##INFO=<ID=BANSR,Number=1,Type=Integer,Description="Count of split reads at this breakend assembled into a contig that does not support the breakpoint.">
##INFO=<ID=BANSRQ,Number=1,Type=Float,Description="Quality score of split reads at this breakend assembled into a contig that does not support the breakpoint.">
##INFO=<ID=BAQ,Number=1,Type=Float,Description="Quality score of assemblies supporting just local breakend">
##INFO=<ID=BASRP,Number=1,Type=Integer,Description="Count of read pairs incorporated into any breakend assembly">
##INFO=<ID=BASSR,Number=1,Type=Integer,Description="Count of split, soft clipped or indel-containing reads incorporated into any breakend assemblies">
##INFO=<ID=BEALN,Number=.,Type=String,Description="Potential alignment locations of breakend sequence in the format chr:start|strand|cigar|mapq. Depending on the alignment information available, strand and mapq may be empty.">
##INFO=<ID=BEID,Number=.,Type=String,Description="Identifiers of assemblies supporting the variant.">
##INFO=<ID=BEIDH,Number=.,Type=Integer,Description="Remote chimeric alignment offset of corresponding BEID assembly.">
##INFO=<ID=BEIDL,Number=.,Type=Integer,Description="Local chimeric alignment offset of corresponding BEID assembly.">
##INFO=<ID=BENAMES,Number=.,Type=String,Description="Read names of all reads providing direct breakend support.">
##INFO=<ID=BMQ,Number=1,Type=Float,Description="Mean MAPQ of breakend supporting reads.">
##INFO=<ID=BMQN,Number=1,Type=Float,Description="Minimum MAPQ of breakend supporting reads.">
##INFO=<ID=BMQX,Number=1,Type=Float,Description="Maximum MAPQ of breakend supporting reads.">
##INFO=<ID=BPNAMES,Number=.,Type=String,Description="Read names of all reads providing direct breakpoint support.">
##INFO=<ID=BQ,Number=1,Type=Float,Description="Quality score of breakend evidence">
##INFO=<ID=BSC,Number=1,Type=Integer,Description="Count of soft clips supporting just local breakend">
##INFO=<ID=BSCQ,Number=1,Type=Float,Description="Quality score of soft clips supporting just local breakend">
##INFO=<ID=BUM,Number=1,Type=Integer,Description="Count of read pairs (with one read unmapped) supporting just local breakend">
##INFO=<ID=BUMQ,Number=1,Type=Float,Description="Quality score of read pairs (with one read unmapped) supporting just local breakend">
##INFO=<ID=BVF,Number=1,Type=Integer,Description="Count of fragments providing breakend for the variant allele.">
##INFO=<ID=CAS,Number=1,Type=Integer,Description="Count of complex compound breakpoint assemblies supporting breakpoint from elsewhere">
##INFO=<ID=CASQ,Number=1,Type=Float,Description="Quality score of complex compound breakpoint assemblies supporting breakpoint from elsewhere">
##INFO=<ID=CIEND,Number=2,Type=Integer,Description="Confidence interval around END for imprecise variants">
##INFO=<ID=CIPOS,Number=2,Type=Integer,Description="Confidence interval around POS for imprecise variants">
##INFO=<ID=CIRPOS,Number=2,Type=Integer,Description="Confidence interval around remote breakend POS for imprecise variants">
##INFO=<ID=CQ,Number=1,Type=Float,Description="Breakpoint quality score before evidence reallocation">
##INFO=<ID=END,Number=1,Type=Integer,Description="Stop position of the interval">
##INFO=<ID=EVENT,Number=1,Type=String,Description="ID of event associated to breakend">
##INFO=<ID=HOMLEN,Number=.,Type=Integer,Description="Length of base pair identical micro-homology at event breakpoints">
##INFO=<ID=HOMSEQ,Number=.,Type=String,Description="Sequence of base pair identical micro-homology at event breakpoints">
##INFO=<ID=IC,Number=1,Type=Integer,Description="Count of read indels supporting breakpoint">
##INFO=<ID=IHOMPOS,Number=2,Type=Integer,Description="Position of inexact homology">
##INFO=<ID=IMPRECISE,Number=0,Type=Flag,Description="Imprecise structural variation">
##INFO=<ID=INSRM,Number=.,Type=String,Description="RepeatMasker classification of inserted sequence in the format of RepeatType#RepeatClass|repeat position|repeat orientation|insertion sequence CIGAR|repeat masker alignment score|edit distance to canonical repeat sequence. Edit distance may be blank.">
##INFO=<ID=INSRMP,Number=1,Type=Float,Description="Portion of inserted sequence whose alignment overlaps the repeatmasker repeat. 1.0 indicates the inserted sequence entirely mapping to the repeat.">
##INFO=<ID=INSRMRC,Number=1,Type=String,Description="Inserted sequence repeatmasker repeat class.">
##INFO=<ID=INSRMRO,Number=1,Type=String,Description="Inserted sequence repeatmasker repeat orientation.">
##INFO=<ID=INSRMRT,Number=1,Type=String,Description="Inserted sequence repeatmasker repeat type.">
##INFO=<ID=INSTAXID,Number=1,Type=Integer,Description="NCBI Taxonomy identifier for inserted sequence.">
##INFO=<ID=IQ,Number=1,Type=Float,Description="Quality score of read indels supporting breakpoint">
##INFO=<ID=MATEID,Number=.,Type=String,Description="ID of mate breakends">
##INFO=<ID=MQ,Number=1,Type=Float,Description="Mean MAPQ of breakpoint supporting reads.">
##INFO=<ID=MQN,Number=1,Type=Float,Description="Minimum MAPQ of breakpoint supporting reads.">
##INFO=<ID=MQX,Number=1,Type=Float,Description="Maximum MAPQ of breakpoint supporting reads.">
##INFO=<ID=RAS,Number=1,Type=Integer,Description="Count of assemblies supporting breakpoint from remote breakend">
##INFO=<ID=RASQ,Number=1,Type=Float,Description="Quality score of assemblies supporting breakpoint from remote breakend">
##INFO=<ID=REF,Number=1,Type=Integer,Description="Count of reads mapping across this breakend">
##INFO=<ID=REFPAIR,Number=1,Type=Integer,Description="Count of reference read pairs spanning this breakend supporting the reference allele">
##INFO=<ID=RF,Number=1,Type=Integer,Description="Reference fragments. Count of fragments supporting the reference allele and not the variant allele.">
##INFO=<ID=RP,Number=1,Type=Integer,Description="Count of read pairs supporting breakpoint">
##INFO=<ID=RPQ,Number=1,Type=Float,Description="Quality score of read pairs supporting breakpoint">
##INFO=<ID=RSI,Number=.,Type=Integer,Description="Support interval offsets of partner breakend.">
##INFO=<ID=SB,Number=1,Type=Float,Description="Strand bias of the reads supporting the variant. 1 indicates that reads would be aligned to the positive strand if the reference was changed to the variant allele. 0 indicates that reads bases would be aligned to the negative strand if the reference was changed to the variant allele. Strand bias is calculated purely from supporting reads and exclude read pair support since these are 100% strand bias. Note that reads both directly supporting the variant, and supporting via assembly will be double-counted. Both breakpoint and breakend supporting reads are included.">
##INFO=<ID=SC,Number=1,Type=String,Description="CIGAR for displaying anchoring alignment of any contributing evidence and microhomologies. Local assemblies are excluded due to https://github.com/PapenfussLab/gridss/issues/213">
##INFO=<ID=SELF,Number=0,Type=Flag,Description="Indicates a breakpoint is self-intersecting">
##INFO=<ID=SI,Number=.,Type=Integer,Description="Support interval offsets from breakend position in which at least one supporting read/read pair/assembly is mapped.">
##INFO=<ID=SR,Number=1,Type=Integer,Description="Count of split reads supporting breakpoint">
##INFO=<ID=SRQ,Number=1,Type=Float,Description="Quality score of split reads supporting breakpoint">
##INFO=<ID=SVLEN,Number=.,Type=Integer,Description="Difference in length between REF and ALT alleles">
##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">
##INFO=<ID=VF,Number=1,Type=Integer,Description="Count of fragments supporting the variant breakpoint allele and not the reference allele.">
##FORMAT=<ID=ASQ,Number=1,Type=Float,Description="Pro-rata quality score contribution of assemblies supporting breakpoint">
##FORMAT=<ID=ASRP,Number=1,Type=Integer,Description="Count of read pairs incorporated into any breakpoint assembly">
##FORMAT=<ID=ASSR,Number=1,Type=Integer,Description="Count of split, soft clipped or indel-containing reads incorporated into any breakpoint assemblies">
##FORMAT=<ID=BANRP,Number=1,Type=Integer,Description="Count of read pairs at this breakend assembled into a contig that does not support the breakpoint.">
##FORMAT=<ID=BANRPQ,Number=1,Type=Float,Description="Quality score of read pairs at this breakend assembled into a contig that does not support the breakpoint.">
##FORMAT=<ID=BANSR,Number=1,Type=Integer,Description="Count of split reads at this breakend assembled into a contig that does not support the breakpoint.">
##FORMAT=<ID=BANSRQ,Number=1,Type=Float,Description="Quality score of split reads at this breakend assembled into a contig that does not support the breakpoint.">
##FORMAT=<ID=BAQ,Number=1,Type=Float,Description="Pro-rata quality score contribution of assemblies supporting just local breakend">
##FORMAT=<ID=BASRP,Number=1,Type=Integer,Description="Count of read pairs incorporated into any breakend assembly">
##FORMAT=<ID=BASSR,Number=1,Type=Integer,Description="Count of split, soft clipped or indel-containing reads incorporated into any breakend assemblies">
##FORMAT=<ID=BQ,Number=1,Type=Float,Description="Quality score of breakend evidence after evidence reallocation">
##FORMAT=<ID=BSC,Number=1,Type=Integer,Description="Count of soft clips supporting just local breakend per category">
##FORMAT=<ID=BSCQ,Number=1,Type=Float,Description="Quality score of soft clips supporting just local breakend per category">
##FORMAT=<ID=BUM,Number=1,Type=Integer,Description="Count of read pairs (with one read unmapped) supporting just local breakend per category">
##FORMAT=<ID=BUMQ,Number=1,Type=Float,Description="Quality score of read pairs (with one read unmapped) supporting just local breakend per category">
##FORMAT=<ID=BVF,Number=1,Type=Integer,Description="Count of fragments providing breakend for the variant allele.">
##FORMAT=<ID=CASQ,Number=1,Type=Float,Description="Pro-rata quality score of complex compound breakpoint assemblies supporting breakpoint from elsewhere">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=IC,Number=1,Type=Integer,Description="Count of read indels supporting breakpoint per category">
##FORMAT=<ID=IQ,Number=1,Type=Float,Description="Quality score of read indels supporting breakpoint per category">
##FORMAT=<ID=QUAL,Number=1,Type=Float,Description="Quality score of breakend evidence after evidence reallocation">
##FORMAT=<ID=RASQ,Number=1,Type=Float,Description="Pro-rata quality score contribution of assemblies supporting breakpoint from remote breakend">
##FORMAT=<ID=REF,Number=1,Type=Integer,Description="Count of reads mapping across this breakend">
##FORMAT=<ID=REFPAIR,Number=1,Type=Integer,Description="Count of reference read pairs spanning this breakend supporting the reference allele">
##FORMAT=<ID=RF,Number=1,Type=Integer,Description="Reference fragments. Count of fragments supporting the reference allele and not the variant allele.">
##FORMAT=<ID=RP,Number=1,Type=Integer,Description="Count of read pairs supporting breakpoint per category">
##FORMAT=<ID=RPQ,Number=1,Type=Float,Description="Quality score of read pairs supporting breakpoint per category">
##FORMAT=<ID=SR,Number=1,Type=Integer,Description="Count of split reads supporting breakpoint per category">
##FORMAT=<ID=SRQ,Number=1,Type=Float,Description="Quality score of split reads supporting breakpoint per category">
##FORMAT=<ID=VF,Number=1,Type=Integer,Description="Count of fragments supporting the variant breakpoint allele and not the reference allele.">
##FILTER=<ID=ASSEMBLY_BIAS,Description="Mismatch between number of directly supporting reads and reads supporting via assembly.">
##FILTER=<ID=ASSEMBLY_ONLY,Description="Variant is supported only by assembly evidence.">
##FILTER=<ID=ASSEMBLY_TOO_FEW_READ,Description="Not enough reads contribute to this assembly as specified by 'assembly.minReads'">
##FILTER=<ID=ASSEMBLY_TOO_SHORT,Description="This assembly is shorter than a read length">
##FILTER=<ID=INSUFFICIENT_SUPPORT,Description="Does not reach the required threshold quality for calling as specified by 'variantcalling.minScore'">
##FILTER=<ID=LOW_QUAL,Description="Low quality call as specified by 'variantcalling.lowQuality'">
##FILTER=<ID=NO_ASSEMBLY,Description="No assembly supporting this variant could be found.">
##FILTER=<ID=NO_RP,Description="Variant does not have any direct read pair support.">
##FILTER=<ID=NO_SR,Description="Variant does not have any direct split read support.">
##FILTER=<ID=REF,Description="Breakpoint corresponds to reference allele">
##FILTER=<ID=SINGLE_ASSEMBLY,Description="Only one side of the breakpoint could be assembled.">
##FILTER=<ID=SINGLE_SUPPORT,Description="Supported by fewer than 'variantcalling.minReads' fragments">
##FILTER=<ID=SMALL_EVENT,Description="Event size is smaller than the minimum reportable size specified by 'variantcalling.minSize'">
##ALT=<ID=INV,Description="Inversion">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	mouse01_N	mouse01_T
"""

def test_read_vcf_empty_manta():
    vcf = viola.read_vcf(StringIO(MANTA))

def test_read_vcf_empty_delly():
    vcf = viola.read_vcf(StringIO(DELLY), variant_caller='delly')

def test_read_vcf_empty_lumpy():
    vcf = viola.read_vcf(StringIO(LUMPY), variant_caller='lumpy')

def test_read_vcf_empty_lumpy():
    vcf = viola.read_vcf(StringIO(GRIDSS), variant_caller='gridss')
    