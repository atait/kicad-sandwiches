import os
import pcbnew
from kigadgets.board import Board
from kisandwich import objview
import kisandwich.core as core


map_copper3 = dict()
map_copper3['TOP', 'inside'] = {
    'F.Cu': None,
    'In1.Cu': None,
    'In2.Cu': None,
    'In3.Cu': None,
    'In4.Cu': 'F.Cu',
    'B.Cu': 'B.Cu',
    'Mid.F.SilkS': None,
    'Mid.B.SilkS': None,
    'Mid.F.Mask': None,
    'Mid.B.Mask': None,
}
map_copper3['MID', 'inside'] = {
    'F.Cu': None,
    'In1.Cu': None,
    'In2.Cu': 'B.Cu',
    'In3.Cu': 'F.Cu',
    'In4.Cu': None,
    'B.Cu': None,
    'Mid.F.SilkS': 'F.SilkS',
    'Mid.B.SilkS': 'B.SilkS',
    'Mid.F.Mask': 'F.Mask',
    'Mid.B.Mask': 'B.Mask',
}  # mid is the decorative/structural board
map_copper3['LOW', 'inside'] = {
    'F.Cu': 'F.Cu',
    'In1.Cu': 'B.Cu',
    'In2.Cu': None,
    'In3.Cu': None,
    'In4.Cu': None,
    'B.Cu': None,
    'Mid.F.SilkS': None,
    'Mid.B.SilkS': None,
    'Mid.F.Mask': None,
    'Mid.B.Mask': None,
}
map_copper3['STENCIL', 'inside'] = {
    'F.Cu': None,
    'In1.Cu': None,
    'In2.Cu': None,
    'In3.Cu': None,
    'In4.Cu': None,
    'B.Cu': None,
    'Mid.F.SilkS': None,
    'Mid.B.SilkS': None,
    'Mid.F.Mask': None,
    'Mid.B.Mask': None,
}
map_copper3[('TOP', 'outside')] = map_copper3['LOW', 'inside']
map_copper3[('LOW', 'outside')] = map_copper3['TOP', 'inside']
map_copper3[('STENCIL', 'outside')] = map_copper3['STENCIL', 'inside']
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
        make_one_sided_pad = False
        if not via.is_through:
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
                make_one_sided_pad = True
                if to_frontboard ^ (sandwich_type == 'inside'):
                    if which_one == 'MID' or which_one == 'STENCIL':
                        to_mask = ['F']
                    elif which_one == 'TOP':
                        to_mask = ['B']
                    elif which_one == 'LOW':
                        pcb.remove(via)
                        continue
                if to_backboard ^ (sandwich_type == 'inside'):
                    if which_one == 'MID' or which_one == 'STENCIL':
                        to_mask = ['B']
                    elif which_one == 'TOP':
                        pcb.remove(via)
                        continue
                    elif which_one == 'LOW':
                        to_mask = ['F']

        elif via.is_through:
            # Bond pad through everything
            make_one_sided_pad = True
            if which_one == 'LOW':
                to_mask = ['F']
            elif which_one == 'TOP':
                to_mask = ['B']
            elif which_one == 'MID' or which_one == 'STENCIL':
                to_mask = ['F', 'B']

        # Make the pads
        if make_one_sided_pad:
            if diameter_override is not None:
                via.diameter = diameter_override
            elif diameter_minimum is not None:
                via.diameter = max(via.diameter, diameter_minimum)
            if drill_override is not None:
                via.drill = drill_override
            elif drill_minimum is not None:
                via.drill = max(via.drill, drill_minimum)
            via.is_through = True

            opening_radius = coverage_ratio * via.diameter / 4
            opening_width = 2 * opening_radius
            opening_kwargs = dict(center=via.center, radius=opening_radius, width=opening_width)
            if shrink_outside:
                via.diameter = via.drill * 1.05
            for mask_side in to_mask:
                pcb.add_circle(layer=mask_side + '.Mask', **opening_kwargs)
                if shrink_outside:
                    start = via.center - (0.001, 0)
                    end = via.center + (0.001, 0)
                    pad = pcb.add_track_segment(start=start, end=end, layer=mask_side+'.Cu', width=2*opening_radius+opening_width)
                    pad.net_name = via.net_name
                    # pcb.add_circle(layer=mask_side + '.Cu', **opening_kwargs)

            if which_one == 'STENCIL' or which_one == 'MID' and proc_opts.enable.stencil:
                x = proc_opts.stencil.get('fill_ratio', 0.8)
                stencil_radius = x * opening_radius + (1-x) * (via.drill / 4)  # Shrink so we don't put too much paste. Will make thinner bond
                stencil_width = 2 * stencil_radius
                stencil_kwargs = dict(center=via.center, radius=stencil_radius, width=stencil_width)
                for mask_side in to_mask:
                    pcb.add_circle(layer=mask_side + '.Paste', **stencil_kwargs)
            continue

        # Turn intra-board blind vias into regular vias. Delete ones in wrong layers
        if not via.is_through:
            toplayer = map_copper3[which_one, sandwich_type].get(via.top_layer, via.top_layer)
            if toplayer is None:
                pcb.remove(via)
            else:
                via.top_layer = toplayer
                via.is_through = True

            bottomlayer = map_copper3[which_one, sandwich_type].get(via.bottom_layer, via.bottom_layer)
            if bottomlayer is None:
                pcb.remove(via)
            else:
                via.bottom_layer = bottomlayer
                via.is_through = True


def transmute_module_cuts(mod, which_one='LOW', flipped=False, proc_opts=None):
    ''' Change Eco1, Eco2, and Margin to Edge.Cuts or delete, depending on which board
        Also maps/deletes non-pad copper
        Pad copper is removed if on the wrong side or through hole
    '''
    which_one_edges = which_one
    if flipped:
        which_one_edges = {'LOW': 'TOP', 'TOP': 'LOW', 'MID': 'MID'}[which_one]
    to_remove = set()
    for dw in mod.graphicalItems:
        dw_layer = core.map_edges[which_one_edges].get(dw.layer, dw.layer)
        dw_layer = map_copper3[which_one, proc_opts.sandwich_type].get(dw_layer, dw_layer)
        dw_layer = core.map_drawings[which_one].get(dw_layer, dw_layer)
        if dw_layer is None:
            to_remove.add(dw)
        else:
            dw.layer = dw_layer
    for dw in to_remove:
        mod.remove(dw)


def process_modules3(pcb, which_one='LOW', proc_opts=None):
    ''' Use KISANDWICH-MIDBOARD in the value to designate footprint on the middle board
        Use KISANDWICH-CUTTER to designate that drawings should be turned into cuts
    '''
    for mod in pcb.modules:
        # cutter modules. Keep cutters in the stencil
        if mod.value.startswith('KISANDWICH-CUTTER'):
            flipped = (mod.layer == 'B.Cu')
            transmute_module_cuts(mod, which_one, flipped, proc_opts=proc_opts)
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
                ^ (mod.layer == 'B.Cu')
                or (which_one == 'STENCIL')
            ):
                pcb.remove(mod)
