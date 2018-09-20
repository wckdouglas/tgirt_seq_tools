from __future__ import print_function
from sequencing_tools.bam_tools import bed_dedup 
from sequencing_tools.bam_tools import poisson_umi_tools



def test_fragment_group():
    fg = bed_dedup.fragment_group('chr1','10000', '20000', '+','ACT','')
    fg.add_member('ACT','')
    fg.add_member('ACG','')
    assert(not fg.check_fragment('chr1','10000','20000','-'))

    max_c = fg.demultiplexing_barcodes(0)
    assert(max_c == 2)

    expected = ['chr1\t10000\t20000\tACG_1_members\t10000\t+',
                 'chr1\t10000\t20000\tACT_2_members\t10000\t+']
    expected.sort()
    out = fg.output_bed_line()
    assert(out == (2,3))


    max_c =  fg.demultiplexing_barcodes(1)
    print(fg.get_unique_umi())
    assert(len(fg.get_unique_umi()) == 1)
    assert(max_c ==3)
    expected = ['chr1\t10000\t20000\tACT_3_members\t10000\t+', 
            'chr1\t10000\t20000\tACG_3_members\t10000\t+']
    out = fg.output_bed_line()
    assert(out == (1,3))

    

def test_umi():
    import os
    import sys
    import string
    f = open(os.devnull, 'w')
    test_fragment = poisson_umi_tools.fragment('chr1','1000','2000','-', 'AAA')
    for s in string.ascii_letters:
        test_fragment.add_fragment(s * 3)
    assert(test_fragment.output_fragments(umi_nt = 3, out_file = f) == 107)
    assert(test_fragment.output_fragments(umi_nt = 5, out_file = f) == 53)


