#!/usr/bin/env python

import pyximport
import pysam
pyximport.install(setup_args={'include_dirs':pysam.get_include()})
import argparse
from tgirt_seq_tools.fragment_pairs import bam_to_bed
import sys


def getopt():
    parser = argparse.ArgumentParser(description = 'Making paired-end bam into bed file for every fragment')
    parser.add_argument('-i', '--in_bam', required=True,
                        help = 'BAM file name, or stdin (-) ** name sorted' )
    parser.add_argument('-o','--out_bed', default='-', help = 'BED file output (default: - )')
    parser.add_argument('-m','--min_size', default=10, type=int,
                        help = 'minimum fragment size to report')
    parser.add_argument('-M','--max_size', default=10000, type=int,
                        help = 'minimum fragment size to report')
    parser.add_argument('-t','--tag', default=None,
                        help = 'tag to extract')

    return parser.parse_args()

def main():
    args = getopt()
    in_bam = args.in_bam
    out_file = sys.stdout if args.out_bed == '-' else open(args.out_bed, 'w')
    tag = args.tag
    if args.max_size <= args.min_size:
        sys.exit('!!!!! Min fragment size > Max fragment size') 
    bam_to_bed(in_bam, out_file, args.min_size, args.max_size, tag)
    return 0

if __name__ == '__main__':
    main()
