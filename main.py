import random

import pygame.sprite
import pygame_gui
from Main_menu import *
from settings import *
from Player import *
from Item import *
from Enemy import *
from pytmx.util_pygame import load_pygame
import os


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Игра")
        self.clock = pygame.time.Clock()
        self.play = False
        self.running = True
        self.saved = False
        self.main = Main_menu()
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.weapons = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.spawn_timer = 0
        self.score_timer = 0
        self.shoot_timer = 0
        self.shoot_interval = 0.5
        self.spawn_interval = 3
        self.score = 0
        self.font = pygame.font.Font(None, 74)
        self.difficulty_settings = {
            "Легко": 5,
            "Средне": 3,
            "Тяжело": 1
        }
        self.player = None

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000  # Ограничение FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if not self.play:  # Обработка событий меню
                    self.main.manager.process_events(event)
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.main.button_new_game:
                            print("Начата новая игра!")
                            self.start_game()  # Переключение в игровой режим
                        elif event.ui_element == self.main.button_shop:
                            print("Открыт магазин!")
                        elif event.ui_element == self.main.button_exit:
                            print("Выход из игры!")
                            self.running = False
                        elif event.ui_element == self.main.mute_icon:
                            if self.main.mute_icon.text == "звук+":
                                self.main.mute_icon.set_text("звук-")
                                print("Звук выключен")
                            else:
                                self.main.mute_icon.set_text("звук+")
                                print("Звук включен")
                    if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                        if event.ui_element == self.main.difficulty_dropdown:
                            print(f"Выбрана сложность: {self.main.difficulty_dropdown.selected_option}")
                            difficulty = self.main.difficulty_dropdown.selected_option
                            print(difficulty[0])
                            self.spawn_interval = self.difficulty_settings[difficulty[0]]
                if event.type == pygame.MOUSEBUTTONDOWN and not self.player is None and self.shoot_timer >= self.shoot_interval:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        direction = pygame.math.Vector2(mouse_pos) - pygame.math.Vector2(self.player.rect.center)
                        if direction.length() > 0:
                            direction = direction.normalize()
                        Bullet(self.enemies, self.player, [self.all_sprites, self.bullets], self.player.rect.center,
                               direction)
                        self.shoot_timer = 0

            # Отрисовка
            self.screen.fill(BACKGROUND_COLOR)
            if not self.play:  # Меню
                self.main.manager.update(dt)
                self.main.manager.draw_ui(self.screen)
            else:  # Игровой режим
                # Обновление таймеров и создание врагов
                if not self.player.killed:
                    self.spawn_timer += dt
                    self.score_timer += dt
                    self.shoot_timer += dt
                    if self.spawn_timer >= self.spawn_interval:
                        self.spawn_enemy()
                        self.spawn_item()
                        self.spawn_timer = 0
                # Логика и отрисовка самой игры
                self.draw_game()

            self.all_sprites.update(dt)
            pygame.display.update()
        pygame.quit()

    def start_game(self):
        """
        Запускает игровой режим: убирает элементы меню.
        """
        self.player = Player((100, 100), self.all_sprites, self.enemies)
        self.play = True
        # Удаляем элементы меню
        self.main.button_new_game.kill()
        self.main.button_exit.kill()
        self.main.button_shop.kill()
        self.main.difficulty_dropdown.kill()
        self.main.mute_icon.kill()

    def draw_game(self):
        """
        Логика и отрисовка игрового процесса.
        """
        if not self.player.killed:
            self.all_sprites.draw(self.screen)
            self.player.draw_health_bar(self.screen)
            self.draw_score()
            self.reload_bar()
        else:
            self.all_sprites.empty()
            self.draw_game_over()
            if not self.saved:
                self.save_score()
                self.saved = True

    def draw_game_over(self):
        """
        Отображает текст "Game Over" на экране.
        """
        text = self.font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        self.screen.blit(text, text_rect)

    def draw_score(self):
        self.score = self.player.counter * 10 + round(self.score_timer, 1) + self.player.kill_counter * 5
        text = self.font.render(str(self.score), True, (255, 0, 0))
        self.screen.blit(text, (10, 10))

    def reload_bar(self):
        bar_width = 50
        bar_height = 5
        border_color = BLUE

        reload_bar_x = self.player.rect.centerx - bar_width // 2
        reload_bar_y = self.player.rect.top - 20
        fill_color = LITE_BLUE

        pygame.draw.rect(self.screen, border_color, (reload_bar_x, reload_bar_y, bar_width, bar_height))

        fill_width = int((self.shoot_timer / self.shoot_interval) * bar_width)
        if fill_width >= bar_width:
            fill_width = bar_width
        pygame.draw.rect(self.screen, fill_color, (reload_bar_x, reload_bar_y, fill_width, bar_height))

    def save_score(self):
        with open("scores.txt", "a") as file:
            file.write(f"{self.score}\n")
        print(f"Очки сохранены: {self.score}")

    def play(self, filename):
        current_directory = os.path.dirname(__file__)
        sounds_directory = os.path.join(current_directory, 'Sounds')
        sound_file_path = os.path.join(sounds_directory, filename)
        pygame.mixer.set_num_channels(1000)
        sound = pygame.mixer.Sound(sound_file_path)  # Создание объекта Sound
        channel = pygame.mixer.find_channel()  # Поиск свободного канала
        if channel:
            channel.play(sound)

    def spawn_enemy(self):
        """
        Создает нового врага на краю экрана.
        """
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            x, y = -50, random.randint(0, screen_height)
        elif side == "right":
            x, y = screen_width + 50, random.randint(0, screen_height)
        elif side == "top":
            x, y = random.randint(0, screen_width), -50
        elif side == "bottom":
            x, y = random.randint(0, screen_width), screen_height + 50
        Enemy((x, y), [self.all_sprites, self.enemies], self.player)

    def spawn_item(self):
        """
        Создает нового врага на краю экрана.
        """
        if len(self.items) <= 4:
            coord = (random.randint(0, screen_width), random.randint(0, screen_height))
            Item(coord, [self.all_sprites, self.items], self.player)


if __name__ == '__main__':
    game = Game()
    game.run()
