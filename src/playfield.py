import math
import pygame
import json
import collections
from pygame.math import Vector2
from src.bubble import Bubble
from src.shooter import Shooter
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
        self.rect = self.surface.get_rect()
        self.hexmap = HexMap(surface_size, cell_size, hex_orientation='pointy')
        self.size = int(cell_size[0] - 2) # this is a magic number, we'll get a better radius method in optimization

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.bubble_map = pygame.sprite.Group()
        self.active_bubble = pygame.sprite.GroupSingle()
        self.next_bubble = pygame.sprite.GroupSingle()
        self.disloc_bubbles = pygame.sprite.Group()

        # shooter sprite
        self.shooter = Shooter(self.hexmap.board.get((-1, 14)).pixel_pos, 0, self.all_sprites)

        # debug
        # self.dbgsurf = pygame.Surface(surface_size)
        # self.dbgsurf.fill(pygame.Color(self.colorkey))
        # self.dbgsurf.convert()
        # for cell in self.hexmap.board.values():
        #     cell.paint(self.dbgsurf, color="grey")

    def update(self):
        self.surface.fill(pygame.Color(self.colorkey))

        # debug
        # self.surface.blit(self.dbgsurf, (0, 0))
        self.all_sprites.update()

        if self.active_bubble:
            try:
                self.process_collision()

            except:
                raise

        # update and paint everything
        self.all_sprites.draw(self.surface)
        self.shooter.draw(self.surface)

    def process_collision(self):
        mv = self.active_bubble.sprite
        collision_list = pygame.sprite.spritecollide(mv, self.bubble_map, False)

        if collision_list:
            # keep going until circle collision
            for spr in collision_list:
                if pygame.sprite.collide_circle(mv, spr):
                    # the idea here is to slow down, find the direction to the nearest sprite,
                    # and move the sprite until it touches at least two others
                    spr_neighbors = self.hexmap.hex_allneighbors(spr.grid_address)
                    mv_cur_address = self.hexmap.get_celladdressbypixel(mv.rect.center)

                    # correct rounding errors
                    if mv_cur_address not in spr_neighbors:
                        # TODO: Validate new address isn't already occupied or enclosed!
                        # make small adjustments to addr until we find the correct one
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
                    dest_cell = self.hexmap.board.get(mv.grid_address)

                    mv.set_velocity(0)
                    mv.set_position(dest_cell.get_pixelpos())
                    # move the active bubble to the map
                    self.bubble_map.add(mv)
                    self.active_bubble.remove(mv)

                continue

    def get_surface(self):
        return self.surface

    def load_map(self, filepath):
        try:
            map_toplevel = json.load(open(filepath, 'r'))
            map_width = map_toplevel['width']
            map_dict = map_toplevel['map']

        except:
            raise SystemExit('Unable to read file located at {0}.'.format(filepath))

        try:
            self.surface = pygame.Surface((map_width, self.surface.get_size()[1])).convert()
            self.rect = self.surface.get_rect()

            for address in map_dict:
                addr = address.split(", ")
                addr = (int(addr[0]), int(addr[1]))
                self.bubble_map.add(
                    # this is test code for now, just drawing bubbles with primitives
                    # later, the ADDRESS : TYPE json approach will be used to decide which sprite
                    # graphic to load and what special properties (if any) the bubble might have
                    Bubble(
                        addr,                                        # adress
                        self.hexmap.board.get(addr).get_pixelpos(),  # pixelpos
                        self.surface.get_rect(),                     # bounds
                        self.size,                                   # radius
                        map_dict.get(address),                       # fill_color
                        'BLACK',                                     # stroke_color
                        180,                                         # angle
                        0,                                           # velocity
                        (self.bubble_map, self.all_sprites)          # *groups
                    )
                )

            self.all_sprites.add(self.bubble_map)
        except:
            raise
