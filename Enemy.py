import pygame.image
from Player import *
from settings import *
import math


class Enemy(pygame.sprite.Sprite):
    def  __init__(self, pos, groups, player):
        super().__init__(groups)
        self.image = pygame.image.load(join('data', 'enemy', 'enemy.png'))
        new_width = int(self.image.get_width() * 0.1)  # Уменьшаем до 50% оригинальной ширины
        new_height = int(self.image.get_height() * 0.1)  # Уменьшаем до 50% оригинальной высоты
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.rect = self.image.get_frect(center=pos)
        self.direction = pygame.Vector2()
        self.speed = 150
        self.player = player

    def move(self, dt):
        direction = pygame.math.Vector2(self.player.rect.center) - pygame.math.Vector2(self.rect.center)

        if direction.length() > 0:  # Проверяем, чтобы избежать деления на ноль
            direction = direction.normalize()

        self.rect.x += direction.x * self.speed * dt
        self.rect.y += direction.y * self.speed * dt

    def update(self, dt):
        self.move(dt)