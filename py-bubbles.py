import pygame
from src.playfield import Playfield
from pygame.locals import *


def main():
    ### CONSTANTS ###
    # SIZE
    DISP_SIZE = (800, 600)
    PFLD_SIZE = (DISP_SIZE[0] * 0.65, DISP_SIZE[1] * 0.95)  # 65% scr width, 95% scr height
    CELL_SIZE = (PFLD_SIZE[0] / 23, PFLD_SIZE[0] / 23)  # Fit 15 bubbles across

    # COLORS

    # ALIGNMENT


    # initialize pygame
    pygame.init()

    # set up the main window

    screen = pygame.display.set_mode(DISP_SIZE)
    pygame.display.set_caption('Py-Bubbles')

    # set up the background
    # simple solid fill for now
    # later, src.Playfield will handle this part
    bg_orig = pygame.Surface(screen.get_size())
    bg_orig = bg_orig.convert(bg_orig)
    bg_orig.fill(pygame.Color('blue'))

    playfield = Playfield(PFLD_SIZE, CELL_SIZE)
    sur = playfield.test(playfield.get_surface())

    clock = pygame.time.Clock()

    while True:
        # paste the background
        screen.blit(bg_orig, (0, 0))
        screen.blit(
            sur,
            ((screen.get_size()[0] / 2) - PFLD_SIZE[0] / 2, (screen.get_size()[1] / 2) - PFLD_SIZE[1] / 2)
        )

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
