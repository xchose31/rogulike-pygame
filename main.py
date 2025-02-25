import random
import datetime
import pygame.sprite
from Shop import ShopUI
from Main_menu import *
from settings import *
from Player import *
from Item import Item
from Enemy import *
import os


class Game:
    def __init__(self):
        pygame.init()
        self.player_class = Player
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
        self.font1 = pygame.font.Font(None, 74)
        self.font2 = pygame.font.Font(None, 60)
        self.difficulty_settings = {
            "Легко": 5,
            "Средне": 3,
            "Тяжело": 1
        }
        self.player = None
        self.check_money_skins()
        self.skin_num = 1
        self.shop_ui = None
        self.shop_visible = False  # Флаг для отслеживания видимости магазина
        self.skin_images = [
            pygame.image.load('./data/player/PlayerLeft1.png'),
            pygame.image.load('./data/player/PlayerLeft2.png'),
            pygame.image.load('./data/player/PlayerLeft3.png')
        ]
        self.skin_prices = [100, 150, 200]

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000  # Ограничение FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if not self.play:  # Обработка событий меню
                    self.main.manager.process_events(event)
                    if self.shop_ui:
                        self.shop_ui.handle_event(event)
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.main.button_new_game:
                            self.start_game()  # Переключение в игровой режим
                        elif event.ui_element == self.main.button_shop:
                            self.toggle_shop()
                        # Ожидание завершения процесса магазина
                        elif event.ui_element == self.main.button_exit:
                            self.running = False
                    if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                        if event.ui_element == self.main.difficulty_dropdown:
                            difficulty = self.main.difficulty_dropdown.selected_option
                            self.spawn_interval = self.difficulty_settings[difficulty[0]]
                        elif event.ui_element == self.main.set_skin_dropdown:
                            if self.main.set_skin_dropdown.selected_option[0] in self.skins:
                                self.skin_num = int(self.main.set_skin_dropdown.selected_option[0])
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
                if self.shop_ui:
                    self.shop_ui.draw()
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

    def toggle_shop(self):
        """
        Переключает видимость магазина.
        """
        self.shop_visible = not self.shop_visible  # Инвертируем флаг видимости
        if self.shop_visible:
            if not self.shop_ui:  # Создаем магазин, если он еще не создан
                self.shop_ui = ShopUI(self.screen, self.main.manager, self.skin_images)
        else:
            if self.shop_ui:
                # Убираем кнопки магазина
                for button in self.shop_ui.buttons:
                    button.kill()
                self.shop_ui = None

    def start_game(self):
        """
        Запускает игровой режим: убирает элементы меню.
        """
        self.player = Player((100, 100), self.all_sprites, self.enemies, self.skin_num)
        self.play = True
        self.play_sound('soundtrack.mp3', loop=True)
        # Удаляем элементы меню
        self.main.button_new_game.kill()
        self.main.button_exit.kill()
        self.main.button_shop.kill()
        self.main.difficulty_dropdown.kill()
        self.start_time = datetime.datetime.now()

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
        text = self.font1.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        self.screen.blit(text, text_rect)
        text2 = self.font2.render(f"Score: {self.score}", True, (255, 0, 0))
        text2_rect = text2.get_rect(center=(screen_width // 2, screen_height // 2 + 90))
        self.screen.blit(text2, text2_rect)
        text3 = self.font2.render(
            f"Заработано: {str(self.player.coins + self.player.kill_counter * 2)}, убито: {self.player.kill_counter}, подобрано монеток: {self.player.coins}",
            True, (255, 0, 0))
        text3_rect = text3.get_rect(center=(screen_width // 2, screen_height // 2 + 170))
        self.screen.blit(text3, text3_rect)

    def draw_score(self):
        self.score = self.player.counter * 10 + round(self.score_timer, 1) + self.player.kill_counter * 5
        text = self.font2.render(str(self.score), True, (255, 0, 0))
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
        con = sqlite3.connect('./data/database/base.sqlite')
        cur = con.cursor()
        end_time = datetime.datetime.now()
        duration = str(end_time - self.start_time)
        cur.execute("""INSERT INTO scores(score, time, kill, coins) VALUES(?, ?, ?, ?)""",
                    (self.score, duration, self.player.kill_counter, self.player.coins))
        con.commit()
        new_money = self.player.coins + self.player.kill_counter * 2
        with open('./data/saved_inf', 'r') as file:
            lines = file.readlines()

        # Меняем первую строку
        lines[0] = f'{int(lines[0].strip()) + new_money}\n'

        # Записываем обратно в файл
        with open('./data/saved_inf', 'w') as file:
            file.writelines(lines)

    def check_money_skins(self):
        with open('./data/saved_inf', 'r') as file:
            ls = file.readlines()
            ls = [line.rstrip() for line in ls]
            self.money = int(ls[0])
            self.skins = ls[1:]

    def play_sound(self, filename, loop=False):
        current_directory = os.path.dirname(__file__)
        sounds_directory = os.path.join(current_directory, 'Sounds')
        sound_file_path = os.path.join(sounds_directory, filename)

        # Убедимся, что есть достаточно каналов
        pygame.mixer.set_num_channels(1000)

        # Создание объекта Sound
        sound = pygame.mixer.Sound(sound_file_path)

        # Поиск свободного канала
        channel = pygame.mixer.find_channel()
        if channel:
            # Воспроизведение звука с учетом зацикливания
            if loop:
                channel.play(sound, loops=-1)  # -1 означает бесконечное повторение
            else:
                channel.play(sound)  # Одноразовое воспроизведение
            self.current_sound = sound  # Сохраняем текущий звук
            self.current_channel = channel  # Сохраняем текущий канал

    def stop(self):
        """Останавливает воспроизведение текущего звука."""
        if self.current_channel:
            self.current_channel.stop()
            self.current_sound = None
            self.current_channel = None

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
            Item(coord, (self.all_sprites, self.items), self.player)


if __name__ == '__main__':
    game = Game()
    game.run()
