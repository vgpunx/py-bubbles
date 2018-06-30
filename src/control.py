import pygame


class Control:
    def __init__(self):
        # initialize events
        self.rotate_left = pygame.USEREVENT + 1
        self.rotate_right = pygame.USEREVENT + 2
        self.shooty_doots = pygame.USEREVENT + 3

    def process_movement(self):
        keys = pygame.key.get_pressed()
        # Left and right
        if keys[pygame.K_a]:
            pygame.event.post(pygame.event.Event(self.rotate_left))
        elif keys[pygame.K_d]:
            pygame.event.post(pygame.event.Event(self.rotate_right))

        # Shooting code for test
        # if keys[pygame.K_SPACE]:
        #     pygame.event.post(pygame.event.Event(self.shooty_doots))

