import random

import pygame_gui
from Main_menu import *
from settings import *
from Player import *
from Enemy import *
from pytmx.util_pygame import load_pygame
import os


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Игра")
        self.play = False
        self.clock = pygame.time.Clock()
        self.running = True
        self.main = Main_menu()
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.weapons =  pygame.sprite.Group()
        self.spawn_timer = 0
        self.spawn_interval = 3
        self.font = pygame.font.Font(None, 74)
        self.difficulty_settings = {
            "Легко": 5,
            "Средне": 3,
            "Тяжело": 1
        }

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

            # Отрисовка
            self.screen.fill(BACKGROUND_COLOR)
            if not self.play:  # Меню
                self.main.manager.update(dt)
                self.main.manager.draw_ui(self.screen)
            else:  # Игровой режим
                # Обновление таймера и создание врагов
                if not self.player.killed:
                    self.spawn_timer += dt
                    if self.spawn_timer >= self.spawn_interval:
                        self.spawn_enemy()
                        self.spawn_timer = 0

                # Логика и отрисовка самой игры
                self.draw_game()

            self.all_sprites.update(dt)
            pygame.display.update()
        pygame.quit()

    def draw_game(self):
        """
        Логика и отрисовка игрового процесса.
        """
        if not self.player.killed:
            self.all_sprites.draw(self.screen)
            self.player.draw_health_bar(self.screen)
        else:
            self.all_sprites.empty()
            self.draw_game_over()

    def draw_game_over(self):
        """
        Отображает текст "Game Over" на экране.
        """
        text = self.font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        self.screen.blit(text, text_rect)


    def play(self, filename):
        current_directory = os.path.dirname(__file__)
        sounds_directory = os.path.join(current_directory, 'Sounds')
        sound_file_path = os.path.join(sounds_directory, filename)
        pygame.mixer.set_num_channels(1000)
        sound = pygame.mixer.Sound(sound_file_path)  # Создание объекта Sound
        channel = pygame.mixer.find_channel()  # Поиск свободного канала
        if channel:
            channel.play(sound)


if __name__ == '__main__':
    game = Game()
    game.run()
