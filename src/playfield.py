import math
import pygame
import json
import collections
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

        self.all_sprites.update()

        try:
            if self.active_bubble:
                mv = self.active_bubble.sprite
                collision_list = pygame.sprite.spritecollide(mv, self.bubble_map, False)

                if collision_list:
                    # keep going until circle collision
                    for spr in collision_list:
                        #  debug
                        print("rect collision with: {0}".format(spr.rect.center))

                        if pygame.sprite.collide_circle(mv, spr):
                            # the idea here is to slow down, find the direction to the nearest sprite,
                            # and move the sprite until it touches at least two others

                            # debug
                            print("circ collision with: {0}".format(spr.grid_address))
                            mv.set_velocity(0)

                            # get the address of the colliding sprite
                            # and calculate our address based on it
                            spr_neighbors = self.hexmap.hex_allneighbors(spr.grid_address)
                            mv_cur_address = self.hexmap.get_celladdressbypixel(mv.rect.center)

                            if mv_cur_address not in spr_neighbors:
                                print("ROUND_ERROR")
                                # make small adjustments to addr until true
                                for i in (1, -1):
                                    test0 = (mv_cur_address[0] + i, mv_cur_address[1])
                                    test1 = (mv_cur_address[0], mv_cur_address[1] + i)
                                    if test0 in spr_neighbors:
                                        mv_cur_address = test0
                                        break
                                    elif test1 in spr_neighbors:
                                        mv_cur_address = test1
                                        break

                            mv.grid_address = mv_cur_address
                            mv.set_position(self.hexmap.board.get(mv.grid_address).pixel_pos)
                            # move the active bubble to the map
                            self.bubble_map.add(mv)
                            self.active_bubble.remove(mv)

                            # get cell containing colliding sprite

                            # debug
                            print(spr_neighbors)
                            print("pixel_pos: {1}; grid_pos: {0}".format(mv.grid_address, mv.pos))

                        continue

            # update and paint everything
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
                addr = address.split(", ")
                addr = (int(addr[0]), int(addr[1]))
                self.bubble_map.add(
                    # this is test code for now, just drawing bubbles with primitives
                    # later, the ADDRESS : TYPE json approach will be used to decide which sprite
                    # graphic to load and what special properties (if any) the bubble might have
                    Bubble(
                        addr,
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
