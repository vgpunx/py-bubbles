from pygame.sprite import Group, Sprite
from bubble import Bubble


class BubbleMap(Group):

    def __init__(self, *sprites):
        """

        :type *sprites: bubble.Bubble
        """
        super().__init__(*sprites)

        # internal structure that keeps track of Bubbles by grid address
        self.sprite_dict_by_address = dict()

    def add(self, *sprites):
        super().add(*sprites)

        for obj in sprites:
            if obj not in self.sprite_dict_by_address:
                self.sprite_dict_by_address[obj.grid_address] = obj

    def remove(self, *sprites):
        super().remove(*sprites)

        for obj in sprites:
            if obj in self.sprite_dict_by_address:
                del self.sprite_dict_by_address[obj.grid_address]

    def empty(self):
        super().empty()
        self.sprite_dict_by_address.clear()

    def get(self, address):
        try:
            return self.sprite_dict_by_address[address]

        except KeyError:
            return None

    def get_present_types(self):
        """
        Returns a list of unique Bubble types currently present in map.

        :return: List
        """
        result = list()

        for item in self.sprite_dict_by_address.values():
            if item.type_property not in result:
                result.append(item.type_property)

        return result
