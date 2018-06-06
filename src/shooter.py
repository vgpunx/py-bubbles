import pygame, random
from pygame.math import Vector2
from src.bubble import Bubble
from pygame.locals import *
from src.constants import *


class Shooter(pygame.sprite.Sprite):

    def __init__(self, position, bubble_origin_addr, bubble_origin_pos, bubble_radius, bubble_map, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((75, 75)).convert()  # temporary value
        self.rect = self.image.get_rect()
        self.rect.midbottom = position

        # Unique shooter properties
        self.angle = 90
        self.limits = (20, 160)
        self._rng = random.Random()
        # TODO: remember to add to playfield spritegroups when changed
        self.next = pygame.sprite.GroupSingle()
        # stored copy of bubble properties
        self._bubble_origin_addr = bubble_origin_addr
        self._bubble_origin_pos = bubble_origin_pos
        self._bubble_radius = bubble_radius
        self._bubble_map = bubble_map  # needed to access get_present_types()

        # placeholder image
        self.image.set_colorkey(pygame.Color('MAGENTA'))
        self.image.fill(pygame.Color('MAGENTA'))
        pygame.draw.polygon(
            self.image,
            pygame.Color("BLUE"),
            [
                (37, 0),
                (75, 75),
                (0, 75),
                (37, 0)
            ]
        )

        # animation stuff
        self._orig_img = pygame.transform.rotate(self.image, -self.angle)
        self._orig_rect = self._orig_img.get_rect()

    def update(self, *args):
        super().update(*args)
        self.image = pygame.transform.rotate(self._orig_img, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if not self.next.sprite:
            self._generate_next(
                self._bubble_origin_addr,
                self._bubble_origin_pos,
                self._bubble_radius,
                self._bubble_map,
                self.next
            )

    def _generate_next(self, start_axial, start_pos, radius, bubble_map, *groups):
        """
        Generates the next Bubble to be fired.  Weighted toward colors/types already present in map.

        :type start_pos: tuple
        :type start_axial: tuple
        :type radius: int
        :type bubble_map: src.bubblemap.BubbleMap
        :return: None
        """

        # probably that this will generate a color that is not currently already present in the map
        rbc = 5

        # colors present in map
        cpc = bubble_map.get_present_types()

        # colors not present in map
        diff = [item for item in ALL_TYPEPROPERTIES if item not in cpc]

        # ran-dumb in
        ri = self._rng.randint(0, 100)

        if ri <= rbc:
            Bubble(
                start_axial,                # address
                start_pos,                  # pixelpos
                radius,                     # radius
                self._rng.choice(diff),     # fill_color
                'BLACK',                    # stroke_color
                self.angle,                 # angle
                0,                          # velocity
                *groups                     # *groups
            )

        else:
            Bubble(
                start_axial,                # address
                start_pos,                  # pixelpos
                radius,                     # radius
                self._rng.choice(cpc),      # fill_color
                'BLACK',                    # stroke_color
                self.angle,                 # angle
                0,                          # velocity
                *groups                     # *groups
            )

    def fire(self, velocity, *groups):
        self.next.sprite.set_position(self._bubble_origin_addr, self.rect.center)
        self.next.sprite.set_velocity(velocity)
        self.next.sprite.set_angle(self.angle)
        self.next.sprite.add(*groups)
        self.next.empty()

    def kill(self):
        super().kill()

    def rotate(self, angle):
        newangle = self.angle + angle

        if newangle < self.limits[0]:
            newangle = self.limits[0]

        elif newangle > self.limits[1]:
            newangle = self.limits[1]

        self.angle = newangle

        # TODO: spritesheet based animation, once i have some artwork

    def draw(self, surface):
        """

        :type surface: pygame.Surface
        """

        res = surface

        res.blit(self.image, self.rect.topleft)

        if DEBUG:
            debug_text = pygame.font.Font(pygame.font.get_default_font(), 14).render(
                "{0} deg".format(self.angle), True, pygame.Color("WHITE"))

            res.blit(debug_text, (self.rect.left + 18, self.rect.bottom - 20))

        return res