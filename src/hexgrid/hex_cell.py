import collections, math
from abc import ABCMeta, abstractclassmethod

Point = collections.namedtuple("Point", ["x", "y"])
Hex = collections.namedtuple("Hex", ["q", "r", "s"])


class HexCell(object):

    def __init__(self, pos_x, pos_y, radius, layout) -> None:
        super().__init__()
        self.axialpos = Point(pos_x, pos_y)
        self.cubepos = Hex(pos_x, pos_y, -pos_x - pos_y)
        self.radius = radius
        self.__layout = layout

    def get_pixelpos(self) -> Point:
        return self.__hex_to_pixel__(self.__layout, self.cubepos)

    def __polygon_corners__(self, layout, h):
        corners = []
        center = self.__hex_to_pixel__(layout, h)
        for i in range(0, 6):
            offset = self.__hex_corner_offset__(layout, i)
            corners.append(Point(center.x + offset.x, center.y + offset.y))
        return corners

    @staticmethod
    def __hex_to_pixel__(layout, h):
        M = layout.orientation
        size = layout.size
        origin = layout.origin
        x = (M.f0 * h.q + M.f1 * h.r) * size.x
        y = (M.f2 * h.q + M.f3 * h.r) * size.y
        return Point(x + origin.x, y + origin.y)

    @staticmethod
    def __pixel_to_hex__(layout, p):
        M = layout.orientation
        size = layout.size
        origin = layout.origin
        pt = Point((p.x - origin.x) / size.x, (p.y - origin.y) / size.y)
        q = M.b0 * pt.x + M.b1 * pt.y
        r = M.b2 * pt.x + M.b3 * pt.y
        return Hex(q, r, -q - r)

    @staticmethod
    def __hex_corner_offset__(layout, corner):
        M = layout.orientation
        size = layout.size
        angle = 2.0 * math.pi * (M.start_angle - corner) / 6
        return Point(size.x * math.cos(angle), size.y * math.sin(angle))

    @abstractclassmethod
    def paint(self, surface):
        """
        Abstract method to blit the image representing this object to a pygame Surface.
        """
        pass
