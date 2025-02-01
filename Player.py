import pygame.image

from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('data', 'player', 'PlayerJump.png'))
        self.rect = self.image.get_frect(center=pos)
        self.direction = pygame.Vector2()
        self.speed = 500

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.rect.center += self.direction * self.speed * dt

    def get_coord(self):
        return self.rect.center

    def update(self, dt):
        self.input()
        self.move(dt)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
        print(self.get_coord())
