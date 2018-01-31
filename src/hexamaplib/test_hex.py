import sys, pygame, collections, hex_map
from pygame.locals import *


def main():

    # init pygame
    pygame.init()

    # configure screen.  we don't care if this one isn't resizable
    screensize = (500, 600)

    screen = pygame.display.set_mode(screensize, RESIZABLE)
    pygame.display.set_caption('Hexamaplib Test')

    # white background surface
    background = pygame.Surface(screen.get_size())
    background = background.convert(background)
    background.fill(pygame.Color('WHITE'))

    # set fps
    clock = pygame.time.Clock()

    # now the hex stuff
    hexsize = (25, 25)
    cell_or = 'flat'

    hexmap = hex_map.HexMap(screensize, hexsize, cell_or)

    for cell in hexmap.board.values():
        cell.paint(background)

    # main loop
    while True:
        clock.tick(15)
        screen.blit(background, (0, 0))

        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    # if len(sys.argv) == 1:
    #     print('No args specified, running with reasonable defaults.')
    #     print('To set parameters, run with values for the following arguments ([] denotes optional):')
    #     print('test_hex.py [ (int) screensize_x (int) screensize_y ] [ (int) hexcount_x (int) hexcount_y ] [ (str) hex_orientation ]')

    main()
