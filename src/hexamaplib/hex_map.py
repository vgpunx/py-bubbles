import math, collections, pygame
from hex_cell import HexCell


# TODO: Implement a HexMap class, incorporate the below methods, and write the damn docstrings
class HexMap:

    def __init__(self, pixelsize, hexcount, hex_orientation='flat'):

        """

        :param pixelsize: -> tuple
        :param hexcount: -> tuple
        :param hex_orientation: -> str
        """

        self.Orientation = collections.namedtuple("Orientation",
                                             ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"])
        self.Layout = collections.namedtuple("Layout", ["orientation", "size", "origin"])
        self.Point = collections.namedtuple("Point", ["x", "y"])
        self.CubeCoord = collections.namedtuple("Hex", ["q", "r", "s"])

        self.pixelsize = pixelsize
        # self.area = pygame.Rect(pixelsize.x, pixelsize.y)
        self.hexcount = hexcount
        self.hex_orientation = hex_orientation

        if hex_orientation == 'flat':
            self.hex_orientation = self.Orientation(
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
        elif hex_orientation == 'pointy':
            self.hex_orientation = self.Orientation(
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

        self.hexsize = self.Point((self.pixelsize[0] / self.hexcount[0] / 2),
                                  (self.pixelsize[1] / self.hexcount[1]) / 2)

        self.board = self.populate_board()

    # Orientation = collections.namedtuple("Orientation", ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"])
    # Layout = collections.namedtuple("Layout", ["orientation", "size", "origin"])
    # Point = collections.namedtuple("Point", ["x", "y"])
    # CubeCoord = collections.namedtuple("Hex", ["q", "r", "s"])

    def hex_add(self, a, b):
        return self.CubeCoord(a.q + b.q, a.r + b.r, a.s + b.s)

    def hex_subtract(self, a, b):
        return self.CubeCoord(a.q - b.q, a.r - b.r, a.s - b.s)

    def hex_scale(self, a, k):
        return self.CubeCoord(a.q * k, a.r * k, a.s * k)

    def hex_rotate_left(self, a):
        return self.CubeCoord(-a.s, -a.q, -a.r)

    def hex_rotate_right(self, a):
        return self.CubeCoord(-a.r, -a.s, -a.q)

    def hex_direction(self, direction):
        hex_directions = [self.CubeCoord(1, 0, -1), self.CubeCoord(1, -1, 0), self.CubeCoord(0, -1, 1),
                          self.CubeCoord(-1, 0, 1), self.CubeCoord(-1, 1, 0), self.CubeCoord(0, 1, -1)]

        return hex_directions[direction]

    def hex_neighbor(self, hex, direction):
        hex_directions = [self.CubeCoord(1, 0, -1), self.CubeCoord(1, -1, 0), self.CubeCoord(0, -1, 1),
                          self.CubeCoord(-1, 0, 1), self.CubeCoord(-1, 1, 0), self.CubeCoord(0, 1, -1)]

        return self.hex_add(hex, hex_directions[direction])

    def hex_diagonal_neighbor(self, hex, direction):
        hex_diagonals = [self.CubeCoord(2, -1, -1), self.CubeCoord(1, -2, 1), self.CubeCoord(-1, -1, 2),
                         self.CubeCoord(-2, 1, 1), self.CubeCoord(-1, 2, -1), self.CubeCoord(1, 1, -2)]

        return self.hex_add(hex, hex_diagonals[direction])

    def hex_length(self, hex):
        return (abs(hex.q) + abs(hex.r) + abs(hex.s)) // 2

    def hex_distance(self, a, b):
        return self.hex_length(self.hex_subtract(a, b))

    def hex_round(self, h):
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

        return self.CubeCoord(q, r, s)

    def hex_lerp(self, a, b, t):
        return self.CubeCoord(a.q * (1 - t) + b.q * t, a.r * (1 - t) + b.r * t, a.s * (1 - t) + b.s * t)

    def hex_linedraw(self, a, b):
        N = self.hex_distance(a, b)
        a_nudge = self.CubeCoord(a.q + 0.000001, a.r + 0.000001, a.s - 0.000002)
        b_nudge = self.CubeCoord(b.q + 0.000001, b.r + 0.000001, b.s - 0.000002)
        results = []
        step = 1.0 / max(N, 1)

        for i in range(0, N + 1):
            results.append(self.hex_round(self.hex_lerp(a_nudge, b_nudge, step * i)))

        return results

    def populate_board(self):
        board = {}
        # r and q switch for flat or pointy
        if self.hex_orientation == 'pointy':
            for r in range(self.hexcount[0]):
                r_offset = int(math.floor(r  / 2))
                for q in range(-r_offset, (self.hexcount[1] - r_offset) - 1):
                    # start in 0,0 + radius
                    board['{0}, {1}'.format(str(q), str(r))] = HexCell(
                        self.Point(q, r),
                        self.Layout(self.hex_orientation, self.hexsize, self.Point(0 + self.hexsize[0], 0 + self.hexsize[1]))
                    )
        else:
            for q in range(self.hexcount[1]):
                q_offset = int(math.floor(q / 2))
                for r in range(-q_offset, self.hexcount[0] - q_offset):
                    # start in 0,0 + radius
                    board['{0}, {1}'.format(str(q), str(r))] = HexCell(
                        self.Point(q, r),
                        self.Layout(self.hex_orientation, self.hexsize, self.Point(0 + self.hexsize[0], 0 + self.hexsize[1]))
                    )

        return board
