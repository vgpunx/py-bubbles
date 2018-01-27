import collections, math
from abc import ABCMeta, abstractclassmethod

Point = collections.namedtuple("Point", ["x", "y"])
CubeCoord = collections.namedtuple("Hex", ["q", "r", "s"])

# Definition of Orientation and Layout named tuples for reference only:
#     Orientation = collections.namedtuple("Orientation", ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"])
#     Layout = collections.namedtuple("Layout", ["orientation", "size", "origin"])
#
# These are used in a few of the functions in this class, but they are intended to be passed in from a HexMap object.

class HexCell(object):

    def __init__(self, pos_x, pos_y, radius, layout) -> None:
        super().__init__()
        self.axialpos = Point(pos_x, pos_y)
        self.cubepos = CubeCoord(pos_x, pos_y, -pos_x - pos_y)
        self.radius = radius
        self.__layout = layout

    def get_pixelpos(self) -> Point:
        """
        Returns the pixel coordinate position of this object.
        """
        return self.__cube_to_pixel__(self.__layout, self.cubepos)

    def __polygon_corners__(self, layout, hex):
        """
        Calculate the polygon corners of a hex object in PIXEL COORDINATES.
        :param layout:  Named tuple with 3 fields.
        :param hex: Named tuple with (q, r, s) fields.
        :return: Point list.
        """
        corners = []
        center = self.__cube_to_pixel__(layout, hex)
        for i in range(0, 6):
            offset = self.__polygon_corner_offset__(layout, i)
            corners.append(Point(center.x + offset.x, center.y + offset.y))
        return corners

    def __polygon_corner_offset__(layout, corner):
        """
        Calculate polygon corner offset from center.
        :param layout: Named tuple with 3 fields.
        :param corner: Integer representing which corner to calculate.
        :return: Point(x, y)
        """
        M = layout.orientation
        size = layout.size
        angle = 2.0 * math.pi * (M.start_angle - corner) / 6
        return Point(size.x * math.cos(angle), size.y * math.sin(angle))

    @staticmethod
    def __cube_to_pixel__(layout, hex):
        """
        Convert cube hex coordinates to pixel position.
        :param layout: Named tuple with 3 fields.
        :param hex: Named tuple with q, r, s fields.
        :return: Returns Point named tuple.
        """
        M = layout.orientation
        size = layout.size
        origin = layout.origin
        x = (M.f0 * hex.q + M.f1 * hex.r) * size.x
        y = (M.f2 * hex.q + M.f3 * hex.r) * size.y
        return Point(x + origin.x, y + origin.y)

    @staticmethod
    def __pixel_to_cube__(layout, pixel_coords):
        """
        Convert pixel coordinates to hex cube position.
        :param layout:
        :param pixel_coords:
        :return:
        """
        M = layout.orientation
        size = layout.size
        origin = layout.origin
        pt = Point((pixel_coords.x - origin.x) / size.x, (pixel_coords.y - origin.y) / size.y)
        q = M.b0 * pt.x + M.b1 * pt.y
        r = M.b2 * pt.x + M.b3 * pt.y
        return CubeCoord(q, r, -q - r)

    @abstractclassmethod
    def paint(self, surface):
        """
        Abstract method to blit the image representing this object to a pygame Surface.
        """
        pass
