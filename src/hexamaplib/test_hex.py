import sys, pygame, collections, hex_map, math
from hex_cell import HexCell
from pygame.locals import *


def main():

    # init pygame
    pygame.init()

    # configure screen.  we don't care if this one isn't resizable
    screensize = (800, 600)

    screen = pygame.display.set_mode(screensize, RESIZABLE)
    pygame.display.set_caption('Hexamaplib Test')

    # white background surface
    background = pygame.Surface(screen.get_size())
    background = background.convert(background)
    background.fill(pygame.Color('WHITE'))

    # set fps
    clock = pygame.time.Clock()

    # now the hex stuff
    hexsize = (30, 30)
    cell_or = 'pointy'

    hexmap = hex_map.HexMap(screensize, hexsize, hex_orientation=cell_or)
    print("The pixel position of the center of cell (0,0) is {0}.".format(hexmap.get_pixeladdressbycell((0, 0))))
    counter = 0
    # main loop
    while True:

        if counter < len(hexmap.board):
            keys = list(hexmap.board.keys())
            hexmap.board.get(keys[counter]).paint(background)
            counter += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("MouseButton {0} click.".format(event.button))
                if event.button == 1:  # left click
                    print("\tClick at pixel address {0}; translated to cell address {1}".format(event.pos, hexmap.get_celladdressbypixel(event.pos)))
                    cell = hexmap.board.get(hexmap.get_celladdressbypixel(event.pos))

                    if cell is not None:
                        cell.paint(background, color='BLUE', width=0)

            if event.type == pygame.MOUSEBUTTONUP:
                print("MouseButton {0} release.".format(event.button))
                if event.button == 1:
                    cell = hexmap.board.get(hexmap.get_celladdressbypixel(event.pos))

                    if cell is not None:
                        cell.paint(background, color='WHITE', width=0)
                        cell.paint(background, color='BLACK', width=2)

        # write to screen
        pos_text = pygame.font.Font(pygame.font.get_default_font(), 12).render(
            "Cursor POS: {0}".format(pygame.mouse.get_pos()), True, pygame.Color("BLUE"))

        screen.blit(background, (0, 0))
        screen.blit(
            pos_text,
            (
                20,
                (screensize[1] - pos_text.get_rect().size[1]) - 20
            )
        )

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    # if len(sys.argv) == 1:
    #     print('No args specified, running with reasonable defaults.')
    #     print('To set parameters, run with values for the following arguments ([] denotes optional):')
    #     print('test_hex.py [ (int) screensize_x (int) screensize_y ] [ (int) hexcount_x (int) hexcount_y ] [ (str) hex_orientation ]')

    main()
