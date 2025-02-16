import pygame.image
from Player import *
from settings import *
import math



class Item(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player):
        super().__init__(groups)
        self.image = pygame.image.load(join('data', 'items', 'coin.png'))
        new_width = int(self.image.get_width() * 0.025)  # Уменьшаем до 10% оригинального размера
        new_height = int(self.image.get_height() * 0.025)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.rect = self.image.get_frect(center=pos)
        self.player = player

    def check_collisions(self):
        """Проверяет столкновения с игроком."""
        if self.rect.colliderect(self.player.rect):
            self.kill()
            self.player.counter += 1
            print(self.player.counter)

    def update(self, dt):
        self.check_collisions()