''' Mousebites using the Eco1 layer.
    An example of an action plugin simplified by kicad-python (200 lines)
    Note: this gives plated vias; NPTH are preferred
    - You can place NPTH Footprints instead of Vias
'''
from kigadgets.board import Board
from kigadgets.drawing import Segment, Arc, Polygon, Rectangle
from kigadgets.via import Via
from kigadgets.point import Point
from kigadgets import notify
from pcbnew import Refresh
from collections import defaultdict
import cmath
import math

radius = 1


def edge_pairs_coterminating(edges):
    x = defaultdict(list)
    pairs = []
    for edge in edges:
        pt1 = (edge.start.x, edge.start.y)
        pt2 = (edge.end.x, edge.end.y)
        x[pt1].append(edge)
        x[pt2].append(edge)

    for corner_coord, hits in x.items():
        if len(hits) < 2:
            continue
        elif len(hits) > 2:
            raise ValueError('Three segments share one point. Abort')
        else:
            pairs.append(hits)
    return pairs

def find_intersection(line1, line2):
    x1, y1 = line1[0]
    x2, y2 = line1[1]
    x3, y3 = line2[0]
    x4, y4 = line2[1]

    # Check if lines are vertical
    if x1 == x2 or x3 == x4:
        if x1 == x2 and x3 == x4:
            # notify(x1, x2, x3, x4)
            return None  # Both lines are vertical and parallel
        elif x1 == x2:
            intersection_x = x1
            slope2 = (y4 - y3) / (x4 - x3)
            intersection_y = slope2 * (intersection_x - x3) + y3
        else:
            intersection_x = x3
            slope1 = (y2 - y1) / (x2 - x1)
            intersection_y = slope1 * (intersection_x - x1) + y1
    else:
        # Calculate slopes
        slope1 = (y2 - y1) / (x2 - x1)
        slope2 = (y4 - y3) / (x4 - x3)

        # Check if lines are parallel
        if slope1 == slope2:
            return None  # Lines are parallel, no intersection

        # Calculate intersection point
        intersection_x = ((slope1 * x1 - slope2 * x3) + y3 - y1) / (slope1 - slope2)
        intersection_y = slope1 * (intersection_x - x1) + y1

    return [intersection_x, intersection_y]

def unique_add(li, it):
    if it in li:
        return True
    li.append(it)
    return False

def three_points(pair):
    pts = []
    for edge in pair:
        if unique_add(pts, edge.start):
            intercept_corner = edge.start
        if unique_add(pts, edge.end):
            intercept_corner = edge.end
    if len(pts) != 3:
        raise ValueError('No coincident ends found\n' + str(pts))
    pts.remove(intercept_corner)
    pts.insert(1, intercept_corner)

    thetas = [None, None]
    dr = intercept_corner - pts[0]
    # notify(dr)
    thetas[0] = math.atan2(dr[1], dr[0])
    dr = pts[-1] - intercept_corner
    # notify(dr)
    thetas[1] = math.atan2(dr[1], dr[0])
    dtheta = thetas[1] - thetas[0]
    # dtheta = dtheta - (2*math.pi)*math.floor((dtheta + math.pi)/(2*math.pi))

    ordered = dtheta < 0
    if dtheta < 0:
        pts = pts[::-1]
        thetas = [th+math.pi for th in thetas[::-1]]
        dtheta *= -1
    return pts, thetas, dtheta, ordered#, start_angle, end_angle

def three_points_old(pair):
    pts = []
    for edge in pair:
        if unique_add(pts, edge.start):
            intercept_corner = edge.start
        if unique_add(pts, edge.end):
            intercept_corner = edge.end
    if len(pts) != 3:
        raise ValueError('No coincident ends found\n' + str(pts))
    pts.remove(intercept_corner)
    pts.insert(1, intercept_corner)


    # Is it in order
    thetas = []
    for pt in pts:
        dx = pt[0] - intercept_corner[0]
        dy = pt[1] - intercept_corner[1]
        thetas.append(math.atan2(dy, dx))
    ordered = thetas[-1] - thetas[0]
    if not ordered:
        return three_points([pair[1], pair[0]])

    # Rotate the first one so they are pointing roughly same direction
    # thetas[0] += math.pi % 2*math.pi
    turn_angle = thetas[-1] - thetas[0]
    # assert turn_angle < 0
    start_angle = thetas[0] - 90
    end_angle = thetas[-1] - 90

    # dtheta = abs(dtheta)
    # if abs(dtheta) > math.pi:
    #     # dtheta -= math.pi
    #     dtheta = 2 * math.pi - dtheta
        # dtheta *= -1
        # thetas = thetas[::-1]
        # pts = pts[::-1]
        # pass
    # if abs(dtheta) > math.pi:
    #     thetas = [th for th in thetas[::-1]]
    #     pts = pts[::-1]
    # dtheta = dtheta % math.pi -
    # notify(dtheta)

    # dtheta = dtheta - 2*math.pi*math.floor((dtheta + 180)/360)

    # if not ordered:
        # notify('hit a')
    #     # thetas = [th for th in thetas[::-1]]
    #     thetas = [math.pi+th for th in thetas]
    #     # pts = pts[::-1]
    #     dtheta = math.pi-dtheta
    #     # ordered = not ordered
    # if not ordered:
    #     thetas = [th for th in thetas[::-1]]
    #     pts = pts[::-1]
        # dtheta = math.pi-dtheta
    # thetas[0] *= -1

    # dtheta = math.pi - dtheta
    # if dtheta > math.pi:
        # notify('hit b')
    #     thetas = thetas[::-1]
    #     pts = pts[::-1]
    #     dtheta = 2*math.pi - dtheta
    #     # dtheta -= math.pi
    #     ordered = not ordered
    # notify(dtheta)

    return pts, thetas, dtheta, ordered, start_angle, end_angle

