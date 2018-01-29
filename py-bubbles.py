import pygame
import pygame.locals


def main():

    # initialize pygame
    pygame.init()

    # set up the main window
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Py-Bubbles')

    # set up the background
    # simple solid fill for now
    # later, src.Playfield will handle this part
    background = pygame.Surface(screen.get_size())
    background = background.convert(background)
    background.fill(pygame.Color('white'))

    clock = pygame.time.Clock()

    while True:
        # paste the background
        screen.blit(background, (0, 0))

        # this is the event handler, which we should move to src.Control
        # this is where any graphical updates are blitted to the display
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # update the display to show changes
        # in production, we will use "dirty rect" updating to improve performance
        pygame.display.update()

        # set framerate to no more than 60FPS
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
