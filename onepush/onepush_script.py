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
import setup_pcbnew_coding_alex  # setup paths
from importlib import reload
import time

### the most basic test of paths and links working correctly
def most_basic_test():
    import pcbnew
    print("Testing onepush")
    board = pcbnew.GetBoard()
    textobj = pcbnew.TEXTE_PCB(board)
    textobj.SetPosition(pcbnew.wxPoint(pcbnew.FromMils(2000), pcbnew.FromMils(1000)))
    textobj.SetText('Testing onepush')
    textobj.SetLayer(pcbnew.Cmts_User)
    board.Add(textobj)
# most_basic_test()
###


#### communicate with the user
import wx
def notify(text):
    text = str(text)
    dialog = wx.MessageDialog(None, text, 'One Push debug output', wx.OK)
    sg = dialog.ShowModal()
    return sg
# test it
# notify('heyooo thereo')
# notify('heyoee again')

#### some tests of kicad-python
import kicad
from kicad.pcbnew import drawing, module, board, layer
reload(kicad)
reload(drawing)
reload(module)
reload(board)
from kicad.pcbnew.layer import Layer
from kicad.pcbnew.board import Board
pcb = Board.from_editor()

# # These have to do with editing modules
# # mod = pcb.add_module('test')
# # modline = drawing.Segment(start=(-8, 0), end=(8, 0), width=0.2, layer='F.SilkS', board=mod)
# # mod.add_line(start=(-8, 0), end=(8, 0), layer='F.SilkS', width=0.2)
# # mod.add(modline)
# # modarc = drawing.Arc([0, 0], 6, start_angle=0, stop_angle=180, layer='F.Cu', width=0.15, board=pcb)
# # mod.add(modarc)
# # m.add_pad(position=(-4, -3), size=2, drill=1)
# # m.add_pad(position=(4, -3), size=2, drill=1, layers=['B.Cu', 'F.Cu'])
# # for n, x in enumerate([-1, -.5, 0, .5, 1]):
# #     m.add_pad(position=(x, -4), size=(0.25, 1.2), name=n, pad_type='smd', shape='rect')

# # get a module already present and move it
# mod = pcb.moduleByRef('U1')
# mod.position = (50, 30)

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

#### Reload footprints
import pcbnew
pcbnew.Refresh()

# time.sleep(2)

# for elem in removed:
#     pcb.add(elem)
# pcbnew.Refresh()


