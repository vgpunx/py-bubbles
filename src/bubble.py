import math
import pygame


class Bubble(pygame.sprite.Sprite):

    def __init__(self, pos, bounds, radius, fill_color, stroke_color, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((radius * 2, radius * 2))
        self.image.set_colorkey(pygame.Color('MAGENTA'))

        self.pos = [pos[0] - radius, pos[1] - radius]
        self.velocity = 0
        self.angle = 90
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
        self.move()
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
        if self.angle < 90:
            radians = math.radians(self.angle)
            self.pos[0] += int(math.cos(radians) * self.velocity)
            self.pos[1] += int(math.sin(radians) * self.velocity * -1)

        elif self.angle > 90:
            radians = math.radians(180 - self.angle)
            self.pos[0] += int(math.cos(radians) * self.velocity * -1)
            self.pos[1] += int(math.cos(radians) * self.velocity * -1)

        else:
            self.pos[0] += 0
            self.pos[1] += self.velocity * -1

    def bounce(self):
        size = self.radius * 2
        ang = math.radians(self.angle)

        if self.pos[0] + size >= self.bounds[0] or self.pos[0] - size <= 0:
            ang = -ang

        elif self.pos[1] + size >= self.bounds[1] or self.pos[1] - size <= size:
            ang = math.pi - ang

        self.angle = int(math.degrees(ang))
