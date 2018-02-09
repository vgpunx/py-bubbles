import math
import pygame
from pygame.math import Vector2


class Bubble(pygame.sprite.Sprite):

    def __init__(self, pos, bounds, radius, fill_color, stroke_color, *groups, angle=90, velocity=0):
        super().__init__(*groups)
        self.image = pygame.transform.rotate(pygame.Surface((radius * 2, radius * 2)), -angle)
        self.image.set_colorkey(pygame.Color('MAGENTA'))

        offset = Vector2(radius, -radius).rotate(angle)
        self.pos = Vector2(pos) - offset
        self.velocity = Vector2(1, 0).rotate(angle) * velocity
        self.angle = angle
        self.rect = self.image.get_rect(center=pos)
        self.bounds = bounds

        # for drawing placeholder images
        # this will be replaced with actual image code later
        self.radius = radius
        self.rect = self.image.get_rect()
        self.fill = pygame.Color(fill_color)
        self.stroke = pygame.Color(stroke_color)

        self.draw()

    def add(self, *groups):
        super().add(*groups)

    def remove(self, *groups):
        super().remove(*groups)

    def add_internal(self, group):
        super().add_internal(group)

    def remove_internal(self, group):
        super().remove_internal(group)

    def update(self, *args):
        super().update(*args)
        if self.alive():
            self.move()
            self.rect.center = self.pos
            self.bounce()

    def kill(self):
        super().kill()

    def groups(self):
        return super().groups()

    def alive(self):
        return super().alive()

    def __repr__(self):
        return super().__repr__()

    def draw(self):
        # placeholder code
        self.image.fill(pygame.Color('MAGENTA'))
        pygame.draw.circle(self.image, self.fill, self.image.get_rect().center, self.radius)  # filled cir
        pygame.draw.circle(self.image, self.stroke, self.image.get_rect().center, self.radius, 2)  # stroke
        self.image.convert()

    def move(self):
        # if self.angle <= 90:
        #     radians = math.radians(self.angle)
        #     self.pos[0] += int(math.cos(radians) * self.velocity)
        #     self.pos[1] += int(math.sin(radians) * self.velocity * -1)
        #
        # elif self.angle > 90:
        #     radians = math.radians(180 - self.angle)
        #     self.pos[0] += int(math.cos(radians) * self.velocity * -1)
        #     self.pos[1] += int(math.cos(radians) * self.velocity * -1)
        #
        # else:
        #     self.pos[0] += 0
        #     self.pos[1] += self.velocity * -1
        self.pos += self.velocity

        # if not self.bounds.contains(self.rect()):
        #     self.kill()

    def bounce(self):
        # 0deg is -->, 90 is ^
        size = self.radius
        aoi = self.angle  # angle of incidence
        aor = 0

        # vertical boundaries
        if self.pos[0] + size >= self.bounds[0]:
            aor = 0

        # homarizontal boundaries
        #     aoi = 360 - (aoi + 180)

        if aoi >= 360:
             aoi -= 360
        elif aoi < 0:
             aoi += 360

        self.angle = aor

    def set_velocity(self, velocity):
        self.velocity = Vector2(1, 0).rotate(self.angle) * velocity
