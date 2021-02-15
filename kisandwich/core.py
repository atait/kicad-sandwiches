''' Sandwich a.k.a. Oreo board logic
'''
from atait_scripting_support import reload, notify
import os

import pcbnew
import kicad
from kicad.pcbnew import drawing, module, board, layer
from kicad.pcbnew.layer import Layer
from kicad.pcbnew.board import Board
# Reload any modules that this project depends on
# reload(kicad)
# reload(drawing)
# reload(module)
# reload(board)


class objview(dict):
    def __getattr__(self, attr):
        return self.__getitem__(attr)

    def __setattr__(self, attr, val):
        self.__setitem__(attr, val)


map_edges = objview(
    TOP={
        'Eco1.User': 'Edge.Cuts',
        'TOP.Cuts': 'Edge.Cuts',
        'Eco2.User': None,
    },
    LOW={
        'Eco2.User': 'Edge.Cuts',
        'LOW.Cuts': 'Edge.Cuts',
        'Eco1.User': None,
    }
)

map_drawings = objview(
    TOP={
        'B.SilkS': None,
        'B.Mask': None,
        'Margin': 'B.Mask'
    }
    LOW={
        'F.SilkS': None,
        'F.Mask': None,
        'Margin': 'F.Mask'
    }
)

map_copper = dict()
map_copper['TOP', 'inside'] = {
    'In1.Cu': None,
    'In2.Cu': 'F.Cu',
    # 'B.Cu': 'B.Cu',
    'F.Cu': None,
}
map_copper['LOW', 'inside'] = {
    'In1.Cu': 'B.Cu',
    'In2.Cu': None,
    # 'F.Cu': 'F.Cu',
    'B.Cu': None,
}
map_copper[('TOP', 'outside')] = map_copper['LOW', 'inside']
map_copper[('LOW', 'outside')] = map_copper['TOP', 'inside']


def process_tracks(pcb, which_one='LOW', sandwich_type='inside'):
    for tr in pcb.tracks:
        tr_layer = map_copper[which_one, sandwich_type].get(tr.layer, tr.layer)
        if tr_layer is None:
            pcb.remove(tr)
        else:
            tr.layer = tr_layer


def process_zones(pcb, which_one='LOW', sandwich_type='inside', remove_keepouts=False):
    ''' Bug: does not work with multi-layer keepouts '''
    for zone in pcb.zones:
        zo_layer = map_copper[which_one, sandwich_type].get(zone.layer, zone.layer)
        if zo_layer is None:
            pcb.remove(zone)
        else:
            zone.layer = zo_layer
        if remove_keepouts and zone.is_keepout:
            pcb.remove(zone)


def process_drawings(pcb, which_one='LOW', sandwich_type='inside', all_opts=None):
    my_map = map_drawings[which_one]
    if all_opts is not None and all_opts['bond_masks']:
        if which_one == 'TOP':
            my_map = dict(
                'B.SilkS': None,
                'F.Mask': None
            )
        else:
            my_map = dict(
                'F.SilkS': None,
                'B.Mask': None
            )
    for dw in pcb.drawings:
        dw_layer = my_map.get(dw.layer, dw.layer)
        if dw_layer is None:
            pcb.remove(dw)
        else:
            dw.layer = dw_layer


def process_modules(pcb, which_one='LOW', sandwich_type='inside'):
    if (sandwich_type == 'inside') ^ (which_one == 'TOP'):
        module_map = {Layer.Back: None}
    else:
        module_map = {Layer.Front: None}

    for mod in pcb.modules:
        mod_layer = module_map.get(mod.layer, mod.layer)
        if mod_layer is None:
            pcb.remove(mod)


def process_vias(pcb, which_one='LOW', sandwich_type='inside',
    coverage_ratio=1.1,
    diameter_override=None, diameter_minimum=None,
    drill_override=None, drill_minimum=None,
    module_treatment=None,
):
    ''' 1. Turn through vias into bonding pads. They really cannot be tented (i.e. with mask opening)
        2. Convert vias to internal layers into through vias. They can be tented.
        Argument units in mm and pertain only to bonding pads
        TODO: replace the bonding pads with a one-sided SMD pad so that routing can happen on the other side... This would be very confusing for DRC
    '''
    assert diameter_override is None or diameter_minimum is None
    assert drill_override is None or drill_minimum is None
    for via in pcb.vias:
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
        # Make open bond pads
        elif via._obj.GetViaType() == pcbnew.VIA_THROUGH:
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
            pcb.add_circle(
                via.center,
                opening_radius,
                'F.Mask' if (which_one == 'LOW') else 'B.Mask',
                opening_width)


def process_all(pcb, which_one='LOW', proc_opts=None, bp_opts=None,
    zone_opts=None, sandwich_type=None, all_opts=None):
    ''' proc_opts is a dictionary with either functions or strings describing the steps to take '''
    if proc_opts is None or proc_opts.get('tracks', False):
        process_tracks(pcb, which_one, sandwich_type=sandwich_type)
    if proc_opts is None or proc_opts.get('drawings', False):
        process_drawings(pcb, which_one, sandwich_type=sandwich_type, all_opts=all_opts)
    if proc_opts is None or proc_opts.get('modules', False):
        process_modules(pcb, which_one, sandwich_type=sandwich_type)
    if proc_opts is None or proc_opts.get('vias', False):
        if bp_opts is None:
            bp_opts = dict()
        process_vias(pcb, which_one, sandwich_type=sandwich_type, **bp_opts)
    if proc_opts is None or proc_opts.get('zones', False):
        if zone_opts is None:
            zone_opts = dict()
        process_zones(pcb, which_one, sandwich_type=sandwich_type, **zone_opts)
    pcb.fill_zones()


### Entry points
def sandwich_from_gui(which_one='LOW', refresh=False, outfile=None,
    proc_opts=None, bp_opts=None, zone_opts=None, sandwich_type=None, all_opts=None):
    livepcb = Board.from_editor()
    if refresh:
        process_all(livepcb, which_one, proc_opts=proc_opts, bp_opts=bp_opts, zone_opts=zone_opts, sandwich_type=sandwich_type, all_opts=all_opts)
        pcbnew.Refresh()
        if outfile is not None:
            livepcb.save(outfile)
    elif outfile is not None:
        tempfile = '~sandwich-temp.kicad_pcb'
        livepcb.save(tempfile)
        try:
            workingpcb = Board.load(tempfile)
            process_all(workingpcb, which_one, proc_opts=proc_opts, bp_opts=bp_opts, zone_opts=zone_opts, sandwich_type=sandwich_type, all_opts=all_opts)
            workingpcb.save(outfile)
        finally:
            os.remove(tempfile)


def base_to_default_boardfile(filepath, which_one='LOW', subdirectory=''):
    ''' subdirectory is relative to the directory that the file is in '''
    basefile = os.path.basename(filepath)
    components = basefile.split('.')
    newbase = components[-2] + '-sandwich_' + which_one + '.' + components[-1]
    newdir = os.path.join(os.path.dirname(filepath), subdirectory)
    if not os.path.exists(newdir):
        os.mkdir(newdir)
    return os.path.join(newdir, newbase)


def sandwich_from_file(infile, which_one='LOW', outfile=None):
    ''' The CLI '''
    if outfile is None:
        outfile = base_to_default_boardfile(infile, which_one)
    workingpcb = Board.load(infile)
    process_all(workingpcb, which_one)
    workingpcb.save(outfile)
