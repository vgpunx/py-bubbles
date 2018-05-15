import pygame
from pygame.math import Vector2


class Bubble(pygame.sprite.Sprite):

    def __init__(self, address, pos, radius, fill_color, stroke_color, angle=90, velocity=0, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = pygame.Surface((radius * 2, radius * 2))
        self.image.set_colorkey(pygame.Color('MAGENTA'))
        self.rect = self.image.get_rect(center=pos)

        # movement & location
        self.grid_address = address
        self.pos = Vector2(pos)
        self.angle = angle
        self.velocity = Vector2(1, 0).rotate(-self.angle) * velocity
        # self.bounds = bounds

        # for drawing placeholder images
        # this will be replaced with actual image code later
        self.radius = radius
        self.fill = pygame.Color(fill_color)
        self.stroke = pygame.Color(stroke_color)
        self.draw()

    def set_velocity(self, velocity):
        self.velocity = Vector2(1, 0).rotate(-self.angle) * velocity

    def set_angle(self, degrees):
        self.angle = degrees
        delta = self.velocity.angle_to(Vector2(1, 0).rotate(-self.angle))
        self.velocity = self.velocity.rotate(delta)

    def set_position(self, coords: list):
        self.pos = Vector2(coords)
        self.rect.center = self.pos

    def update(self, *args):
        super().update(*args)
        self.move(self.velocity)
        # self.bounce()

    def draw(self):
        # placeholder code
        self.image.fill(pygame.Color('MAGENTA'))
        pygame.draw.circle(self.image, self.fill, self.image.get_rect().center, self.radius)  # filled cir
        pygame.draw.circle(self.image, self.stroke, self.image.get_rect().center, self.radius, 2)  # stroke
        self.image.convert()

    def move(self, direction: pygame.math.Vector2):

        # TODO: implement alive test
        self.pos += direction
        self.rect.center = self.pos

    def bounce(self, collision_vector):
        """
        Updates internal velocity vector with one that is reflected off of the given collision vector.
        :param collision_vector: pygame.math.Vector2
        :return: None
        """

        self.velocity = self.velocity.reflect(collision_vector.rotate(90).normalize())
        # self.move(self.velocity)


    # overload placeholders
    def add(self, *groups):
        super().add(*groups)

    def remove(self, *groups):
        super().remove(*groups)

    def add_internal(self, group):
        super().add_internal(group)

    def remove_internal(self, group):
        super().remove_internal(group)

    def kill(self):
        super().kill()

    def groups(self):
        return super().groups()

    def alive(self):
        return super().alive()

    def __repr__(self):
        return super().__repr__()

