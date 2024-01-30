import os
import pytest
# Tell lytest about out layouts
import lytest
# lytest.kdb_xor.run_xor = lytest.kdb_xor.run_xor_pcbnew
lytest.utest_buds.default_file_ext = '.kicad_pcb'
lytest.utest_buds.test_root = os.path.dirname(__file__)
lytest.utest_buds.get_src_dir()
