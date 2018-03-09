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
        self.surface = pygame.Surface(surface_size).convert()
        self.hexmap = HexMap(surface_size, cell_size)
        self.size = int(cell_size[0] - 2) # this is a magic number, we'll get a better radius method in optimization

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.bubble_map = pygame.sprite.Group()
        self.active_bubble = pygame.sprite.GroupSingle()
        self.next_bubble = pygame.sprite.GroupSingle()
        self.disloc_bubbles = pygame.sprite.Group()

        # debug
        self.dbgsurf = pygame.Surface(surface_size)
        self.dbgsurf.fill(pygame.Color(self.colorkey))
        self.dbgsurf.convert()
        for cell in self.hexmap.board.values():
            cell.paint(self.dbgsurf, color="grey")

    def update(self):
        self.surface.fill(pygame.Color(self.colorkey))

        # debug
        self.surface.blit(self.dbgsurf, (0, 0))

        try:
            if self.active_bubble:
                mv = self.active_bubble.sprite
                # TODO: replace this loop with a method that returns the colliding sprite list
                collision_list = pygame.sprite.spritecollide(mv, self.bubble_map, False)

                if collision_list:
                    # the idea here is to slow down, find the direction to the nearest sprite,
                    # and move the sprite until it touches at least two others
                    mv.set_velocity(0)

                    mv.grid_address = self.hexmap.get_celladdressbypixel(mv.rect.center)
                    # get cell containing colliding sprite
                    print("pixel_pos: {mv.grid_address}; grid_pos: {mv.}")

                    # move the active bubble to the map
                    self.bubble_map.add(mv)
                    self.active_bubble.remove(mv)

            # update and paint everything
            self.all_sprites.update()
            self.all_sprites.draw(self.surface)

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
                        address,
                        self.hexmap.board.get(address).get_pixelpos(),
                        self.surface.get_rect(),
                        self.size,
                        map_dict.get(address),
                        'BLACK'
                    )
                )

            self.all_sprites.add(self.bubble_map)
        except:
            raise
