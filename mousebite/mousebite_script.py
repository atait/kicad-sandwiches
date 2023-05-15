''' Do you hate the pcbnew console? Me too.
    This script can be run at the press of a button in the Pcbnew GUI. Great for semi-interactive coding
    It uses a plugin entry point, which can be hotkeyed.

    Usage:
    - write stuff below
    - in Pcbnew, press Cmd+Enter

    Setup:
    1) register an entry point. I have already done this for you. It's called onepush_plugin.py
        - it is an external plugin and should show up in your Pcbnew menu
        - it just has to register the right name and find this file
    2) shortcut it in System Preferences (OSX)
        - keyboard > shortcuts
        - pick Application shortcuts from the menu
        - hit plus button, scroll to "Other..." at the bottom of the dropdown menu
        - find "kicad.app" within the KiCAD folder
        - enter the menu item name (One Push) and key combo (for me, Cmd+Enter)
        - repeat for the "pcbnew.app" in case you run that as standalone

    Notes:
    The python kernel persists while Pcbnew is open.
    - if you import another module, it will not run again.
    - attributes changed in that module will not reset.
    - if you had edited that module, stuff can get weird.
    - to reinit that module, use "reload(that_module)"
    The entry point will reload this script, thus reinitializing and running it every time
'''
from atait_scripting_support import reload, notify
import sys
import time

def default():
    notify(
        'This is kicad-sandwiches, the mousebite macro. '
        'Edit the script directly at \n\n{}\n\n'.format(__file__)
    )
# default()  # Comment this line when ready to run your own code below

from kicad.pcbnew.board import Board
pcb = Board.from_editor()

dwgs = []
for draw in pcb.drawings:
    dwgs.append(draw)
# notify('\n'.join(str(dw) for dw in dwgs))

eco_dwgs = [dw for dw in dwgs if dw.layer == 'User.Eco1']
edge_dwgs = [dw for dw in dwgs if dw.layer == 'Edge.Cuts']

# notify(f'Found {len(eco_dwgs)} eco drawings')

bbs = []
for dwg in eco_dwgs:
    bbs.append(dwg._obj.GetBoundingBox())
# notify(bbs)
coo = []
for bb in bbs:
    top = bb.GetTop() / 1e6
    bottom = bb.GetBottom() / 1e6
    left = bb.GetLeft() / 1e6
    right = bb.GetRight() / 1e6
    coords = (top, bottom, left, right)
    coo.append(coords)
# notify('\n'.join(str(co) for co in coo))
matches = []
for bb in bbs:
    matches.append([])
    for edge in edge_dwgs:
        if bb.Intersects(edge._obj):
            matches[-1].append((bb, edge))
notify(matches)
