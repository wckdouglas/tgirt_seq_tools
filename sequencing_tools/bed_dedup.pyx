from __future__ import print_function
import sys
import fileinput 
from operator import itemgetter
from itertools import combinations
from functools import partial
from collections import Counter, defaultdict
from networkx import Graph, connected_components
import sys
from numba import jit


class fragment_group:

    def __init__(self, chrom, start, end, strand, bc):
        self.chrom = chrom
        self.start = start
        self.end = end
        self.strand = strand
        self.fragment_size = long(self.end) - long(self.start)

        self.barcodes_set = defaultdict(int)
        self.unique_barcodes = None
        self.barcode_counter = None

        # add first record
        self.barcodes_set[bc] += 1

    def add_member(self, bc):
        self.barcodes_set[bc] += 1


    def demultiplexing_barcodes(self, threshold):
        if len(self.barcodes_set.keys()) == 1:
            self.unique_barcodes = ['{barcode}_{count}_members'.format(barcode=self.barcodes_set.keys()[0], 
                                                                count = self.barcodes_set.values()[0])]
        else:
            self.unique_barcodes = demultiplex(self.barcodes_set, threshold)


    def output_bed_line(self):
        for barcode in self.unique_barcodes:
            template = '{chrom}\t{start}\t{end}\t{barcode}\t{length}\t{strand}' \
                .format(chrom = self.chrom,
                    start = self.start,
                    end = self.end,
                    barcode = barcode,
                    length = self.fragment_size,
                    strand= self.strand)
            yield template

    def check_fragment(self, chrom, start, end, strand):
        chrom_same = (chrom == self.chrom)
        start_end_same = (start == self.start and end == self.end)
        strand_same = (strand == self.strand)
        return chrom_same and start_end_same and strand_same


cdef int hamming_barcode(barcode_pair):
    cdef:
        str a, b
        str i, j
        int hd

    a, b = barcode_pair
    assert len(a) == len(b), 'Wrong barcode extraction'
    hd = 0
    for i, j in zip(a, b):
        if i != j:
            hd += 1
    return hd

def make_graph(comparison, threshold):
    '''
    Using a graph to connect all umi with <= threshold mismatches
    '''
    G = Graph()
    for pair in comparison:
        if hamming_barcode(pair) <= threshold:
            G.add_edge(pair[0],pair[1])
        else:
            G.add_node(pair[0])
            G.add_node(pair[1])
    return G

def unique_barcode_from_graph(graph, barcodes):
    '''
    '''
    unique_barcode = []
    for subgraph in connected_components(graph):
        subgraph = list(subgraph)
        if len(subgraph) == 1:
            barcode_id = subgraph[0]
            member_counts = barcodes[barcode_id]
            barcode_id = barcode_id + '_' + str(member_counts) + '_members'
        else:
            member_counts = sum(barcodes[bc] for bc in subgraph)
            barcode_id = subgraph[0] + '_' + str(member_counts) + '_members'
        unique_barcode.append(barcode_id)
    return unique_barcode

def demultiplex(barcodes, threshold):
    comparison = combinations(barcodes.keys(),r=2)
    graph = make_graph(comparison, threshold)
    unique_barcode =  unique_barcode_from_graph(graph, barcodes)
    #print 'In: %i, out: %i' %(len(barcodes), len(unique_barcode))
    return unique_barcode



def dedup_bed(in_file_handle, out_file_handle, threshold, str delim, int f):
    cdef:
        str line, bc, read_name, chrom, start, end, strand
        str bc_line
        int in_count
        int out_count = 0

    barcode_group = None
    for in_count, line in enumerate(in_file_handle):
        fields = line.strip().split('\t')
        read_name = fields[3]
        bc = read_name.split(delim)[f]
        chrom, start, end, strand = itemgetter(0,1,2,5)(fields)
        if not barcode_group:
            '''
            if no initial barcode group, initilize one
            '''
            barcode_group = fragment_group(chrom, start, end, strand, bc)

        elif barcode_group.check_fragment(chrom, start, end, strand):
            '''
            add member if same chrom, start, end & strand
            '''
            barcode_group.add_member(bc)

        else:
            '''
            summarize previous group and
            initialize new fragment group if not same coordinate
            '''
            barcode_group.demultiplexing_barcodes(threshold)
            for bc_line in barcode_group.output_bed_line():
                print(bc_line, file=out_file_handle)
                out_count += 1

            barcode_group = fragment_group(chrom, start, end, strand, bc)

    # output the last group
    barcode_group.demultiplexing_barcodes(threshold)
    for bc_line in barcode_group.output_bed_line():
        print(bc_line, file=out_file_handle)
        out_count += 1

    print('Iput %i lines, output %i lines' %(in_count + 1, out_count), file=sys.stderr)
    return 0