import numpy as np
import copy
from scipy.spatial import ConvexHull
from aihub_utils.sort_point import check_vertical, sort_4_point_h, sort_4_point_v

def points2minrect(points):

    result_poly = np.array(points)
    pi2 = np.pi/2.

    #ConvexHull(result_poly).vertices -> result_poly에서 점을 찍을 꼭지점의 index
    #hull_points -> result_poly[인덱스 값] -> 점 좌표

    hull_points = result_poly[ConvexHull(result_poly).vertices]

    edges = np.zeros((len(hull_points), 2))
    edges = hull_points[1:] - hull_points[:-1]

    angles = np.zeros((len(edges)))
    angles = np.arctan2(edges[:, 1], edges[:, 0])

    angles = np.abs(np.mod(angles, pi2))
    angles = np.unique(angles)

    rotations = np.vstack([
        np.cos(angles),
        np.cos(angles-pi2),
        np.cos(angles+pi2),
        np.cos(angles)]).T

    rotations = rotations.reshape((-1, 2, 2))

    rot_points = np.dot(rotations, hull_points.T)

    min_x = np.nanmin(rot_points[:, 0], axis=1)
    max_x = np.nanmax(rot_points[:, 0], axis=1)
    min_y = np.nanmin(rot_points[:, 1], axis=1)
    max_y = np.nanmax(rot_points[:, 1], axis=1)

    areas = (max_x - min_x) * (max_y - min_y)
    best_idx = np.argmin(areas)

    x1 = max_x[best_idx]
    x2 = min_x[best_idx]
    y1 = max_y[best_idx]
    y2 = min_y[best_idx]
    r = rotations[best_idx]

    rval = np.zeros((4, 2))
    rval[0] = np.dot([x1, y2], r)
    rval[1] = np.dot([x2, y2], r)
    rval[2] = np.dot([x2, y1], r)
    rval[3] = np.dot([x1, y1], r)

    return rval.tolist()

def check_word_include_char(bw, bc, margin=5):
    wp = [bw[0], bw[1], bw[0]+bw[2], bw[1]+bw[3]]
    cp = [bc[0], bc[1], bc[0]+bc[2], bc[1]+bc[3]]

    if wp[0]-margin<cp[0] and wp[1]-margin<cp[1] and \
            wp[2]+margin>cp[2] and wp[3]+margin>cp[3]:
        return True
    else:
        return False

def generate_rbox(anno_word, anno_chars_in_w):
    anno_rbox = copy.deepcopy(anno_word)

    poly_points=[]
    for anno in anno_chars_in_w:
        [x, y, w, h] = anno['bbox']
        #print(anno['bbox'])
        poly = [[x,y], [x+w, y], [x+w, y+h], [x, y+h]]
        for j in poly:
            poly_points.append(j)

    rect = points2minrect(poly_points)
    vertical = check_vertical(rect, 1.5)
    if vertical:
        new_rect = sort_4_point_v(rect)
    else:
        new_rect = sort_4_point_h(rect)
    rect_list = np.reshape(new_rect, -1)
    anno_rbox['poly'] = rect_list
    anno_rbox['attributes']['class']='rbox'
    return anno_rbox