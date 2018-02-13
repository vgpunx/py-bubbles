import collections
import math
# import sys
import pygame

Point = collections.namedtuple("Point", ["x", "y"])
CubeCoord = collections.namedtuple("Hex", ["q", "r", "s"])


# Definition of Orientation and Layout named tuples for reference only:
#     Orientation = collections.namedtuple("Orientation",
#           ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"])
#     Layout = collections.namedtuple("Layout", ["orientation", "size", "origin"])
#
# These are used in a few of the functions in this class, but they are intended to be passed in from a HexMap object.


class HexCell(object):

    def __init__(self, axial_coords, layout) -> None:
        super().__init__()
        self.Layout = collections.namedtuple("Layout", ["orientation", "size", "origin"])
        self.axialpos = axial_coords
        self.cubepos = CubeCoord(axial_coords.x, axial_coords.y, -axial_coords.x - axial_coords.y)
        self.layout = layout

    def get_pixelpos(self) -> Point:
        """
        Returns the pixel coordinate position of the center of this cell.
        """
        return self.__cube_to_pixel__(self.layout, self.cubepos)

    def get_size(self):
        return self.layout.size

    def get_polygon_corners(self, layout, cubecoord):
        """
        Calculate the polygon corners of a hex object in PIXEL COORDINATES.
        :param layout:  Named tuple with 3 fields.
        :param cubecoord: Named tuple with (q, r, s) fields.
        :return: Point list.
        """
        corners = []
        center = self.__cube_to_pixel__(layout, cubecoord)
        for i in range(0, 6):
            offset = self.__polygon_corner_offset__(layout, i)
            corners.append(Point(center.x + offset.x, center.y + offset.y))

        return corners

    def __polygon_corner_offset__(self, layout, corner):
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
    def __cube_to_pixel__(layout, cubecoord):
        """
        Convert cube hex coordinates to pixel position.
        :param layout: Named tuple with 3 fields.
        :param cubecoord: Named tuple with q, r, s fields.
        :return: Returns Point named tuple.
        """
        M = layout.orientation
        size = layout.size
        origin = layout.origin
        x = (M.f0 * cubecoord.q + M.f1 * cubecoord.r) * size.x
        y = (M.f2 * cubecoord.q + M.f3 * cubecoord.r) * size.y

        return Point(int(x + origin.x), int(y + origin.y))

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

    def paint(self, surface, color='black', width=2) -> pygame.Surface:
        """
        Method to paint a representation of the cell to a provided pygame surface.
        As currently written this is intended primarily for debugging.
        :surface: Pass in the object of class pygame.Surface to blit to.
        """

        pygame.draw.polygon(surface, pygame.Color(color), self.get_polygon_corners(self.layout, self.cubepos),
            width
        )
        font = pygame.font.Font(pygame.font.get_default_font(), 10)
        text = font.render('{0}, {1}'.format(self.axialpos.x, self.axialpos.y), False, pygame.Color("RED"))
        surface.blit(text, (self.get_pixelpos().x - (text.get_size()[0] / 2), self.get_pixelpos().y))

        return surface
