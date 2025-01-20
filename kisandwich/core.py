''' Sandwich a.k.a. Oreo board logic
'''
import os
import pcbnew
from kigadgets.board import Board
from kigadgets.layer import LayerSet
from kisandwich import objview
# Reload any modules that this project depends on
# from kigadgets import drawing, module, board, layer
# reload(kigadgets)
# reload(drawing)
# reload(module)
# reload(board)


map_edges = objview(
    TOP={
        'User.Eco1': 'Edge.Cuts',
        'Eco1.User': 'Edge.Cuts',
        'User.Eco2': None,
        'Eco2.User': None,
        'Margin': None,
        'User.3': None,
    },
    LOW={
        'User.Eco2': 'Edge.Cuts',
        'Eco2.User': 'Edge.Cuts',
        'User.Eco1': None,
        'Eco1.User': None,
        'Margin': None,
        'User.3': None,
    },
    MID={
        'Margin': 'Edge.Cuts',
        'User.3': 'Edge.Cuts',
        'User.Eco1': None,
        'Eco1.User': None,
        'User.Eco2': None,
        'Eco2.User': None,
    },
    STENCIL={
        'Margin': None,
        'User.3': None,
        'User.Eco1': None,
        'Eco1.User': None,
        'User.Eco2': None,
        'Eco2.User': None,
        'Edge.Cuts': None,
    }
)

