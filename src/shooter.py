import pygame, random
from pygame.math import Vector2
from pygame.locals import *
from src.constants import *


class Shooter(pygame.sprite.Sprite):
    def __init__(self, position, angle, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((50, 100)).convert()  # temporary value
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.angle = angle

        # placeholder image
        self.image.set_colorkey(pygame.Color('MAGENTA'))
        self.image.fill(pygame.Color('MAGENTA'))

        pygame.draw.polygon(
            self.image,
            pygame.Color('BLACK'),
            [[0, 100], [25, 0], [50, 100]],
            5
        )


    def update(self, *args):
        super().update(*args)
        pygame.transform.rotate(self.image, self.angle)

    def kill(self):
        super().kill()

