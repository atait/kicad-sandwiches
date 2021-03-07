from atait_scripting_support import reload, notify
import os

import pcbnew
import kicad
from kicad.pcbnew import drawing, module, board, layer
from kicad.pcbnew.layer import Layer
from kicad.pcbnew.board import Board
from kisandwich import objview
import kisandwich.core as core


# Method 2
map_copper3 = dict()
map_copper3['TOP', 'inside'] = {
    'F.Cu': None,
    'In1.Cu': None,
    'In2.Cu': None,
    'In3.Cu': None,
    'In4.Cu': 'F.Cu',
    'B.Cu': 'B.Cu',
}
map_copper3['MID', 'inside'] = {
    'F.Cu': None,
    'In1.Cu': None,
    'In2.Cu': 'B.Cu',
    'In3.Cu': 'F.Cu',
    'In4.Cu': None,
    'B.Cu': None,
}  # mid is the decorative/structural board
map_copper3['LOW', 'inside'] = {
    'F.Cu': 'F.Cu',
    'In1.Cu': 'B.Cu',
    'In2.Cu': None,
    'In3.Cu': None,
    'In4.Cu': None,
    'B.Cu': None,
}
map_copper3[('TOP', 'outside')] = map_copper3['LOW', 'inside']
map_copper3[('LOW', 'outside')] = map_copper3['TOP', 'inside']
map_copper3[('MID', 'outside')] = {  # except flip it
    'F.Cu': None,
    'In1.Cu': None,
    'In2.Cu': 'F.Cu',
    'In3.Cu': 'B.Cu',
    'In4.Cu': None,
    'B.Cu': None,
}


def process_vias3(pcb, which_one='LOW', proc_opts=None):
    ''' 1. Turn through vias into bonding pads. They really cannot be tented (i.e. with mask opening)
        2. Convert vias to internal layers into through vias. They can be tented.
        Argument units in mm and pertain only to bonding pads
    '''
    sandwich_type = proc_opts.sandwich_type
    coverage_ratio = proc_opts.vias.coverage_ratio
    diameter_override = proc_opts.vias.get('diameter_override', None)
    diameter_minimum = proc_opts.vias.get('diameter_minimum', None)
    drill_override = proc_opts.vias.get('drill_override', None)
    drill_minimum = proc_opts.vias.get('drill_minimum', None)
    shrink_outside = proc_opts.vias.get('shrink', True)
    assert diameter_override is None or diameter_minimum is None
    assert drill_override is None or drill_minimum is None

    for via in pcb.vias:
        # Bond pad cases
        make_pad = False
        if via._obj.GetViaType() in [pcbnew.VIA_MICROVIA, pcbnew.VIA_BLIND_BURIED]:
            to_midboard = (
                via.top_layer in {'In2.Cu', 'In3.Cu'}
                or via.bottom_layer in {'In2.Cu', 'In3.Cu'}
            )
            to_frontboard = (
                via.top_layer in {'In1.Cu', 'F.Cu'}
                or via.bottom_layer in {'In1.Cu', 'F.Cu'}
            )
            to_backboard = (
                via.top_layer in {'In4.Cu', 'B.Cu'}
                or via.bottom_layer in {'In4.Cu', 'B.Cu'}
            )

            # Simple pad to the decorative board
            if to_midboard and (to_frontboard or to_backboard):
                make_pad = True
                if to_frontboard ^ (sandwich_type == 'inside'):
                    if which_one == 'MID':
                        to_mask = ['F']
                    elif which_one == 'TOP':
                        to_mask = ['B']
                    elif which_one == 'LOW':
                        pcb.remove(via)
                        continue
                if to_backboard ^ (sandwich_type == 'inside'):
                    if which_one == 'MID':
                        to_mask = ['B']
                    elif which_one == 'TOP':
                        pcb.remove(via)
                        continue
                    elif which_one == 'LOW':
                        to_mask = ['F']

        elif via._obj.GetViaType() == pcbnew.VIA_THROUGH:
            # Bond pad through everything
            make_pad = True
            if which_one == 'LOW':
                to_mask = ['F']
            elif which_one == 'TOP':
                to_mask = ['B']
            elif which_one == 'MID':
                to_mask = ['F', 'B']

        # Make the pads
        if make_pad:
            if diameter_override is not None:
                via.diameter = diameter_override
            elif diameter_minimum is not None:
                via.diameter = max(via.diameter, diameter_minimum)
            if drill_override is not None:
                via.drill = drill_override
            elif drill_minimum is not None:
                via.drill = max(via.drill, drill_minimum)
            via._obj.SetViaType(pcbnew.VIA_THROUGH)

            opening_radius = coverage_ratio * via.diameter / 4
            opening_width = 2 * opening_radius
            if shrink_outside:
                via.diameter = via.drill * 1.05

            for mask_side in to_mask:
                pcb.add_circle(
                    via.center,
                    opening_radius,
                    mask_side + '.Mask',
                    opening_width)
                if shrink_outside:
                    pcb.add_circle(
                        via.center,
                        opening_radius,
                        mask_side + '.Cu',
                        opening_width)
            continue


        # Turn blind vias into regular vias. Delete ones in wrong layers
        if via._obj.GetViaType() in [pcbnew.VIA_MICROVIA, pcbnew.VIA_BLIND_BURIED]:
            toplayer = map_copper3[which_one, sandwich_type].get(via.top_layer, via.top_layer)
            if toplayer is None:
                pcb.remove(via)
            else:
                via.top_layer = toplayer
                via._obj.SetViaType(pcbnew.VIA_THROUGH)

            bottomlayer = map_copper3[which_one, sandwich_type].get(via.bottom_layer, via.bottom_layer)
            if bottomlayer is None:
                pcb.remove(via)
            else:
                via.bottom_layer = bottomlayer
                via._obj.SetViaType(pcbnew.VIA_THROUGH)


def transmute_module_cuts(mod, which_one='LOW', flipped=False):
    ''' Change Eco1, Eco2, and Margin to Edge.Cuts or delete, depending on which board
    '''
    if flipped:
        which_one = {'LOW': 'TOP', 'TOP': 'LOW', 'MID': 'MID'}[which_one]
    the_map = core.map_edges[which_one]
    for dw in mod.graphicalItems:
        dw_layer = the_map.get(dw.layer, dw.layer)
        if dw_layer is None:
            mod.remove(dw)
        else:
            dw.layer = dw_layer


def process_modules3(pcb, which_one='LOW', proc_opts=None):
    '''Use KISANDWICH-MIDBOARD in the value to designate footprint on the middle board
        Use KISANDWICH-CUTTER to designate that drawings should be turned into cuts
    '''
    for mod in pcb.modules:
        # cutter modules
        if mod.value.startswith('KISANDWICH-CUTTER'):
            flipped = (mod.layer == Layer.Back)
            transmute_module_cuts(mod, which_one, flipped)
            continue  # never delete this module
        # midboard modules that can be on either layer
        elif mod.value.startswith('KISANDWICH-MIDBOARD'):
            if which_one != 'MID':
                pcb.remove(mod)
            else:
                continue  # keep it regardless of side, if we are doing the middle board
        elif which_one == 'MID':
            pcb.remove(mod)
        # regular modules whose layer determines which board to go on
        else:
            if (
                (which_one == 'LOW')
                ^ (proc_opts.sandwich_type == 'inside')
                ^ (mod.layer == Layer.Back)
            ):
                pcb.remove(mod)
