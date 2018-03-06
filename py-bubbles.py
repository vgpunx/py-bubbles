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

    ## PATHS
    BGM_PATH = os.path.join(os.curdir, 'resource', 'audio', 'bgm')
    SFX_PATH = os.path.join(os.curdir, 'resource', 'audio', 'sfx')
    BGI_PATH = os.path.join(os.curdir, 'resource', 'image', 'bkg')
    SPR_PATH = os.path.join(os.curdir, 'resource', 'image', 'sprites')

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
    test_bkg = pygame.image.load(os.path.join(BGI_PATH, 'test_bkg.jpg'))

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    # background.fill(pygame.Color('blue'))
    background = pygame.transform.scale(test_bkg, DISP_SIZE)

    # load music
    # this may need to move or use a variable to integrate level music later
    pygame.mixer.music.load(os.path.join(BGM_PATH, 'test_music_drums.wav'))

    # start playing the music
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1, start=0.0)


    playfield = Playfield(PFLD_SIZE, CELL_SIZE)
    playfield.load_map(os.path.join(os.curdir, 'maps', 'TEST_MAP0.JSON'))

    ball_angle = 20

    clock = pygame.time.Clock()

    while True:
        # paste the background
        screen.blit(background, (0, 0))

        # update the playfield and blit it
        playfield.update()
        screen.blit(
            playfield.get_surface(),
            # there has to be a more elegant way to align surfaces than this
            ((screen.get_size()[0] / 2) - PFLD_SIZE[0] / 2, (screen.get_size()[1] / 2) - PFLD_SIZE[1] / 2)
        )

        # this is the event handler, which we should move to src.Control
        # this is where any graphical updates are blitted to the display
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fire_test(playfield, ball_angle)

                    if ball_angle < 160:
                        ball_angle += 5
                    else:
                        ball_angle = 20

        # update the display to show changes
        # in production, we will use "dirty rect" updating to improve performance
        pygame.display.update()

        pygame.event.pump()

        # set framerate to no more than 60FPS
        clock.tick(60)

    # stop music playback
    # this will need to move later to the appropriate place based on design
    pygame.mixer.music.stop()

    pygame.quit()


def fire_test(playfield: Playfield, angle):
    b_start = list(playfield.hexmap.board.get('7, 9').get_pixelpos())
    b_start[0] = int(b_start[0] + (playfield.get_surface().get_size()[0] / 2) - b_start[0])

    playfield.active_bubbles.add(
        Bubble(
            pos=b_start,
            bounds=playfield.get_surface().get_rect(),
            radius=int(playfield.hexmap.cellsize[0] - 2),
            fill_color='RED',
            stroke_color='BLACK',
            angle=angle,
            velocity=10
        )
    )

if __name__ == "__main__":
    main()
