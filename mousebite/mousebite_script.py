''' Mousebites using the Eco1 layer.
    An example of an action plugin simplified by kicad-python (200 lines)
    Note: this gives plated vias; NPTH are preferred
    - You can place NPTH Footprints instead of Vias
'''
from kicad.pcbnew.board import Board
from kicad.pcbnew.drawing import Segment, Arc, Polygon, Rectangle
from kicad.pcbnew.via import Via
from kicad.point import Point
# from kicad import notify
from atait_scripting_support import reload, notify
from pcbnew import Refresh
from mousebite import objview

is_vert = lambda seg: seg.start.x == seg.end.x
is_horz = lambda seg: seg.start.y == seg.end.y

def get_segments(board):
    ''' Called multiple times because we are changing the segments
        every time we manifest a new mousebite
    '''
    eco_dwgs = []
    edge_dwgs = []
    for dwg in board.drawings:
        if not isinstance(dwg, Segment): continue
        if dwg.layer == opts.slay:
            eco_dwgs.append(dwg)
        elif dwg.layer == 'Edge.Cuts':
            edge_dwgs.append(dwg)
    eco_vert = [eco for eco in eco_dwgs if is_vert(eco)]
    eco_horz = [eco for eco in eco_dwgs if is_horz(eco)]
    edge_vert = [edge for edge in edge_dwgs if is_vert(edge)]
    edge_horz = [edge for edge in edge_dwgs if is_horz(edge)]
    return eco_vert, eco_horz, edge_vert, edge_horz

def intersect_perp(vert, horz, either=True):
    x = vert.start.x
    y = horz.start.y
    if either and intersect_perp(horz, vert, either=False):
        return True
    if (horz.start.x < x) ^ (horz.end.x > x):
        return False
    if (vert.start.y < y) ^ (vert.end.y > y):
        return False
    return True

def converstion_query():
    text = 'Converting a box/polygon into segments. Are you sure?'
    try:
        import wx
    except ImportError:
        print(text)
    else:
        dialog = wx.MessageDialog(None, text, 'kisandwich debug output', wx.OK)
        sg = dialog.ShowModal()

# notify(f'Found {len(eco_dwgs)} eco drawings')
# notify('--Edges--\n', '\n'.join(str(isinstance(ee, Segment)) for ee in edge_dwgs))

def get_bite_pairs(eco_segments, edge_segments):
    all_matches = []
    for eco in eco_segments:
        matches = []
        for ed in edge_segments:
            if intersect_perp(eco, ed):
                matches.append(ed)
        if len(matches) == 2:
            all_matches.append((eco, matches))
        elif len(matches) == 0:
            pass
        else:
            eco.select()
            raise ValueError(
                f'Got {len(matches)} of intersecting Edge.Cuts segments.\n'
                'It must be exactly 2. See the selected {} segment.'.format(opts.slay)
            )
    return all_matches

def get_bite_pair(eco_segments, edge_segments):
    for eco in eco_segments:
        matches = []
        for ed in edge_segments:
            if intersect_perp(eco, ed):
                matches.append(ed)
        if len(matches) == 2:
            return (eco, matches[0], matches[1])
        elif len(matches) == 0:
            pass
        else:
            eco.select()
            raise ValueError(
                f'Got {len(matches)} of intersecting Edge.Cuts segments.\n'
                'It must be exactly 2. See the selected {} segment.'.format(opts.slay)
            )
    return None

def sort_box(og_box, ix=0):
    ''' Sorts a 2x2 list of Points
        The first index is north/south with ascending y
        The second index is west/east with ascending x
    '''
    og_box[0].sort(key=lambda pt: pt[ix])
    og_box[1].sort(key=lambda pt: pt[ix])
    og_box.sort(key=lambda ln: ln[0][1-ix])

def do_drawing(board, eco, h1, h2, horizontal=False):
    # XY indexing
    ix = 1 if horizontal else 0
    iy = 1 - ix
    if horizontal:
        latlon_point = lambda lat, lon: Point(lon, lat)
    else:
        latlon_point = lambda lat, lon: Point(lat, lon)

    for ln in [eco, h1, h2]:
        board.remove(ln, permanent=False)

    # Key anchor points oriented by latitude/longitude instead of X/Y
    box_corner = [[h1.start, h1.end], [h2.start, h2.end]]
    sort_box(box_corner, ix)
    longitudes = [h.start[iy] for h in (h1, h2)]  # y if vertical, x if not
    latitudes = [eco.start[ix] + sgn * opts.tab_width/2 for sgn in [-1, 1]]
    box_bridge = [[latlon_point(lat, lon) for lat in latitudes] for lon in longitudes]
    sort_box(box_bridge, ix)

    # Place the fillets, bridge, and snipped original edge
    dwg_kws = dict(width=h1.width, layer='Edge.Cuts', board=board)
    for iwe in range(2):
        for ins in range(2):
            sgn_we = (-1) ** iwe
            sgn_ns = (-1) ** ins
            # fillet
            dr = latlon_point(-sgn_we * opts.fillet, sgn_ns * opts.fillet)
            center = box_bridge[ins][iwe] + dr
            angle = 90 * (ins - iwe * sgn_ns)
            if horizontal and ins == iwe:
                angle += 180
            arc = Arc(center, opts.fillet, angle, angle + 90, **dwg_kws)
            board.add(arc)
            # replacement clipped edge
            outward_end = arc.start if (ins == iwe ^ horizontal) else arc.end
            inward_end = arc.end if (ins == iwe ^ horizontal) else arc.start
            board.add(Segment(outward_end, box_corner[ins][iwe], **dwg_kws))
            # bridge
            if ins == 0:
                prev_end = inward_end
            else:
                board.add(Segment(prev_end, inward_end, **dwg_kws))
    # Vias
    lat0 = eco.start[ix]
    nvias = int((opts.tab_width + 2 * opts.fillet) / opts.pitch)
    longitudes = [box_corner[0][0][iy] - opts.inset, box_corner[1][0][iy] + opts.inset]
    for lon in longitudes:
        for ivia in range(-nvias+1, nvias):
            point = latlon_point(lat0 + ivia * opts.pitch, lon)
            board.add(Via(
                point,
                layer_pair=['B.Cu', 'F.Cu'],
                diameter=.1, drill=opts.drill,
                board=board)
            )

opts = objview(
    slay = 'User.Eco1',
    tab_width = 3,  # mm
    pitch = 1.3,
    fillet = 1,
    drill = .8,
    inset = 0.25,
)

def main_gui(dialog_opts=None):
    if dialog_opts is not None:
        opts.update(dialog_opts)
    pcb = Board.from_editor()

    for _ in range(100):
        eco_vert, _, _, edge_horz = get_segments(pcb)
        lines = get_bite_pair(eco_vert, edge_horz)
        if lines is None: break
        do_drawing(pcb, *lines, horizontal=False)

    for _ in range(100):
        _, eco_horz, edge_vert, _ = get_segments(pcb)
        lines = get_bite_pair(eco_horz, edge_vert)
        if lines is None: break
        do_drawing(pcb, *lines, horizontal=True)

    Refresh()

# main_gui()
