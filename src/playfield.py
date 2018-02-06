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

        self.colorkey = 'WHITE'
        self.surface = pygame.Surface(surface_size)
        self.hexmap = HexMap(surface_size, cell_size)
        self.bubble_map = []

    def update(self):
        self.surface.fill(pygame.Color(self.colorkey))

    def get_surface(self):
        return self.surface

    def load_map(self, filepath):
        try:
            m = open(filepath, 'r').readline()
            self.bubble_map = m.split(';')
        except:
            raise SystemExit('Unable to read file located at {0}.'.format(filepath))

    def test(self, surface, bubble_map=None, showcoords=False):

        if self.bubble_map and bubble_map is None:
            this_map = self.bubble_map
        elif bubble_map is None:
            this_map = bubble_map
        else:
            this_map = None

        surface.fill(pygame.Color('WHITE'))

        COLORS = ['ORANGE', 'YELLOW', 'GREEN', 'CYAN', 'BLUE', 'PINK', 'VIOLET']

        if this_map is not None:
            for address in this_map:
                random.shuffle(COLORS)
                bubblecolor = pygame.Color(COLORS[0])
                cell = self.hexmap.board.get(address)
                radius = int(cell.get_size().x) - 2
                pos = cell.get_pixelpos()

                pygame.draw.circle(surface, bubblecolor, pos, radius)
                pygame.draw.circle(surface, pygame.Color('BLACK'), pos, radius, 2)

                if showcoords:
                    cell.paint(surface)

        else:
            for cell in self.hexmap.board.values():
                random.shuffle(COLORS)
                bubblecolor = pygame.Color(COLORS[0])
                radius = int(cell.get_size().x) - 2
                pos = cell.get_pixelpos()

                pygame.draw.circle(surface, bubblecolor, pos, radius)

                if showcoords:
                    cell.paint(surface)

        return surface
