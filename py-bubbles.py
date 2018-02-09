import pygame, os
from src.playfield import Playfield
from src.bubble import Bubble
from pygame.locals import *


def main():
    ### CONSTANTS ###
    ## SIZE
    DISP_SIZE = (800, 600)
    PFLD_SIZE = (DISP_SIZE[0] * 0.65, DISP_SIZE[1] * 0.98)  # 65% scr width, 85% scr height
    CELL_SIZE = (PFLD_SIZE[0] / 23, PFLD_SIZE[0] / 23)  # Fit 15 bubbles across

    ## BUBBLE MAP


    ## COLORS

    ## ALIGNMENT


    # initialize pygame
    pygame.init()

    # set up the main window

    screen = pygame.display.set_mode(DISP_SIZE)
    pygame.display.set_caption('Py-Bubbles')
    screen.set_colorkey(pygame.Color('MAGENTA'))

    # set up the background
    # simple solid fill for now
    # later, src.Playfield will handle this part
    bg_orig = pygame.Surface(screen.get_size())
    bg_orig = bg_orig.convert()
    bg_orig.fill(pygame.Color('blue'))

    playfield = Playfield(PFLD_SIZE, CELL_SIZE)
    playfield.load_map(os.path.join(os.curdir, 'maps', 'TEST_MAP0'))
    sur = playfield.get_surface()
    # sur.set_colorkey(pygame.Color('MAGENTA'))
    sur.convert()

    b_start = list(playfield.hexmap.board.get('7, 9').get_pixelpos())
    b_start[0] = int(b_start[0] + (sur.get_size()[0] / 2) - b_start[0])
    b_orig = b_start[1]
    test_bub = Bubble(
        b_start,
        playfield.get_surface().get_size(),
        int(CELL_SIZE[0] - 2),
        'RED',
        'BLACK'
    )

    test_bub.velocity = 10
    test_bub.angle = 45

    clock = pygame.time.Clock()

    while True:
        # paste the background
        playfield.update()
        sur.blit(test_bub.image, test_bub.pos)

        screen.blit(bg_orig, (0, 0))
        screen.blit(
            sur,
            ((screen.get_size()[0] / 2) - PFLD_SIZE[0] / 2, (screen.get_size()[1] / 2) - PFLD_SIZE[1] / 2)
        )

        if test_bub.pos[1] <= 0:
            test_bub.pos[1] = b_orig
        else:
            test_bub.update()
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
