import math
from itertools import chain
import pygame
import json
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
        self.size = int(cell_size[0] - 2) # this is a magic number, we'll get a better radius method in optimization
        self.bubble_map = pygame.sprite.Group()
        self.active_bubbles = pygame.sprite.Group()

    def update(self):
        self.surface.fill(pygame.Color(self.colorkey))

        try:
            if len(self.active_bubbles) > 0:
                fired_bubble = self.active_bubbles.sprites()[0]
            else:
                fired_bubble = None

            for bubble in chain(self.bubble_map, self.active_bubbles):
                bubble.update()

                if fired_bubble:
                    if pygame.sprite.collide_circle(fired_bubble, bubble):
                        #fired_bubble.set_velocity(0)
                        # this code doesn't work
                        print("collision with bubble at {0}".format(bubble.pos))
                        self.bubble_map.add(fired_bubble)
                        self.active_bubbles.remove(fired_bubble)

                self.surface.blit(bubble.image, bubble.rect)
        except:
            raise

    def get_surface(self):
        return self.surface

    def load_map(self, filepath):
        try:
            map_dict = json.load(open(filepath, 'r'))

        except:
            raise SystemExit('Unable to read file located at {0}.'.format(filepath))

        try:
            for address in map_dict:
                self.bubble_map.add(
                    # this is test code for now, just drawing bubbles with primitives
                    # later, the ADDRESS : TYPE json approach will be used to decide which sprite
                    # graphic to load and what special properties (if any) the bubble might have
                    Bubble(
                        self.hexmap.board.get(address).get_pixelpos(),
                        self.surface.get_rect(),
                        self.size,
                        map_dict.get(address),
                        'BLACK'
                    )
                )
        except:
            raise
