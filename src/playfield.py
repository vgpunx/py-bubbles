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
        self.hexmap = HexMap(surface_size, cell_size)

    def update(self):
        self.surface.fill(self.colorkey)

    def get_surface(self):
        return self.surface

    def test(self, surface):
        surface.fill(pygame.Color('WHITE'))

        COLORS = ['ORANGE', 'YELLOW', 'GREEN', 'CYAN', 'BLUE', 'PINK', 'VIOLET']

        for cell in self.hexmap.board.values():
            random.shuffle(COLORS)
            color = pygame.Color(COLORS[0])
            radius = int(cell.get_size().x) - 2
            pos = cell.get_pixelpos()

            pygame.draw.circle(surface, color, pos, radius)
            #cell.paint(surface)

        return surface
