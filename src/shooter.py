import pygame, random
from pygame.math import Vector2
from pygame.locals import *
from src.constants import *


class Shooter(pygame.sprite.Sprite):

    def __init__(self, position, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((75, 75)).convert()  # temporary value
        self.rect = self.image.get_rect()
        self.rect.midbottom = position

        # Unique shooter properties
        self.angle = 90
        self.limits = (20, 160)

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