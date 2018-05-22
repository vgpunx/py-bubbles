import pygame, random
from pygame.math import Vector2
from pygame.locals import *
from src.constants import *


class Shooter(pygame.sprite.Sprite):

    def __init__(self, position, angle, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((100, 100)).convert()  # temporary value
        self.rect = self.image.get_rect()
        self.rect.bottomright = position
        self.angle = angle

        # parts
        self.__collection__ = self.__create_internalsprites__(pygame.sprite.LayeredUpdates()) # type: pygame.sprite.LayeredUpdates


        # placeholder image
        self.image.set_colorkey(pygame.Color('MAGENTA'))
        self.image.fill(pygame.Color('MAGENTA'))

        # animation stuff
        self.__flag_frame__ = 0

    def __str__(self):
        properties = ""  # type: str

        for sprite in self.__collection__:  # type: Shooter
            properties += "Layer: {0}\nRect: {1}\nTopLeft: {2}\n-------\n".format(sprite.layer, sprite.rect, sprite.rect.topleft)

        return properties

    def __create_internalsprites__(self, spritegroup):
        background = pygame.sprite.Sprite(spritegroup)
        wheel = pygame.sprite.Sprite(spritegroup)
        foreground = pygame.sprite.Sprite(spritegroup)

        foreground.layer = 2
        foreground.image = pygame.Surface((50, 50)).convert()
        foreground.rect = foreground.image.get_rect()
        foreground.image.fill(pygame.Color('BLUE'))

        wheel.layer = 1
        wheel.image = pygame.Surface((70, 70)).convert()
        wheel.image.fill(pygame.Color('MAGENTA'))
        wheel.image.set_colorkey(pygame.Color('MAGENTA'))
        wheel.rect = wheel.image.get_rect()

        pygame.draw.circle(
            wheel.image,            # surface
            pygame.Color('RED'),    # color
            [35, 35],               # center
            30                      # radius
        )
        pygame.draw.line(
            wheel.image,            # surface
            pygame.Color('BLACK'),  # color
            [35, 35],               # start
            [0, 35],                # end
            3                       # stroke width
        )

        background.layer = 0
        background.image = pygame.Surface((40, 20)).convert()
        background.rect = background.image.get_rect()
        background.image.fill(pygame.Color('GREEN'))

        background.rect.topleft = [10, 40]
        wheel.rect.topleft = [10, 30]
        foreground.rect.topleft = [0, 50]

        return spritegroup

    def update(self, *args):
        super().update(*args)
        # eng = self.__collection__.get_sprites_from_layer(0)[0]

        # if pygame.time.get_ticks() / 10 == 6:
        #     if self.__flag_frame__ == 0:
        #         eng.rect.center = (eng.rect.center[0], eng.rect.center[1] - 20)
        #         self.__flag_frame__ = 1
        #     else:
        #         eng.rect.center = (eng.rect.center[0], eng.rect.center[1] + 20)
        #         self.__flag_frame__ = 0


        self.__collection__.update()


    def kill(self):
        super().kill()

    def draw(self, surface):
        """

        :type surface: pygame.Surface
        """
        self.__collection__.draw(self.image)
        return surface.blit(self.image, self.rect.topleft)