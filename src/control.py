import pygame


class Control:
    def __init__(self):
        # initialize events
        self.rotate_left = pygame.USEREVENT + 1
        self.rotate_right = pygame.USEREVENT + 2
        self.shooty_doots = pygame.USEREVENT + 3

    def process_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            pygame.event.post(pygame.event.Event(self.rotate_left))

        elif keys[pygame.K_d]:
            pygame.event.post(pygame.event.Event(self.rotate_right))
