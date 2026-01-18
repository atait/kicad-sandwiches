import os
import pytest
from lytest.utest_buds import get_src_dir
from lytest import contained_pcbnewBoard, contained_script, difftest_it

import kisandwich
from kisandwich.core import sandwich_from_file
from kisandwich import objview

proc_opts = objview(
    # enable = objview(tracks=True, drawings=True, modules=True, vias=True, zones=True, stencil=True),
    sandwich_type = 'inside',
    n_boards = 2,
    # stencil = objview(fill_ratio=1.0),
    # vias = objview(coverage_ratio=1.0, shrink=True),
    # zones = objview(remove_keepouts=True),
    # drawings = objview(bond_masks=False),
)

@contained_script
def sandwich2_LOW():
    infile = os.path.join(get_src_dir(), 'sandwich-example.kicad_pcb')
    from kigadgets.board import Board
    pcb1 = Board.load(infile)
    outfile = os.path.join(get_src_dir(), 'sandwich-example-temp.kicad_pcb')
    sandwich_from_file(infile, which_one='LOW', outfile=outfile, proc_opts=proc_opts)
    pcb2 = Board.load(outfile)
    # breakpoint()
    return outfile

# @pytest.mark.skip('Working but lytest is not loading!?')
def test_sandwich2_LOW(): difftest_it(sandwich2_LOW)()

@contained_script
def sandwich2_TOP():
    infile = os.path.join(get_src_dir(), 'sandwich-example.kicad_pcb')
    outfile = os.path.join(get_src_dir(), 'sandwich-example-temp2.kicad_pcb')
    sandwich_from_file(infile, which_one='TOP', outfile=outfile, proc_opts=proc_opts)
    return outfile

# @pytest.mark.skip('Working but lytest is not loading!?')
def test_sandwich2_TOP(): difftest_it(sandwich2_TOP)()
