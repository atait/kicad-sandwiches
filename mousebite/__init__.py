import sys, os
sys.path.append(os.path.dirname(__file__))

from .action_mousebite import MouseBite
MouseBite().register() # Instantiate and register to Pcbnew

