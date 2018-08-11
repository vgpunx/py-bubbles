import pygame


class Control:
    def __init__(self):
        # Initialize joystick module
        pygame.joystick.init()

        # initialize events
        self.rotate_left = pygame.USEREVENT + 1
        self.rotate_right = pygame.USEREVENT + 2
        self.shooty_doots = pygame.USEREVENT + 3

        # Get the number of connected joysticks
        self.joystick_count = pygame.joystick.get_count()

        # For each joystick
        for i in range(self.joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            name = joystick.get_name()  # perhaps used later?

    def process_movement(self):
        keys = pygame.key.get_pressed()
        # Left and right
        if keys[pygame.K_a]:
            pygame.event.post(pygame.event.Event(self.rotate_left))
        elif keys[pygame.K_d]:
            pygame.event.post(pygame.event.Event(self.rotate_right))

        # Joystick left and right
        for i in range(self.joystick_count):
            joystick = pygame.joystick.Joystick(i)
            if joystick.get_axis(0) <= -0.5:
                pygame.event.post(pygame.event.Event(self.rotate_left))
            if joystick.get_axis(0) >= 0.5:
                pygame.event.post(pygame.event.Event(self.rotate_right))

        # Shooting code for test
        if keys[pygame.K_SPACE]:
            pygame.event.post(pygame.event.Event(self.shooty_doots))

