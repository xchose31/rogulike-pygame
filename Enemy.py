import pygame.image
from Player import *
from settings import *
import math


class Enemy(pygame.sprite.Sprite):
    def  __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('data', 'enemy', 'enemy.png'))
        new_width = int(self.image.get_width() * 0.1)  # Уменьшаем до 50% оригинальной ширины
        new_height = int(self.image.get_height() * 0.1)  # Уменьшаем до 50% оригинальной высоты
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.rect = self.image.get_frect(center=pos)
        self.direction = pygame.Vector2()
        self.speed = 100

    def move(self, dt):
        coord = Player.get_coord()
        player_x = coord[0]
        player_y = coord[1]
        s_coord = self.rect.center


        direction_x = player_x - self.rect.centerx
        direction_y = player_y - self.rect.centery
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

        if distance != 0:
            direction_x /= distance
            direction_y /= distance

            # обновляем позицию врага
            self.rect.x += direction_x * self.speed
            self.rect.y += direction_y * self.speed

            self.rect.center += self.direction * self.speed * dt