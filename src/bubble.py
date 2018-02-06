import pygame, math, collections


class Bubble(pygame.sprite.Sprite):

    def __init__(self, surface, pos, radius, fill_color, stroke_color, *groups):
        super().__init__(*groups)
        self.surface = surface

        self.pos = pos
        self.velocity = 0
        self.angle = 90

        # for drawing placeholder images
        # this will be replaced with actual image code later
        self.radius = radius
        self.fill = pygame.Color(fill_color)
        self.stroke = pygame.Color(stroke_color)

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
        self.draw()

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
        pygame.draw.circle(self.surface, self.fill, self.pos, self.radius)  # filled cir
        pygame.draw.circle(self.surface, self.stroke, self.pos, self.radius, 2)  # stroke

    def move(self):
        if self.angle < 90:
            radians = math.radians(self.angle)
            self.pos[0] += math.cos(radians) * self.velocity
            self.pos[1] += math.sin(radians) * self.velocity * -1

        elif self.angle > 90:
            radians = math.radians(180 - self.angle)
            self.pos[0] += math.cos(radians) * self.velocity * -1
            self.pos[1] += math.cos(radians) * self.velocity * -1

        else:
            self.pos[0] += 0
            self.pos[1] += self.velocity * -1
