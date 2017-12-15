#!/usr/bin/env python

from __future__ import print_function
import numpy as np
import argparse
import pysam
import sys
from functools import partial
from sequencing_tools.unique_bam import filter_bam_single_end, filter_bam_pair_end

def getopt():
    parser = argparse.ArgumentParser(description = 'Filter alignments from sam file by softclip ratio')
    parser.add_argument('-i', '--inbam', required=True, help = 'input bam file (can be stdin, use -)')
    parser.add_argument('-o','--outbam', default = '-', help = 'output bam file (default: - )')
    parser.add_argument('-s','--single_end',default = 0.2, type=float,
                        help ='Maximum ratio of the whole alignment being clipped in one end (default: 0.2)')
    parser.add_argument('-b','--both_end',default = 0.5, type=float,
                        help ='Maximum ratio of the whole alignment being clipped in sum(each end) (default : 0.5)')
    parser.add_argument('-v','--inverse', action = 'store_true',
                        help ='Only output alignment with clipped base > threshold (like grep -v)')
    parser.add_argument('--pe', action = 'store_true',
                        help ='Paired end input')
    args = parser.parse_args()
    return args

def main():
    args = getopt()
    in_bam = args.inbam
    out_bam = args.outbam
    single_end_thresh = args.single_end
    both_end_thresh = args.both_end
    print('Filtering %s' %in_bam, file = sys.stderr)


    if args.pe:
        filter_bam_func = partial(filter_bam_pair_end)   
        unit = 'alignment pairs'
    else:
        filter_bam_func = partial(filter_bam_single_end)
        unit = 'alignments'
    output_count, in_count = filter_bam_func(in_bam, out_bam, single_end_thresh, both_end_thresh, args.inverse)
    print('Written %i from %i %s to %s' %(output_count, in_count, unit, out_bam), file = sys.stderr)

if __name__ == '__main__':
    main()
