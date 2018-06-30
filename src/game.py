import pygame, os
from src.playfield import Playfield
from src.bubble import Bubble
from src.constants import *
from pygame.locals import *
from src.control import *


class Game:
    def __init__(self):
        # initialize pygame
        pygame.init()

        # set up the main window
        self.screen = pygame.display.set_mode(DISP_SIZE)
        pygame.display.set_caption('Py-Bubbles')
        self.screen.set_colorkey(pygame.Color('MAGENTA'))

        # set up the background
        # test background for now
        # later, src.Playfield will handle this part
        self.test_bkg = pygame.image.load(os.path.join(BGI_PATH, 'test_bkg.jpg'))

        # background = pygame.Surface(screen.get_size()).convert()
        # background.fill(pygame.Color('blue'))
        self.background = pygame.transform.scale(self.test_bkg, DISP_SIZE).convert_alpha()

        # load music
        # this may need to move or use a variable to integrate level music later
        pygame.mixer.music.load(os.path.join(BGM_PATH, 'test_music_drums.wav'))

        # start playing the music
        if BGM_ENABLED:
            pygame.mixer.music.set_volume(BGM_VOLUME)
            pygame.mixer.music.play(loops=-1, start=0.0)

        self.playfield = Playfield(os.path.join(os.curdir, 'maps', 'TEST_MAP1.JSON'), CELL_SIZE)
        self.playfield_pos = (
            DISP_SIZE[0] / 2 - (self.playfield.rect.width / 2),
            DISP_SIZE[1] / 2 - self.playfield.rect.height / 2
        )

        self.ball_angle = 20

        self.clock = pygame.time.Clock()

        # Instantiating controls object (temporary/test)
        self.control = Control()

    def run(self):
        # Run code
        while True:
            # paste the background
            self.screen.blit(self.background, (0, 0))

            # update the playfield and blit it
            self.playfield.update()
            self.screen.blit(self.playfield.image, self.playfield_pos)

            # write to screen
            if DEBUG:
                pos_text = pygame.font.Font(pygame.font.get_default_font(), 12).render(
                    "Cursor POS: {0}".format(pygame.mouse.get_pos()), True, pygame.Color("WHITE"))

                self.screen.blit(
                    pos_text,
                    (
                        20,
                        (DISP_SIZE[1] - pos_text.get_rect().size[1]) - 20
                    )
                )

            # handle controls for debugging
            self.control.process_movement()

            # this is the event handler, which we should move to src.Control
            # this is where any graphical updates are blitted to the display
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # stop music playback
                    # this will need to move later to the appropriate place based on design
                    pygame.mixer.music.stop()
                    return

                if event.type == self.control.shooty_doots:
                    if not self.playfield.active_bubble.sprite:
                        self.playfield.shooter.fire(10, self.playfield.active_bubble)

                if event.type == self.control.rotate_left:
                    self.playfield.shooter.rotate(1)
                elif event.type == self.control.rotate_right:
                    self.playfield.shooter.rotate(-1)

            # update the display to show changes
            # in production, we will use "dirty rect" updating to improve performance
            pygame.display.update()

            pygame.event.pump()

            # set framerate to no more than 60FPS
            self.clock.tick(60)