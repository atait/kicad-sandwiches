import sys, os
sys.path.append(os.path.dirname(__file__))

from .action_fillet import Fillet
Fillet().register() # Instantiate and register to Pcbnew

