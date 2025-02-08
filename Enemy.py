import pygame.image
from Player import *
from settings import *
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player):
        super().__init__(groups)
        self.image = pygame.image.load(join('data', 'enemy', 'enemy.png'))
        new_width = int(self.image.get_width() * 0.1)  # Уменьшаем до 10% оригинального размера
        new_height = int(self.image.get_height() * 0.1)
        self.k = 1
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.rect = self.image.get_frect(center=pos)
        self.direction = pygame.Vector2()
        self.speed = 150 * self.k
        self.player = player

    def move(self, dt):
        direction = pygame.math.Vector2(self.player.rect.center) - pygame.math.Vector2(self.rect.center)
        if direction.length() > 0:
            direction = direction.normalize()
        self.rect.center += direction * self.speed * dt

    def take_damage(self, amount):
        """Наносит урон врагу."""
        self.health -= amount
        print(f"Здоровье врага: {self.health}")
        if self.health <= 0:
            print("Враг уничтожен!")
            self.kill()

    def check_collisions(self):
        """Проверяет столкновения с игроком."""
        if self.rect.colliderect(self.player.rect):
            self.kill()
            self.player.take_damage(10)  # Игрок получает урон

    def update(self, dt):
        self.move(dt)
        self.check_collisions()
        self.k += dt / 100
        self.speed = 150 * self.k
