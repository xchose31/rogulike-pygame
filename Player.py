import pygame.image

from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, enemies):
        super().__init__(groups)
        self.image = pygame.image.load(join('data', 'player', 'PlayerJump.png'))
        new_width = int(self.image.get_width() * 2)  # Увеличиваем до 200% оригинального размера
        new_height = int(self.image.get_height() * 2)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.rect = self.image.get_frect(center=pos)
        self.direction = pygame.Vector2()
        self.speed = 500
        self.max_health = 100
        self.health = 100  # Здоровье игрока
        self.enemies = enemies  # Группа врагов для проверки коллизий
        self.killed = False

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        """Двигает игрока, если нет коллизий."""
        # Создаем временную прямоугольную область для будущей позиции
        future_rect = self.rect.copy()
        future_rect.center += self.direction * self.speed * dt

        # Проверяем коллизии с врагами
        collided_enemies = pygame.sprite.spritecollide(self, self.enemies, False)
        for enemy in collided_enemies:
            if future_rect.colliderect(enemy.rect):  # Если будущая позиция пересекается
                return  # Отменяем движение

        # Если коллизий нет, обновляем позицию
        self.rect.center = future_rect.center

    def take_damage(self, amount):
        """Наносит урон игроку."""
        self.health -= amount
        print(f"Здоровье игрока: {self.health}")
        if self.health <= 0:
            print("Игрок уничтожен!")
            self.killed = True
            self.kill()

    def draw_health_bar(self, screen):
        """
        Рисует полоску здоровья над игроком.
        """
        bar_width = 50
        bar_height = 5
        border_color = BLUE
        fill_color = GREEN if self.health > 30 else RED

        health_bar_x = self.rect.centerx - bar_width // 2
        health_bar_y = self.rect.top - 10

        pygame.draw.rect(screen, border_color, (health_bar_x, health_bar_y, bar_width, bar_height))

        fill_width = int((self.health / self.max_health) * bar_width)
        pygame.draw.rect(screen, fill_color, (health_bar_x, health_bar_y, fill_width, bar_height))

    # def check_collisions(self):
    #     """Проверяет столкновения с врагами."""
    #     collided_enemies = pygame.sprite.spritecollide(self, self.enemies, False)
    #     if collided_enemies:
    #         for enemy in collided_enemies:
    #             self.take_damage(10)  # Игрок получает урон

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
