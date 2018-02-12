import math
import pygame
import random
from src.bubble import Bubble

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
        self.surface.convert()
        self.hexmap = HexMap(surface_size, cell_size)
        self.size = int(cell_size[0] - 2)
        self.bubble_map = pygame.sprite.Group()
        self.active_bubbles = pygame.sprite.Group()

    def update(self):
        self.surface.fill(pygame.Color(self.colorkey))

        try:
            for bubble in self.bubble_map and self.active_bubbles:
                bubble.update()
                self.surface.blit(bubble.image, bubble.rect)
        except:
            raise

    def get_surface(self):
        return self.surface

    def load_map(self, filepath):
        try:
            COLORS = ['ORANGE', 'YELLOW', 'GREEN', 'CYAN', 'BLUE', 'PINK', 'VIOLET']

            m = open(filepath, 'r').readline()
            addresses = m.split(';')

        except:
            raise SystemExit('Unable to read file located at {0}.'.format(filepath))

        try:
            for address in addresses:
                random.shuffle(COLORS)
                curr_clr = COLORS[0]

                self.bubble_map.add(
                    Bubble(
                        self.hexmap.board.get(address).get_pixelpos(),
                        self.surface.get_rect(),
                        self.size,
                        curr_clr,
                        'BLACK'
                    )
                )
        except:
            raise

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
                bubblecolor = COLORS[0]
                radius = int(cell.get_size().x) - 2
                pos = cell.get_pixelpos()

                pygame.draw.circle(surface, bubblecolor, pos, radius)

                if showcoords:
                    cell.paint(surface)

        return surface
