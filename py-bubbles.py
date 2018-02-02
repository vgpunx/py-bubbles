import pygame
from src.playfield import Playfield
from pygame.locals import *


def main():

    # initialize pygame
    pygame.init()

    # set up the main window
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption('Py-Bubbles')

    # set up the background
    # simple solid fill for now
    # later, src.Playfield will handle this part
    bg_orig = pygame.Surface(screen.get_size())
    bg_orig = bg_orig.convert(bg_orig)
    bg_orig.fill(pygame.Color('blue'))

    playfield_size = (400, 600)
    cell_size = (30, 30)
    playfield = Playfield(playfield_size, cell_size)
    playfield.test()

    clock = pygame.time.Clock()

    while True:
        # paste the background
        screen.blit(bg_orig, (0, 0))
        screen.blit(playfield.get_surface(), ((screen.get_size()[0] / 2) - playfield_size[0] / 2, 0))

        # this is the event handler, which we should move to src.Control
        # this is where any graphical updates are blitted to the display
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # update the display to show changes
        # in production, we will use "dirty rect" updating to improve performance
        pygame.display.update()

        pygame.event.pump()

        # set framerate to no more than 60FPS
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
