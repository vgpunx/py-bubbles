import math
import pygame
import json
import collections
from pygame.math import Vector2
from src.bubble import Bubble
from src.shooter import Shooter
from src.hexamaplib.hex_map import HexMap
from src.constants import *
from pygame.locals import *


class Playfield:

    def __init__(self, map_file_path, cell_size):
        """
        Renders a background and gameboard surface.

        :param surface_size: Size to use for the gameboard surface
        :type surface_size: Tuple (int, int)
        :param cell_size: Size to use for HexMap cell size
        :type cell_size: Tuple(int, int)
        """

        self.colorkey = 'WHITE'
        # self.image = pygame.Surface(surface_size).convert()
        # self.rect = self.image.get_rect()
        # self.area_params = DISP_SIZE[1] * 0.98
        #
        # self.hexmap = HexMap(surface_size, cell_size, hex_orientation='pointy')

        self.cell_size = cell_size
        self.cell_radius = int(cell_size[0] - 2) # this is a magic number, we'll get a better radius method in optimization

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.bubble_map = pygame.sprite.Group()
        self.active_bubble = pygame.sprite.GroupSingle()
        self.next_bubble = pygame.sprite.GroupSingle()
        self.disloc_bubbles = pygame.sprite.Group()

        self.load_map(map_file_path)

    def update(self):
        self.image.fill(pygame.Color(self.colorkey))

        # debug
        if DEBUG:
            self.image.blit(self.dbgsurf, (0, 0))

        self.all_sprites.update()

        if self.active_bubble:
            self.process_collision()

        # update and paint everything
        self.all_sprites.draw(self.image)
        self.shooter.draw(self.image)


    def process_collision(self):
        mv = self.active_bubble.sprite

        # check for boundary collision and bounce
        if mv.rect.top < 0:
            mv.bounce(Vector2(1, 0))
            return
        elif mv.rect.left < 0 or mv.rect.right > self.rect.width:
            mv.bounce(Vector2(0, 1))
            return

        collision_list = pygame.sprite.spritecollide(mv, self.bubble_map, False)

        if collision_list:
            # keep going until circle collision
            for spr in collision_list:
                if pygame.sprite.collide_circle(mv, spr):
                    # the idea here is to slow down, find the direction to the nearest sprite,
                    # and move the sprite until it touches at least two others
                    spr_neighbors = self.hexmap.hex_allneighbors(spr.grid_address)
                    mv_cur_address = self.hexmap.get_celladdressbypixel(mv.rect.center)

                    # if mv_cur_address in spr_neighbors \
                    #     and not self.__test_occupied__(mv_cur_address) \
                    #     and not self.__test_surrounded__(mv_cur_address):
                    #     break

                    # correct rounding errors
                    if mv_cur_address not in spr_neighbors:
                        # TODO: Validate new address isn't already occupied or enclosed!
                        # make small adjustments to addr until we find the correct one
                        for i in (1, -1):
                            test0 = (mv_cur_address[0] + i, mv_cur_address[1])
                            test1 = (mv_cur_address[0], mv_cur_address[1] + i)

                            if self.__test_shared_rings__(test0, spr.grid_address) \
                                    and not self.__test_occupied__(test0) \
                                    and not self.__test_surrounded__(test0):
                                mv_cur_address = test0
                                break
                            elif self.__test_shared_rings__(test1, spr.grid_address) \
                                    and not self.__test_occupied__(test1) \
                                    and not self.__test_surrounded__(test1):
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

    def __test_shared_rings__(self, celladdr_1, celladdr_2):
        """
        Validates two cells share neighborhood rings.
        :param celladdr_1: Tuple
        :param celladdr_2: Tuple
        :return: boolean
        """
        cell_1_neighbors = self.hexmap.hex_allneighbors(celladdr_1)
        cell_2_neighbors = self.hexmap.hex_allneighbors(celladdr_2)

        if celladdr_1 in cell_2_neighbors and celladdr_2 in cell_1_neighbors:
            return True


        return False


    def __test_occupied__(self, celladdr):
        """
        Validates a cell is occupied by a Bubble.
        :param celladdr: Tuple
        :return: boolean
        """

        return isinstance(self.hexmap.board.get(celladdr), Bubble)


    def __test_surrounded__(self, celladdr):
        """
        Validates a cell is surrounded by Bubbles.
        :param celladdr: Tuple
        :return: boolean
        """

        ring = self.hexmap.hex_allneighbors(celladdr)
        counter = 0

        for celladdr in ring:
            if isinstance(self.hexmap.board.get(celladdr), Bubble):
                counter += 1

        if counter == 5:
            return True

        return False


    def get_surface(self):
        return self.image

    def load_map(self, filepath):
        try:
            map_toplevel = json.load(open(filepath, 'r'))
            map_width = map_toplevel['width']
            map_height = map_toplevel['height']
            map_dict = map_toplevel['map']

        except:
            raise SystemExit('Unable to read file located at {0}.'.format(filepath))

        try:
            # reset affected properties
            #debug
            if DEBUG:
                print("Loading map...")

            self.image = pygame.Surface((map_width, map_height)).convert()
            self.area_params = self.image.get_size()
            self.rect = self.image.get_rect()
            self.hexmap = HexMap(self.area_params, self.cell_size, hex_orientation='pointy')

            # shooter sprite
            shooter_pos = self.rect.midbottom
            self.shooter = Shooter(shooter_pos, 0, self.all_sprites)

            # debug
            if DEBUG:
                print("Playfield dimensions: {0}".format(self.area_params))
                print(self.shooter)
                self.dbgsurf = pygame.Surface(self.area_params)
                self.dbgsurf.fill(pygame.Color(self.colorkey))
                self.dbgsurf.convert()
                for cell in self.hexmap.board.values():
                    cell.paint(self.dbgsurf, color="grey")

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
                        self.cell_radius,                            # radius
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
