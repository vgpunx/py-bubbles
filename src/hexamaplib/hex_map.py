import math, collections, pygame
from src.hexamaplib.hex_cell import HexCell


# TODO: Implement a HexMap class, incorporate the below methods, and write the damn docstrings
class HexMap:

    def __init__(self, surface_size, cellsize, hex_orientation='flat'):

        """

        :param surface_size: Size of target Surface.
        :type surface_size: Tuple
        :param cellsize: Radii for hex cell size.
        :type cellsize: Tuple
        :param hex_orientation: Orientation of individual hexagon cells.
        :type hex_orientation: str
        """

        self.Orientation = collections.namedtuple("Orientation",
                                                  ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"])
        self.Layout = collections.namedtuple("Layout", ["orientation", "size", "origin"])
        self.Point = collections.namedtuple("Point", ["x", "y"])
        self.CubeCoord = collections.namedtuple("Hex", ["q", "r", "s"])

        self.surface_size = surface_size
        self.hextype = str.lower(hex_orientation)

        self.cellsize = self.Point(cellsize[0], cellsize[1])

        # Calculate cell count from cell size and surface size:
        # colcount = s / (Rc * 1.50)
        # rowcount = s / (math.sqrt(3) / 2) * (Ri * 2)
        colcount = self.cellsize.x * 1.5
        rowcount = (math.sqrt(3) / 2) * (self.cellsize.x * 2)

        if self.hextype == 'flat':
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

            self.cellcount = self.Point(int(self.surface_size[0] / colcount),
                                            int(self.surface_size[1] / rowcount))

        elif self.hextype == 'pointy':
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

            self.cellcount = self.Point(int(self.surface_size[0] / rowcount),
                                            int(self.surface_size[1] / colcount))

        else:
            raise Exception('Value of hex_orientation must be either "flat" or "pointy."')

        self.board = self.populate_board()

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

    def hex_neighbor(self, cell, direction):
        hex_directions = [self.CubeCoord(1, 0, -1), self.CubeCoord(1, -1, 0), self.CubeCoord(0, -1, 1),
                          self.CubeCoord(-1, 0, 1), self.CubeCoord(-1, 1, 0), self.CubeCoord(0, 1, -1)]

        return self.hex_add(cell, hex_directions[direction])

    def hex_diagonal_neighbor(self, cell, direction):
        hex_diagonals = [self.CubeCoord(2, -1, -1), self.CubeCoord(1, -2, 1), self.CubeCoord(-1, -1, 2),
                         self.CubeCoord(-2, 1, 1), self.CubeCoord(-1, 2, -1), self.CubeCoord(1, 1, -2)]

        return self.hex_add(cell, hex_diagonals[direction])

    def hex_length(self, cell):
        return (abs(cell.q) + abs(cell.r) + abs(cell.s)) // 2

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
            # TODO: Fix this part, it's still not producing a rectangular map
            for r in range(self.cellcount.y):
                r_offset = int(math.floor(r / 2))
                for q in range(-r_offset, (self.cellcount.x - r_offset) - 1):
                    # start in 0,0 + radius
                    board['{0}, {1}'.format(str(q), str(r))] = HexCell(
                        self.Point(q, r),
                        self.Layout(self.hex_orientation, self.cellsize,
                                    self.Point(self.cellsize[0], self.cellsize[1]))
                    )
        else:
            for q in range(self.cellcount.x):
                q_offset = int(math.floor(q / 2))
                for r in range(-q_offset, self.cellcount.y - q_offset):
                    # start in 0,0 + radius
                    board['{0}, {1}'.format(str(q), str(r))] = HexCell(
                        self.Point(q, r),
                        self.Layout(self.hex_orientation, self.cellsize,
                                    self.Point(0 + self.cellsize[0], 0 + self.cellsize[1]))
                    )

        return board
