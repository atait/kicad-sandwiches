""" Top level importer for multiple action plugin packages
"""
import sys, os
from kigadgets import kireload

if os.path.dirname(__file__) not in sys.path:
    sys.path.insert(0, os.path.dirname(__file__))


# Old style imports that do not reload when source changes or pcbnew is restarted
# import onepush
# import mousebite_kigadget
# import kisandwich
# import fillet
# import quick_reload

# New style import (first time) or forced reload (subsequent times)
# kireload('onepush')
# kireload('mousebite_kigadget')
kireload('kisandwich')
# kireload('fillet')
# kireload('quick_reload')