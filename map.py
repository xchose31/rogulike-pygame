import pygame
from settings import *

MAP_DATA = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
]


class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, groups, file):
        super().__init__(groups)
        self.image = pygame.image.load(join('data', 'maps', file))
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image.get_width() * 0.5), int(self.image.get_height() * 0.5)))
        self.rect = self.image.get_frect(center=pos)


class TileMap:
    def __init__(self, map_data, tile_size, sprites):
        self.map_data = map_data
        self.all_sprites = sprites
        self.tile_size = tile_size
        self.tiles = {
            1: "block.png",
        }
        self.width = len(map_data[0]) * tile_size
        print(self.width)
        self.height = len(map_data) * tile_size
        print(self.height)
        self.collide_sprites = pygame.sprite.Group()
        self.collidable_tiles = 1
        for row_index, row in enumerate(self.map_data):
            for col_index, tile_type in enumerate(row):
                if tile_type == self.collidable_tiles:
                    CollisionSprite((col_index * self.tile_size,
                                     row_index * self.tile_size,), [self.all_sprites, self.collide_sprites],
                                    self.tiles[tile_type])
