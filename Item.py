import random

import pygame
from os import path
from Player import *
from settings import *
import math


class Item(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player):
        super().__init__(groups)
        self.frames = [pygame.image.load(path.join('data', 'items', f'coin{i}.png')) for i in range(1, 16)]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        new_width = int(self.image.get_width() * 2)  # Уменьшаем до 10% оригинального размера
        new_height = int(self.image.get_height() * 2)
        self.k = 1
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.rect = self.image.get_frect(center=pos)
        self.direction = pygame.Vector2()
        self.speed = 150 * self.k
        self.player = player

        # Параметры анимации
        self.animation_speed = 0.1  # Скорость анимации, можно настроить
        self.animation_time = 0

    def check_collisions(self):
        """Проверяет столкновения с игроком."""
        if self.rect.colliderect(self.player.rect):
            self.kill()
            self.player.take_item()
        for elem in self.player.enemies:
            if self.rect.colliderect(elem.rect):
                print(1)
                self.rect.center = (random.randint(0, screen_width), random.randint(0, screen_height))

    def update(self, dt):
        self.check_collisions()
        self.animate(dt)  # Вызов функции анимации

    def animate(self, dt):
        # Обновление времени анимации
        self.animation_time += dt
        if self.animation_time >= self.animation_speed:
            self.animation_time -= self.animation_speed
            self.current_frame = (self.current_frame + 1) % len(self.frames)

            # Изменение размера нового текущего кадра
            original_image = self.frames[self.current_frame]
            new_width = int(original_image.get_width() * 2)
            new_height = int(original_image.get_height() * 2)
            self.image = pygame.transform.scale(original_image, (new_width, new_height))
