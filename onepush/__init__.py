import sys, os
sys.path.append(os.path.dirname(__file__))

from .action_onepush import OnePush
OnePush().register() # Instantiate and register to Pcbnew

