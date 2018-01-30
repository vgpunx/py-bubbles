import sys, pygame, collections, hex_map
from pygame.locals import *


def main():

    # if len(sys.argv >= 3):
    #     # Handle screen size setting
    #     if sys.argv[1] is not None and type(sys.argv[1]) is int:
    #         if sys.argv[2] is None or type(sys.argv[2]) is not int:
    #             raise Exception('You must specify two integer arguments to set the screen size.')
    #         screensize = (sys.argv[1], sys.argv[2])
    #     else:
    screensize = (400, 400)
    #
    # if len(sys.argv >= 5):
    #     # handle cell count setting
    #     if sys.argv[3] is not None and type(sys.argv[3]) is int:
    #         if sys.argv[4] is None or type(sys.argv[4]) is not int:
    #             raise Exception('You must specify two integer arguments to set the hex row and column counts.')
    #         hexcount = (sys.argv[3], sys.argv[4])
    #     else:
    hexcount = (10, 10)
    #
    # if len(sys.argv >= 6):
    #     # handle orientation setting
    #     if sys.argv[5] is not None and type(sys.argv[5]) is str and sys.argv[5] in ('flat', 'pointy'):
    #         cell_or = sys.argv[5]
    #     elif sys.argv[5] is None:
    cell_or = 'flat'
    #     else:
    #         raise Exception('You must specify either "flat" or "pointy" to set cell orientation.')

    # init pygame
    pygame.init()

    # configure screen.  we don't care if this one isn't resizable
    screen = pygame.display.set_mode(screensize)
    pygame.display.set_caption('Hexamaplib Test')

    # white background surface
    background = pygame.Surface(screen.get_size())
    background = background.convert(background)
    background.fill(pygame.Color('WHITE'))

    # set fps
    clock = pygame.time.Clock()

    # now the hex stuff
    hexmap = hex_map.HexMap(screensize, hexcount, cell_or)
    cellsurf = pygame.Surface(screen.get_size())

    # main loop
    while True:
        screen.blit(background, (0, 0))

        for cell in hexmap.board.values():
            cell.paint(cellsurf)

        screen.blit(cellsurf, cell.get_pixelpos())
        pygame.display.update()

        pygame.event.pump()

        for event in pygame.event.get():
            if event == pygame.QUIT:
                return

        clock.tick(15)

    pygame.quit()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('No args specified, running with reasonable defaults.')
        print('To set parameters, run with values for the following arguments ([] denotes optional):')
        print('test-hex.py [ (int) screensize_x (int) screensize_y ] [ (int) hexcount_x (int) hexcount_y ] \
              [ (str) hex_orientation ]')

    main()