# Silk and mask always point outwards
# F.Adhesive points inwards, and it is mirrored on both boards
# Mid.X.Y (e.g. Mid.F.Silkscreen) goes on midboard, if there are three layers
map_drawings = objview(
    TOP={
        'B.Silkscreen': None,
        'B.Mask': None,
        'F.Adhesive': None,
        'B.Adhesive': 'B.Mask',
        'Mid.F.Silkscreen': None,
        'Mid.B.Silkscreen': None,
        'Mid.F.Mask': None,
        'Mid.B.Mask': None,
    },
    LOW={
        'F.Silkscreen': None,
        'F.Mask': None,
        'F.Adhesive': 'F.Mask',
        'B.Adhesive': None,
        'Mid.F.Silkscreen': None,
        'Mid.B.Silkscreen': None,
        'Mid.F.Mask': None,
        'Mid.B.Mask': None,
    },
    MID={
        'F.Silkscreen': None,
        'F.Mask': None,
        'B.Silkscreen': None,
        'B.Mask': None,
        'F.Adhesive': None,
        'B.Adhesive': None,
        'Mid.F.Silkscreen': 'F.Silkscreen',
        'Mid.B.Silkscreen': 'B.Silkscreen',
        'Mid.F.Mask': 'F.Mask',
        'Mid.B.Mask': 'B.Mask',
    },
    STENCIL={
        'F.Silkscreen': None,
        'F.Mask': None,
        'F.Adhesive': None,
        'B.Silkscreen': None,
        'B.Mask': None,
        'B.Adhesive': None,
        'Mid.F.Silkscreen': None,
        'Mid.B.Silkscreen': None,
        'Mid.F.Mask': None,
        'Mid.B.Mask': None,
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
map_copper['STENCIL', 'inside'] = {
    'In1.Cu': None,
    'In2.Cu': None,
    'F.Cu': None,
    'B.Cu': None,
}
map_copper[('TOP', 'outside')] = map_copper['LOW', 'inside']
map_copper[('LOW', 'outside')] = map_copper['TOP', 'inside']
map_copper[('STENCIL', 'outside')] = map_copper['STENCIL', 'inside']


proc_opts_default = objview(
    enable = objview(tracks=True, drawings=True, modules=True, vias=True, zones=True, stencil=True),
    sandwich_type = 'inside',
    n_boards = 3,
    stencil = objview(fill_ratio=1.0),
    vias = objview(coverage_ratio=1.0, shrink=True),
    zones = objview(remove_keepouts=True),
    drawings = objview(bond_masks=False),
)


def process_tracks(pcb, which_one='LOW', proc_opts=None):
    sandwich_type = proc_opts.sandwich_type
    for tr in pcb.tracks:
        tr_layer = map_copper[which_one, sandwich_type].get(tr.layer, tr.layer)
        if tr_layer is None:
            pcb.remove(tr)
        else:
            tr.layer = tr_layer


def process_zones(pcb, which_one='LOW', proc_opts=None):
    sandwich_type = proc_opts.sandwich_type
    remove_keepouts = proc_opts.zones.remove_keepouts
    for zone in pcb.zones:
        if remove_keepouts and zone.is_keepout:
            pcb.remove(zone)
            continue
        zo_layers_from = zone.layerset.layers
        zo_layers_to = [map_copper[which_one, sandwich_type].get(fro, fro) for fro in zo_layers_from]
        zo_2 = [x for x in zo_layers_to if x is not None]
        if len(zo_2) == 0:
            pcb.remove(zone)
            continue
        zone.layerset = LayerSet(zo_2, pcb)


def process_drawings(pcb, which_one='LOW', proc_opts=None):
    my_map = map_drawings[which_one]
    if proc_opts is not None and proc_opts.drawings.bond_masks:
        if which_one == 'TOP':
            my_map = {
                'B.Silkscreen': None,
                'F.Mask': None
            }
        elif which_one == 'LOW':
            my_map = {
                'F.Silkscreen': None,
                'B.Mask': None
            }
        elif which_one == 'MID':  # For now there is no way to control silk and mask of mid board
            my_map = {
                'F.Silkscreen': None,
                'B.Mask': None,
                'B.Silkscreen': None,
                'F.Mask': None
            }
    for dw in pcb.drawings:
        dw_layer = my_map.get(dw.layer, dw.layer)
        dw_layer = map_edges[which_one].get(dw_layer, dw_layer)  # Also do edge cuts. This might be a separate function
        dw_layer = map_copper[which_one, proc_opts.sandwich_type].get(dw_layer, dw_layer)  # Also do drawings on copper layers
        if dw_layer is None:
            pcb.remove(dw)
        else:
            dw.layer = dw_layer


def process_modules2(pcb, which_one='LOW', proc_opts=None):
    for mod in pcb.modules:
        # cutter modules. Keep cutters in the stencil
        if mod.value.startswith('KISANDWICH-CUTTER'):
            from kisandwich.three_board import transmute_module_cuts
            flipped = (mod.layer == 'B.Cu')
            transmute_module_cuts(mod, which_one, flipped, proc_opts=proc_opts)
            continue  # never delete this module
        if (
            (which_one == 'LOW')
            ^ (proc_opts.sandwich_type == 'inside')
            ^ (mod.layer == 'B.Cu')
            or (which_one == 'STENCIL')
        ):
            pcb.remove(mod)


def process_vias2(pcb, which_one='LOW', proc_opts=None):
    ''' 1. Turn through vias into bonding pads. They really cannot be tented (i.e. with mask opening)
        2. Convert vias to internal layers into through vias. They can be tented.
        Argument units in mm and pertain only to bonding pads
        TODO: replace the bonding pads with a one-sided SMD pad so that routing can happen on the other side... This would be very confusing for DRC
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
        # Turn blind vias into regular vias. Delete ones in wrong layers
        if not via.is_through:
            toplayer = map_copper[which_one, sandwich_type].get(via.top_layer, via.top_layer)
            if toplayer is None:
                pcb.remove(via)
            else:
                via.top_layer = toplayer
                via.is_through = True

            bottomlayer = map_copper[which_one, sandwich_type].get(via.bottom_layer, via.bottom_layer)
            if bottomlayer is None:
                pcb.remove(via)
            else:
                via.bottom_layer = bottomlayer
                via.is_through = True

        # Make open bond pads
        elif via.is_through:
            if diameter_override is not None:
                via.size = diameter_override
            elif diameter_minimum is not None:
                via.size = max(via.size, diameter_minimum)
            if drill_override is not None:
                via.drill = drill_override
            elif drill_minimum is not None:
                via.drill = max(via.drill, drill_minimum)

            opening_radius = coverage_ratio * via.size / 4
            opening_width = 2 * opening_radius
            opening_kwargs = dict(center=via.center, radius=opening_radius, width=opening_width)
            mask_side = 'F' if (which_one == 'LOW') else 'B'
            pcb.add_circle(layer=mask_side+'.Mask', **opening_kwargs)
            if shrink_outside:
                via.size = via.drill * 1.05
                start = via.center - (0.001, 0)
                end = via.center + (0.001, 0)
                pad = pcb.add_track_segment(start=start, end=end, layer=mask_side+'.Cu', width=2*opening_radius+opening_width)
                pad.net_name = via.net_name
                # pcb.add_circle(layer=mask_side+'.Cu', **opening_kwargs)
            if which_one == 'STENCIL':
                x = proc_opts.stencil.get('fill_ratio', 0.6)
                stencil_radius = x * opening_radius + (1-x) * (via.drill / 4)  # Shrink so we don't put too much paste. Will make thinner bond
                stencil_width = 2 * stencil_radius
                stencil_kwargs = dict(center=via.center, radius=stencil_radius, width=stencil_width)
                pcb.add_circle(layer='F.Paste', **stencil_kwargs)
                pcb.add_circle(layer='B.Paste', **stencil_kwargs)


def export_vrml(pcb, outfile=None):
    ''' Can we batch this somehow? It only works in window right now '''
    if outfile is None:
        outfile = pcb.filename.split('.')[0] + '.wrl'
    # print('write to', outfile)

    settings = dict(aFullFileName=outfile, aMMtoWRMLunit=1.0, aExport3DFiles=True, aUseRelativePaths=True, a3D_Subdir='shapes3D', aXRef=0, aYRef=0)
    # v6?
    # pcbnew.VRML_WRITER().ExportVRML_File(outfile, 1.0, True, True, 'shapes3D', 0, 0)
    # works on v7
    # return pcbnew.ExportVRML(outfile, **settings)
    project = pcb._obj.GetProject()
    writer = pcbnew.EXPORTER_VRML(pcb._obj)
    return writer.ExportVRML_File(project, '', **settings)


def process_all(pcb, which_one='LOW', proc_opts=None):
    ''' proc_opts is a dictionary with either functions or strings describing the steps to take '''
    global map_copper
    if proc_opts.n_boards == 3:
        from kisandwich.three_board import process_modules3, map_copper3, process_vias3
        process_modules = process_modules3
        process_vias = process_vias3
        map_copper = map_copper3
    else:
        process_modules = process_modules2
        process_vias = process_vias2
    if proc_opts.enable.tracks:
        process_tracks(pcb, which_one, proc_opts=proc_opts)
    if proc_opts.enable.drawings:
        process_drawings(pcb, which_one, proc_opts=proc_opts)
    if proc_opts.enable.modules:
        process_modules(pcb, which_one, proc_opts=proc_opts)
    if proc_opts.enable.vias:
        process_vias(pcb, which_one, proc_opts=proc_opts)
    if proc_opts.enable.zones:
        process_zones(pcb, which_one, proc_opts=proc_opts)
    pcb.fill_zones()


### Entry points
def sandwich_from_gui(which_one='LOW', refresh=False, outfile=None, proc_opts=None):
    livepcb = Board.from_editor()
    livepath = livepcb.filename
    if refresh:
        process_all(livepcb, which_one, proc_opts=proc_opts)
        pcbnew.Refresh()
        if outfile is not None:
            livepcb.save(outfile)
    elif outfile is not None:
        # livepcb.save(outfile)
        sandwich_from_file(livepath, which_one, outfile, proc_opts)


def base_to_default_boardfile(filepath, which_one='LOW', subdirectory=''):
    ''' subdirectory is relative to the directory that the file is in '''
    basefile = os.path.basename(filepath)
    components = basefile.split('.')
    newbase = components[-2] + '-sandwich_' + which_one + '.' + components[-1]
    newdir = os.path.join(os.path.dirname(filepath), subdirectory)
    if not os.path.exists(newdir):
        os.mkdir(newdir)
    return os.path.join(newdir, newbase)


def sandwich_from_file(infile, which_one='LOW', outfile=None, proc_opts=None):
    ''' The CLI '''
    if outfile is None:
        outfile = base_to_default_boardfile(infile, which_one, subdirectory='kisandwich-out')
    proc_opts_full = proc_opts_default.copy()
    if proc_opts is not None:
        proc_opts_full.update(proc_opts)
    workingpcb = Board.load(infile)
    process_all(workingpcb, which_one, proc_opts_full)
    workingpcb.save(outfile)
    try:
        outvrml = os.path.splitext(outfile)[0] + '.wrl'
        # outwrl = outfile.split('.')[0] + '.wrl'
        export_vrml(workingpcb, outvrml)
    except Exception:
        pass
