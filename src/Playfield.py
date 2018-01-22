import math, pygame

class Playfield:

    def __init__(self, height, width, surface):
        assert isinstance(height, int)
        assert isinstance(width, int)
        assert isinstance(surface, pygame.SurfaceType)

        self.__SURF = surface

        # The base playfield is a 2D hex grid
        # which will begin life as a 2D matrix
        self.map = []
        for y in range(height):
            self.map.append([0 for x in range(width)])
            
    
    def draw(self):
        # TODO: blit the background image to the imported surface