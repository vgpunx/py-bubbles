import math, pygame
import random

from src.hexamaplib.hex_map import HexMap
from pygame.locals import *


class Playfield:

    def __init__(self, surface_size, cell_size):
        """
        Renders a background and gameboard surface.

        :param surface_size: Size to use for the gameboard surface
        :type surface_size: Tuple (int, int)
        :param cell_size: Size to use for HexMap cell size
        :type cell_size: Tuple(int, int)
        """

        self.colorkey = (255, 0, 255)
        self.surface = pygame.Surface(surface_size)
        self.hexmap = HexMap(cell_size, surface_size)

    def update(self):
        self.surface.fill(self.colorkey)

    def get_surface(self):
        return self.surface

    def test(self):
        self.surface.fill(pygame.Color('WHITE'))
        COLORS = ['RED', 'ORANGE', 'YELLOW', 'GREEN', 'CYAN', 'BLUE', 'VIOLET']
        colcount = self.hexmap.cellcount.x
        rowcount = 4

        for i in range(colcount):
            for j in range(rowcount):
                address = '{0}, {1}'.format(i, j)
                cell = self.hexmap.board.get(address)
                clr = random.shuffle(COLORS)
                pygame.draw.circle(self.surface, pygame.Color(clr), cell.get_pixelpos(), cell.layout.size.x)
