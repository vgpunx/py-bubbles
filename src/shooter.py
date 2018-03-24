import pygame, random
from pygame.math import Vector2
from pygame.locals import *
from src.constants import *


class Shooter(pygame.sprite.Sprite):
    def __init__(self, position, angle, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((100, 100)).convert()  # temporary value
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.angle = angle

        # parts
        self.__collection__ = pygame.sprite.LayeredUpdates()


        # placeholder image
        self.image.set_colorkey(pygame.Color('MAGENTA'))
        self.image.fill(pygame.Color('MAGENTA'))

    def __create_internalsprites__(self):
        self.__foreground__ = pygame.sprite.Sprite()
        self.__wheel__ = pygame.sprite.Sprite()
        self.__background__ = pygame.sprite.Sprite()

        self.__foreground__.layer = 2
        self.__foreground__.image = pygame.Surface((50, 50)).convert()
        self.__foreground__.rect = self.__foreground__.image.get_rect()
        self.__foreground__.rect.topleft = [50, 13]
        self.__foreground__.image.fill(pygame.Color('BLUE'))

        self.__wheel__.layer = 1
        self.__wheel__.image = pygame.Surface((72, 72)).convert()
        self.__wheel__.rect = self.__wheel__.image.get_rect()
        self.__wheel__.rect.center = [self.__foreground__.topright[0] - 10, self.__foreground__.topright[1] - 10]
        pygame.draw.circle(
            self.__wheel__.image,
            pygame.Color('RED'),
            (36, 36),
            60,
            3
        )
        pygame.draw.line(
            self.__wheel__.image,
            pygame.Color('BLACK'),
            (36, 36),
            (0, 36),
            3
        )

        self.__background__.layer = 0
        self.__background__.image = pygame.Surface((45, 30)).convert()
        self.__background__.rect = self.__background__.image.get_rect()
        self.__background__.image.fill(pygame.Color('GREEN'))
        pygame.transform.rotate(self.__background__.image, 22)

    def update(self, *args):
        super().update(*args)

    def kill(self):
        super().kill()

