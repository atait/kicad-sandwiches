from atait_scripting_support import reload, notify
import os

import pcbnew
import kicad
from kicad.pcbnew import drawing, module, board, layer
from kicad.pcbnew.layer import Layer
from kicad.pcbnew.board import Board
from kisandwich import objview
import kisandwich.core as core


# Method 1. Method 2 is the same except mid and top are switched
# map_copper = dict()
# map_copper['TOP', 'inside'] = {
#     'F.Cu': None,
#     'In1.Cu': None,
#     'In2.Cu': 'F.Cu',
#     'In3.Cu': 'B.Cu',
#     'In4.Cu': None,
#     'B.Cu': None,
# }  # top is the decorative board
# map_copper['MID', 'inside'] = {
#     'F.Cu': None,
#     'In1.Cu': None,
#     'In2.Cu': None,
#     'In4.Cu': None,
#     'In4.Cu': 'F.Cu',
#     'B.Cu': 'B.Cu',
# }
# map_copper['LOW', 'inside'] = {
#     'F.Cu': 'F.Cu',
#     'In1.Cu': 'B.Cu',
#     'In2.Cu': None,
#     'In3.Cu': None,
#     'In4.Cu': None,
#     'B.Cu': None,
# }

# Method 2
map_copper = dict()
map_copper['TOP', 'inside'] = {
    'F.Cu': None,
    'In1.Cu': None,
    'In2.Cu': None,
    'In4.Cu': None,
    'In4.Cu': 'F.Cu',
    'B.Cu': 'B.Cu',
}
map_copper['MID', 'inside'] = {
    'F.Cu': None,
    'In1.Cu': None,
    'In2.Cu': 'F.Cu',
    'In3.Cu': 'B.Cu',
    'In4.Cu': None,
    'B.Cu': None,
}  # mid is the decorative/structural board
map_copper['LOW', 'inside'] = {
    'F.Cu': 'F.Cu',
    'In1.Cu': 'B.Cu',
    'In2.Cu': None,
    'In3.Cu': None,
    'In4.Cu': None,
    'B.Cu': None,
}
map_copper[('TOP', 'outside')] = map_copper['LOW', 'inside']
map_copper[('LOW', 'outside')] = map_copper['TOP', 'inside']

# Alternative naming to reduce code changes
# map_copper = dict()
# map_copper['EXTRA', 'inside'] = {
#     'F.Cu': None,
#     'In1.Cu': None,
#     'In2.Cu': 'F.Cu',
#     'In3.Cu': 'B.Cu',
#     'In4.Cu': None,
#     'B.Cu': None,
# }  # top is the decorative board
# map_copper['TOP', 'inside'] = {
#     'F.Cu': None,
#     'In1.Cu': None,
#     'In2.Cu': None,
#     'In4.Cu': None,
#     'In4.Cu': 'F.Cu',
#     'B.Cu': 'B.Cu',
# }
# map_copper['LOW', 'inside'] = {
#     'F.Cu': 'F.Cu',
#     'In1.Cu': 'B.Cu',
#     'In2.Cu': None,
#     'In3.Cu': None,
#     'In4.Cu': None,
#     'B.Cu': None,
# }


def process_vias3(pcb, which_one='LOW', proc_opts=None):
    ''' 1. Turn through vias into bonding pads. They really cannot be tented (i.e. with mask opening)
        2. Convert vias to internal layers into through vias. They can be tented.
        Argument units in mm and pertain only to bonding pads
        TODO: replace the bonding pads with a one-sided SMD pad so that routing can happen on the other side... This would be very confusing for DRC
    '''
    sandwich_type = proc_opts.sandwich_type
    coverage_ratio = proc_opts.vias.coverage_ratio
    # diameter_override = proc_opts.vias.get('diameter_override', None)
    # diameter_minimum = proc_opts.vias.get('diameter_minimum', None)
    # drill_override = proc_opts.vias.get('drill_override', None)
    # drill_minimum = proc_opts.vias.get('drill_minimum', None)
    shrink_outside = proc_opts.vias.get('shrink', True)
    # assert diameter_override is None or diameter_minimum is None
    # assert drill_override is None or drill_minimum is None

    for via in pcb.vias:
        # Bond pad cases
        make_pad = False
        if via._obj.GetViaType() in [pcbnew.VIA_MICROVIA, pcbnew.VIA_BLIND_BURIED]:
            if {via.top_layer, via.bottom_layer} == {'In1.Cu', 'In2.Cu'}:
                # Bond pad through everything
                make_pad = True
                if which_one == 'LOW':
                    to_mask = ['F']
                elif which_one == 'TOP':
                    to_mask = ['B']
                elif which_one == 'MID':
                    to_mask = ['F', 'B']
            elif {via.top_layer, via.bottom_layer} == {'In3.Cu', 'In4.Cu'}:
                # Simple pad to the decorative board
                make_pad = True
                if which_one == 'LOW':
                    pcb.remove(via)
                    continue
                elif which_one == 'TOP':
                    to_mask = ['B']
                elif which_one == 'MID':
                    to_mask = ['F']
        elif via._obj.GetViaType() == pcbnew.VIA_THROUGH:
            # Simple pad between technical boards
            make_pad = True
            if which_one == 'LOW':
                to_mask = ['F']
            elif which_one == 'TOP':
                pcb.remove(via)
                continue
            elif which_one == 'MID':
                to_mask = ['B']

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
            toplayer = map_copper[which_one, sandwich_type].get(via.top_layer, via.top_layer)
            if toplayer is None:
                pcb.remove(via)
            else:
                via.top_layer = toplayer
                via._obj.SetViaType(pcbnew.VIA_THROUGH)

            bottomlayer = map_copper[which_one, sandwich_type].get(via.bottom_layer, via.bottom_layer)
            if bottomlayer is None:
                pcb.remove(via)
            else:
                via.bottom_layer = bottomlayer
                via._obj.SetViaType(pcbnew.VIA_THROUGH)


def process_modules3(pcb, which_one='LOW', proc_opts=None):
    '''Use KISANDWICH-MIDBOARD in the value to designate '''
    for mod in pcb.modules:
        if (which_one == 'MID') ^ mod.value.startswith('KISANDWICH-MIDBOARD'):
            pcb.remove(mod)

    # filter again if it is one of the outer boards
    if which_one != 'MID':
        return core.process_modules(pcb, which_one, proc_opts)

