import math, collections, pygame


# TODO: Implement a HexMap class, incorporate the below methods, and write the damn docstrings
class HexMap:

    Orientation = collections.namedtuple("Orientation", ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"])
    Layout = collections.namedtuple("Layout", ["orientation", "size", "origin"])
    Point = collections.namedtuple("Point", ["x", "y"])
    CubeCoord = collections.namedtuple("Hex", ["q", "r", "s"])

    def __init__(self, pixelsize_x, pixelsize_y, orientation='flat'):
        Orientation = collections.namedtuple("Orientation",
                                             ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"])
        Layout = collections.namedtuple("Layout", ["orientation", "size", "origin"])
        Point = collections.namedtuple("Point", ["x", "y"])
        CubeCoord = collections.namedtuple("Hex", ["q", "r", "s"])

        self.pixelsize = (pixelsize_x, pixelsize_y)
        self.area = pixelsize_x * pixelsize_y

        if orientation == 'flat':
            self.layout = Orientation(
                3.0 / 2.0,
                0.0,
                math.sqrt(3.0) / 2.0,
                math.sqrt(3.0),
                2.0 / 3.0,
                0.0,
                -1.0 / 3.0,
                math.sqrt(3.0) / 3.0,
                0.0
            )
        elif orientation == 'pointy':
            self.layout = Orientation(
                math.sqrt(3.0),
                math.sqrt(3.0) / 2.0,
                0.0,
                3.0 / 2.0,
                math.sqrt(3.0) / 3.0,
                -1.0 / 3.0,
                0.0,
                2.0 / 3.0,
                0.5
            )
        else:
            raise Exception('You must specify flat-topped or pointy-topped hexagons.')

        # Rows and columns are diagonal in the axial and cube coordinate system.
        # It might be easier in this instance to convert to offset rows long enough to populate the grid.
        self.hexradius = math.sqrt(pixelsize_x ** 2 + pixelsize_y ** 2)

        self.surface = pygame.Surface(self.pixelsize)


# layout_pointy = Orientation(
#     math.sqrt(3.0),
#     math.sqrt(3.0) / 2.0,
#     0.0,
#     3.0 / 2.0,
#     math.sqrt(3.0) / 3.0,
#     -1.0 / 3.0,
#     0.0,
#     2.0 / 3.0,
#     0.5
# )
#
# layout_flat = Orientation(
#     3.0 / 2.0,
#     0.0,
#     math.sqrt(3.0) / 2.0,
#     math.sqrt(3.0),
#     2.0 / 3.0,
#     0.0,
#     -1.0 / 3.0,
#     math.sqrt(3.0) / 3.0,
#     0.0
# )


def hex_add(a, b):
    return CubeCoord(a.q + b.q, a.r + b.r, a.s + b.s)


def hex_subtract(a, b):
    return CubeCoord(a.q - b.q, a.r - b.r, a.s - b.s)


def hex_scale(a, k):
    return CubeCoord(a.q * k, a.r * k, a.s * k)


def hex_rotate_left(a):
    return CubeCoord(-a.s, -a.q, -a.r)


def hex_rotate_right(a):
    return CubeCoord(-a.r, -a.s, -a.q)


hex_directions = [CubeCoord(1, 0, -1), CubeCoord(1, -1, 0), CubeCoord(0, -1, 1), CubeCoord(-1, 0, 1), CubeCoord(-1, 1, 0), CubeCoord(0, 1, -1)]


def hex_direction(direction):
    return hex_directions[direction]


def hex_neighbor(hex, direction):
    return hex_add(hex, hex_direction(direction))


hex_diagonals = [CubeCoord(2, -1, -1), CubeCoord(1, -2, 1), CubeCoord(-1, -1, 2), CubeCoord(-2, 1, 1), CubeCoord(-1, 2, -1), CubeCoord(1, 1, -2)]


def hex_diagonal_neighbor(hex, direction):
    return hex_add(hex, hex_diagonals[direction])


def hex_length(hex):
    return (abs(hex.q) + abs(hex.r) + abs(hex.s)) // 2


def hex_distance(a, b):
    return hex_length(hex_subtract(a, b))


def hex_round(h):
    q = int(round(h.q))
    r = int(round(h.r))
    s = int(round(h.s))
    q_diff = abs(q - h.q)
    r_diff = abs(r - h.r)
    s_diff = abs(s - h.s)
    if q_diff > r_diff and q_diff > s_diff:
        q = -r - s
    else:
        if r_diff > s_diff:
            r = -q - s
        else:
            s = -q - r
    return CubeCoord(q, r, s)


def hex_lerp(a, b, t):
    return CubeCoord(a.q * (1 - t) + b.q * t, a.r * (1 - t) + b.r * t, a.s * (1 - t) + b.s * t)


def hex_linedraw(a, b):
    N = hex_distance(a, b)
    a_nudge = CubeCoord(a.q + 0.000001, a.r + 0.000001, a.s - 0.000002)
    b_nudge = CubeCoord(b.q + 0.000001, b.r + 0.000001, b.s - 0.000002)
    results = []
    step = 1.0 / max(N, 1)
    for i in range(0, N + 1):
        results.append(hex_round(hex_lerp(a_nudge, b_nudge, step * i)))
    return results