# def sorted_pair(pair):
#     pts, theta, dtheta, ordered = three_points(pair)
#     if not ordered:
#         pair = pair[::-1]
#         return [[pts[1], pts[0]], [pts[1], pts[2]]]

def pair_to_arc(pair, rad):
    pts, thetas, dtheta, ordered = three_points(pair)
    intercept_corner = pts[1]

    pcb.add(Via(
        pts[0],
        layer_pair=['B.Cu', 'F.Cu'],
        diameter=.1, drill=drill,
        board=pcb)
    )

    insets = [None, None]
    for i in [0, -1]:
        normal = (-rad * math.sin(thetas[i]), rad * math.cos(thetas[i]))
        insets[i] = [pts[i] + normal, intercept_corner + normal]

    # pcb.add(Segment(*insets[0], layer='User.Eco2', board=pcb))
    # pcb.add(Segment(*insets[1], layer='F.Paste', board=pcb))

    # notify(thetas)
    # notify(pts)
    '''
    if ordered and False:
        normal = (-rad * math.sin(thetas[0]), rad * math.cos(thetas[0]))
        if thetas[0] > 1/2 * math.pi and thetas[0] < 3/2 * math.pi:
            insets[0] = [pts[0] - normal, intercept_corner - normal]
        else:
            insets[0] = [pts[0] + normal, intercept_corner + normal]

        normal = (-rad * math.sin(thetas[-1]), rad * math.cos(thetas[-1]))
        if thetas[-1] > 1/2 * math.pi and thetas[-1] < 3/2 * math.pi:
            insets[-1] = [pts[-1] + normal, intercept_corner + normal]
        else:
            insets[-1] = [pts[-1] - normal, intercept_corner - normal]


        # normal = (-rad * math.sin(thetas[-1]), rad * math.cos(thetas[-1]))
        # insets[1] = [pts[-1] - normal, intercept_corner - normal]
    else:
        rad_sgn = rad #* (1 if ordered else -1)
        normal = (-rad_sgn * math.sin(thetas[0]), rad_sgn * math.cos(thetas[0]))
        insets[0] = [pts[0] + normal, intercept_corner + normal]

        normal = (-rad_sgn * math.sin(thetas[-1]), rad_sgn * math.cos(thetas[-1]))
        insets[1] = [pts[-1] + normal, intercept_corner + normal]
    '''
    center = find_intersection(insets[0], insets[1])

    # theta = thetas[0]# if ordered else thetas[-1]
    # theta *= 180 / math.pi
    # arc_angle = dtheta * 180 / math.pi

    if True:
        tt = thetas
    else:
        tt = [thetas[-1], thetas[0]]
    start_angle = tt[0] * 180 / math.pi
    end_angle = tt[1] * 180 / math.pi

    # if False:
    #     arc_angle = 180 - arc_angle

    # notify(theta, dtheta)

    # return center, rad, thetas[0] * 180 / math.pi - 90, thetas[-1] * 180 / math.pi - 90
    return center, rad, start_angle, end_angle


pcb = Board.from_editor()

selected_by_layer = defaultdict(list)
for item in pcb.selected_items:
    if isinstance(item, Segment):
        selected_by_layer[item.layer].append(item)

for layer, segments in selected_by_layer.items():
    pairs = edge_pairs_coterminating(segments)
    for pair in pairs:
        pts, theta, dtheta, ordered = three_points(pair)

        if dtheta in [0, 180]:
            continue
        arc_args = pair_to_arc(pair, radius)

        if not ordered:
            tmp = pair[0]
            pair[0] = pair[1]
            pair[1] = tmp
        intercept_corner = pts[1]
        # pcb.add(Via(
        #     intercept_corner,
        #     layer_pair=['B.Cu', 'F.Cu'],
        #     diameter=.1, drill=drill,
        #     board=pcb)
        # )
        # notify(arc_args[0])
        if arc_args[0] is None:
            continue
        arc = Arc(*arc_args, width=pair[0].width, layer=layer, board=pcb)
        pcb.add(arc)

        for seg, target in zip(pair, [arc.end, arc.start]):
            if seg.start == intercept_corner:
                seg.start = target
            elif seg.end == intercept_corner:
                seg.end = target
            else:
                notify('problems')
        # if pair[0].start == intercept_corner:
        #     pair[0].start = arc.end
        # elif pair[0].end == intercept_corner:
        #     pair[0].end = arc.end
        # else:
        #     notify('big problem')
        # if pair[1].start == intercept_corner:
        #     pair[1].start = arc.start
        # elif pair[1].end == intercept_corner:
        #     pair[1].end = arc.start
        # else:
        #     notify('big problem')
        continue




def converstion_query():
    text = 'Converting a box/polygon into segments. Are you sure?'
    try:
        import wx
    except ImportError:
        print(text)
    else:
        dialog = wx.MessageDialog(None, text, 'kisandwich debug output', wx.OK)
        sg = dialog.ShowModal()


Refresh()
