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
        'This is kicad-sandwiches, the one-push macro script. '
        'Edit the script directly at \n\n{}\n\n'
        'Use it to develop your own code without '
        'having to restart pcbnew every time.'.format(__file__)
    )
default()  # Comment this line when ready to run your own code below

### the most basic test that paths and links and board loading are working correctly
def hello_world():
    import pcbnew
    notify("One push hello world")
    board = pcbnew.GetBoard()
    textobj = pcbnew.TEXTE_PCB(board)
    textobj.SetPosition(pcbnew.wxPoint(pcbnew.FromMils(0), pcbnew.FromMils(0)))
    textobj.SetText('One push hello world')
    textobj.SetLayer(pcbnew.Cmts_User)
    board.Add(textobj)
# hello_world()



#### some tests of kicad-python

# Verify autoreloading
def test_autoreload():
    from kicad.pcbnew.board import Board
    pcb = Board.from_editor()
    try:
        notify(pcb.temporary_attribute)
    except AttributeError:
        notify(
'''
Add the attribute to kicad.pcbnew.board:Board at this line:

class Board(object):
    temporary_attribute = 'hey there'
    def __init__(self, wrap=None):
'''
        )
# test_autoreload()

# get a module already present and move it
def move_footprint():
    from kicad.pcbnew.board import Board
    pcb = Board.from_editor()
    mod = pcb.moduleByRef('D1')
    mod.position = (50, 30)
# move_footprint()

# # add test track with via
# track1 = [(30, 26), (30, 50), (60, 80)]
# track2 = [(60, 80), (80, 80)]
# pcb.add_track(track1, layer='F.Cu', width=0.25)
# pcb.add_track(track2, layer='B.Cu')
# from kicad.pcbnew.via import Via
# pcb.add(Via(track1[-1], ['F.Cu', 'B.Cu'], 1, .5, board=pcb))

# # add board edge
# ul = (20, 20)
# pcb_size = (100, 80)
# edge = [ul,
#         (ul[0], ul[1]+pcb_size[1]),
#         (ul[0]+pcb_size[0], ul[1]+pcb_size[1]),
#         (ul[0]+pcb_size[0], ul[1]),
#         ul]
# pcb.add_polyline(edge, layer='Edge.Cuts')

#### Reload main window
import pcbnew
pcbnew.Refresh()

# time.sleep(2)

# for elem in removed:
#     pcb.add(elem)
# pcbnew.Refresh()


