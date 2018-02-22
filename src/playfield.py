import math
from itertools import chain
import pygame
import json
from pygame.math import Vector2
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

        # sprite groups
        self.bubble_map = pygame.sprite.Group()
        self.active_bubble = pygame.sprite.GroupSingle()
        self.disloc_bubbles = pygame.sprite.Group()

    def update(self):
        self.surface.fill(pygame.Color(self.colorkey))
        # debug
        for cell in self.hexmap.board.values():
            cell.paint(self.surface)

        try:
            if self.active_bubble:
                mv = self.active_bubble.sprite
                # TODO: replace this loop with a method that returns the colliding sprite list
                for bubble in self.bubble_map:
                    if pygame.sprite.collide_circle(mv, bubble):
                        mv.set_velocity(1)

                        # get current cell and lock bubble to it
                        cur_cell = self.hexmap.get_celladdressbypixel(mv.rect.center)
                        col_cell = self.hexmap.get_celladdressbypixel(bubble.rect.center)
                        col_nbor = None  # need to implement hex_ring(hex) for this
                        cur_cell_px_ctr = self.hexmap.get_pixeladdressbycell(cur_cell)
                        # get the direction from current position to cell center
                        dir_to = Vector2(mv.rect.center, cur_cell_px_ctr)
                        ang_to = mv.velocity.angle_to(dir_to)  # need to convert this to absolute degrees
                        if mv.rect.center != cur_cell_px_ctr:
                            # TODO: this *almost* works, but need to ensure the bubble anchors to at least 2 others
                            mv.set_velocity(0)
                            mv.velocity.rotate_ip(ang_to)
                            mv.set_position(cur_cell_px_ctr)
                            mv.update()

                        mv.set_velocity(0)
                        print("({0}) {1} -- ({2})".format(cur_cell, mv.rect.center, cur_cell_px_ctr))

                        self.bubble_map.add(mv)
                        self.active_bubble.remove(mv)

            for group in self.bubble_map, self.active_bubble:
                group.update()
                group.draw(self.surface)

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
