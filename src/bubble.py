import pygame, math


class Bubble:

    def __init__(self, color, size, location) -> None:
        assert isinstance(color, str)
        assert isinstance(size, int)
        assert isinstance(location, tuple)

        self.color = color
        self.size = size
        self.location = location


