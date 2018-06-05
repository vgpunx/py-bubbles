import pygame, os
from src.playfield import Playfield
from src.bubble import Bubble
from src.constants import *
from pygame.locals import *


def main():

    # initialize pygame
    pygame.init()

    # set up the main window
    screen = pygame.display.set_mode(DISP_SIZE)
    pygame.display.set_caption('Py-Bubbles')
    screen.set_colorkey(pygame.Color('MAGENTA'))

    # set up the background
    # test background for now
    # later, src.Playfield will handle this part
    test_bkg = pygame.image.load(os.path.join(BGI_PATH, 'test_bkg.jpg'))

    #background = pygame.Surface(screen.get_size()).convert()
    # background.fill(pygame.Color('blue'))
    background = pygame.transform.scale(test_bkg, DISP_SIZE).convert()

    # load music
    # this may need to move or use a variable to integrate level music later
    pygame.mixer.music.load(os.path.join(BGM_PATH, 'test_music_drums.wav'))

    # start playing the music
    if BGM_ENABLED:
        pygame.mixer.music.set_volume(BGM_VOLUME)
        pygame.mixer.music.play(loops=-1, start=0.0)

    playfield = Playfield(os.path.join(os.curdir, 'maps', 'TEST_MAP1.JSON'), CELL_SIZE)
    playfield_pos = (
        DISP_SIZE[0] / 2 - (playfield.rect.width / 2),
        DISP_SIZE[1] / 2 - playfield.rect.height / 2
    )
    # playfield.rect.center = screen.get_rect().center

    ball_angle = 20

    clock = pygame.time.Clock()

    while True:
        # paste the background
        screen.blit(background, (0, 0))

        # update the playfield and blit it
        playfield.update()
        screen.blit(playfield.image, playfield_pos)

        # write to screen
        if DEBUG:
            pos_text = pygame.font.Font(pygame.font.get_default_font(), 12).render(
                "Cursor POS: {0}".format(pygame.mouse.get_pos()), True, pygame.Color("WHITE"))

            screen.blit(
                pos_text,
                (
                    20,
                    (DISP_SIZE[1] - pos_text.get_rect().size[1]) - 20
                )
            )

        # handle controls for debugging
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            fire_test(playfield, playfield.shooter.angle)

        elif keys[K_a]:
            playfield.shooter.rotate(1)

        elif keys[K_d]:
            playfield.shooter.rotate(-1)

        # this is the event handler, which we should move to src.Control
        # this is where any graphical updates are blitted to the display
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         fire_test(playfield, playfield.shooter.angle)
            #
            #     elif event.key == pygame.K_a:
            #         playfield.shooter.rotate(2)
            #
            #     elif event.key == pygame.K_d:
            #         playfield.shooter.rotate(-2)


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
    b_origin_pos = playfield.shooter.rect.center
    b_origin_cell = playfield.hexmap.get_celladdressbypixel(b_origin_pos)
    # b_origin_pos[0] = int(b_origin_pos[0] + (playfield.get_surface().get_size()[0] / 2) - b_origin_pos[0])

    if len(playfield.active_bubble) == 0:
        fire = Bubble(
            b_origin_cell,                                       # address
            b_origin_pos,                                            # pixelpos
            int(playfield.hexmap.cellsize[0] - 2),              # radius
            'RED',                                              # fill_color
            'BLACK',                                            # stroke_color
            angle,                                              # angle
            10,                                                 # velocity
            (playfield.all_sprites, playfield.active_bubble)    # *groups
        )
        # playfield.active_bubble.add(fire)
        # playfield.all_sprites.add(fire)

if __name__ == "__main__":
    main()
