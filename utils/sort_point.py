def check_vertical(p, thres=1.5):
    """
    sort 4 points to TL, TR, BL, BR
    """
    xs  = [p[0][0], p[1][0], p[2][0], p[3][0]]
    ys  = [p[0][1], p[1][1], p[2][1], p[3][1]]

    height = max(ys)-min(ys)
    width = max(xs)-min(xs)
    return height > width * 1.5



def sort_4_point_h(ppoints):
    """
    sort 4 points to TL, TR, BL, BR
    """
    points = sorted(ppoints)
    points.sort() # sort by x first y next


    if points[0][1] < points[1][1]:
        tl = points[0]
        bl = points[1]
    else:
        tl = points[1]
        bl = points[0]


    if points[2][1] < points[3][1]:
        tr = points[2]
        br = points[3]
    else:
        tr = points[3]
        br = points[2]
    return [tl, tr, br, bl]

def sort_4_point_v(ppoints):
    """
    sort 4 points to TL, TR, BL, BR
    """
    points = sorted(ppoints, key=lambda x: list(reversed(x)))
    #points.sort() # sort by x first y next


    if points[0][0] < points[1][0]:
        tl = points[0]
        tr = points[1]
    else:
        tl = points[1]
        tr = points[0]


    if points[2][0] < points[3][0]:
        bl = points[2]
        br = points[3]
    else:
        bl = points[3]
        br = points[2]
    #print([tr, br, tl, bl])
    return [tl, tr, br, bl]