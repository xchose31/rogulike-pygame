import pygame_gui
from Main_menu import *
from settings import *
from Player import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Игра")
        self.play = False
        self.clock = pygame.time.Clock()
        self.running = True
        self.main = Main_menu()  # Инициализация меню

        self.all_sprites = pygame.sprite.Group()

    def start_game(self):
        """
        Запускает игровой режим: убирает элементы меню.
        """
        self.player = Player((100, 100), self.all_sprites)
        self.play = True
        # Удаляем элементы меню
        self.main.button_new_game.kill()
        self.main.button_exit.kill()
        self.main.button_shop.kill()
        self.main.difficulty_dropdown.kill()
        self.main.mute_icon.kill()

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

            # Отрисовка
            self.screen.fill(BACKGROUND_COLOR)
            if not self.play:  # Меню
                self.main.manager.update(dt)
                self.main.manager.draw_ui(self.screen)
            else:  # Игровой режим
                # Здесь будет логика и отрисовка самой игры
                self.draw_game()

            self.all_sprites.update(dt)
            pygame.display.update()

        pygame.quit()

    def draw_game(self):
        """
        Логика и отрисовка игрового процесса.
        """
        # Временно: просто текст в центре
        self.all_sprites.draw(self.screen)


if __name__ == '__main__':
    game = Game()
    game.run()
    print(dir(pygame))
