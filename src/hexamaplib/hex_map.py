import math, collections
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

        if hex_orientation.lower() not in ('flat', 'pointy'):
            raise ValueError('Argument hex_orientation must be one of (flat, pointy).')

        self.hextype = hex_orientation.lower()
        self.cellsize = self.Point(cellsize[0], cellsize[1])

        # hex center offset from the 0,0 pixel position
        self.origin = self.cellsize

        # Calculate cell count from cell size and surface size:
        # colcount = s / (Rc * 1.50)
        # rowcount = s / (math.sqrt(3) / 2) * (Ri * 2)
        colcount = int(self.cellsize.x * 1.5)
        rowcount = int((math.sqrt(3) / 2) * (self.cellsize.x * 2))

        if self.hextype == 'flat':
            self.hex_orientation = self.Orientation(
                3.0 / 2.0,              # f0
                0.0,                    # f1
                math.sqrt(3.0) / 2.0,   # f2
                math.sqrt(3.0),         # f3
                2.0 / 3.0,              # b0
                0.0,                    # b1
                -1.0 / 3.0,             # b2
                math.sqrt(3.0) / 3.0,   # b3
                0.0                     # start_angle
            )

            self.cellcount = self.Point(int(self.surface_size[0] // colcount),
                                        int(self.surface_size[1] // rowcount))

        elif self.hextype == 'pointy':
            self.hex_orientation = self.Orientation(
                math.sqrt(3.0),         # f0
                math.sqrt(3.0) / 2.0,   # f1
                0.0,                    # f2
                float(3.0 / 2.0),              # f3
                math.sqrt(3.0) / 3.0,   # b0
                -1.0 / 3.0,             # b1
                0.0,                    # b2
                float(2.0 / 3.0),              # b3
                float(0.5)                     # start_angle
            )

            self.cellcount = self.Point(int(self.surface_size[0] // rowcount),
                                        int(self.surface_size[1] // colcount))

        else:
            raise Exception('Value of hex_orientation must be either "flat" or "pointy."')

        self.board = self.populate_board()

    def get_celladdressbypixel(self, pixel_coords):
        """
        Convert pixel coordinates to hex cube position.
        :param layout:
        :param pixel_coords:
        :return:
        """
        M = self.hex_orientation
        size = self.cellsize
        origin = self.origin
        pt = self.Point(
            (pixel_coords[0] - origin.x) / size.x,
            (pixel_coords[1] - origin.y) / size.y
        )
        q = (M.b0 * pt.x) + (M.b1 * pt.y)
        r = (M.b2 * pt.x) + (M.b3 * pt.y)

        rslt = self.hex_round(self.CubeCoord(q, r, -q - r))

        return rslt.q, rslt.r

    def get_pixeladdressbycell(self, cubecoord):
        """
        Convert cube hex coordinates to pixel position.
        :param layout: Named tuple with 3 fields.
        :param cubecoord: Named tuple with q, r, s fields.
        :return: Returns Point named tuple.
        """
        M = self.hex_orientation
        size = self.cellsize
        origin = self.origin
        x = (M.f0 * cubecoord[0] + M.f1 * cubecoord[1]) * size.x
        y = (M.f2 * cubecoord[0] + M.f3 * cubecoord[1]) * size.y

        return int(x + origin.x), int(y + origin.y)

    def find_cell_by_pixel(self, pixel_address):
        for cell in self.board.values():
            if cell.pixel_pos == pixel_address:
                return cell

        return None

    def hex_add(self, a, b):
        return self.CubeCoord(a.q + b.q, a.r + b.r, a.s + b.s)

    def axial_add(self, a, b):
        a_cube = self.CubeCoord(a[0], a[1], -a[0] - a[1])
        b_cube = self.CubeCoord(b[0], b[1], -b[0] - b[1])

        cube_res = self.hex_add(a_cube, b_cube)

        return cube_res.q, cube_res.r

    def hex_subtract(self, a, b):
        return self.CubeCoord(a.q - b.q, a.r - b.r, a.s - b.s)

    def axial_subtract(self, a, b):
        a_cube = self.CubeCoord(a[0], a[1], -a[0] - a[1])
        b_cube = self.CubeCoord(b[0], b[1], -b[0] - b[1])

        cube_res = self.hex_subtract(a_cube, b_cube)

        return cube_res.q, cube_res.r

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

    def hex_allneighbors(self, cell):
        cell_cube = self.CubeCoord(cell[0], cell[1], -cell[0] - cell[1])
        result = []

        for i in range(6):
            c = self.hex_neighbor(cell_cube, i)
            result.append((c.q, c.r))

        return result

    def hex_diagonal_neighbor(self, cell, direction):
        hex_diagonals = [self.CubeCoord(2, -1, -1), self.CubeCoord(1, -2, 1), self.CubeCoord(-1, -1, 2),
                         self.CubeCoord(-2, 1, 1), self.CubeCoord(-1, 2, -1), self.CubeCoord(1, 1, -2)]

        return self.hex_add(cell, hex_diagonals[direction])

    def hex_length(self, cell):
        return (abs(cell.q) + abs(cell.r) + abs(cell.s)) // 2

    def hex_distance(self, a, b):
        return self.hex_length(self.hex_subtract(a, b))

    def hex_round(self, cell):
        qi = int(round(cell.q))
        ri = int(round(cell.r))
        si = int(round(cell.s))
        q_diff = abs(qi - cell.q)
        r_diff = abs(ri - cell.r)
        s_diff = abs(si - cell.s)

        if q_diff > r_diff and q_diff > s_diff:
            qi = -ri - si
        else:
            if r_diff > s_diff:
                ri = -qi - si
            else:
                si = -qi - ri

        return self.CubeCoord(qi, ri, si)

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

    def __test_fit__(self, cell, area):
        """
        Tests a cell's pixel position to validate it fits within the provided area.

        :param cell: Hexcell
        :param area: Tuple
        :param orientation:
        :return: boolean
        """

        if self.hextype == "pointy":
            test_cellsize = self.Point(self.cellsize[0] * 0.75, self.cellsize[1])

        elif self.hextype == "flat":
            test_cellsize = self.Point(self.cellsize[0], self.cellsize[1] * 0.75)

        else:
            raise AttributeError("Value for parameter 'orientation' must be one of ('pointy', 'flat').")

        return cell.pixel_pos.x + test_cellsize.x < area[0] and cell.pixel_pos.y + test_cellsize.y < area[1]

    def populate_board(self):
        board = {}
        # r and q switch for flat or pointy
        if self.hextype == 'pointy':
            # TODO: Fix this part, it's still not producing a rectangular map
            for r in range(self.cellcount.y ):
                r_offset = r >> 1  # int(math.floor(r / 2))
                for q in range(-r_offset, self.cellcount.x - r_offset):
                    # start in 0,0 + radius
                    newcell = HexCell(
                        self.Point(q, r),
                        self.Layout(self.hex_orientation, self.cellsize, self.origin)
                    )

                    # test fit
                    if self.__test_fit__(newcell, self.surface_size):
                        board[(q, r)] = newcell

                    continue

        elif self.hextype == 'flat':
            for q in range(self.cellcount.x):
                q_offset = int(math.floor(q / 2))
                for r in range(-q_offset, self.cellcount.y - q_offset):
                    # start in 0,0 + radius
                    newcell = HexCell(
                        self.Point(q, r),
                        self.Layout(self.hex_orientation, self.cellsize, self.origin)
                    )

                    # test fit
                    if self.__test_fit__(newcell, self.surface_size):
                        board[(q, r)] = newcell

                    continue

        return board
