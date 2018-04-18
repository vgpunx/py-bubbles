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
        self.__collection__ = self.__create_internalsprites__(pygame.sprite.LayeredUpdates())


        # placeholder image
        self.image.set_colorkey(pygame.Color('MAGENTA'))
        self.image.fill(pygame.Color('MAGENTA'))

    def __create_internalsprites__(self, spritegroup):
        foreground = pygame.sprite.Sprite(spritegroup)
        wheel = pygame.sprite.Sprite(spritegroup)
        background = pygame.sprite.Sprite(spritegroup)

        foreground.layer = 2
        foreground.image = pygame.Surface((50, 50)).convert()
        foreground.rect = foreground.image.get_rect()
        foreground.rect.topleft = [50, 13]
        foreground.image.fill(pygame.Color('BLUE'))

        wheel.layer = 1
        wheel.image = pygame.Surface((72, 72)).convert()
        wheel.rect = wheel.image.get_rect()
        wheel.rect.center = [foreground.rect.topright[0] - 10,
                                      foreground.rect.topright[1] - 10]
        pygame.draw.circle(
            wheel.image,
            pygame.Color('RED'),
            (36, 36),
            60,
            3
        )
        pygame.draw.line(
            wheel.image,
            pygame.Color('BLACK'),
            (36, 36),
            (0, 36),
            3
        )

        background.layer = 0
        background.image = pygame.Surface((45, 30)).convert()
        background.rect = background.image.get_rect()
        background.image.fill(pygame.Color('GREEN'))
        pygame.transform.rotate(background.image, 22)

        return spritegroup

    def update(self, *args):
        super().update(*args)

    def kill(self):
        super().kill()

    def draw(self, surface):
        return self.__collection__.draw(surface)