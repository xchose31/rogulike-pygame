import pygame_gui
from settings import *


class Main_menu:
    def __init__(self):
        self.check_skins()
        self.money = 0
        self.manager = pygame_gui.UIManager((screen_width, screen_height), theme_path=None)
        self.button_new_game = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((screen_width // 2 - 100, 200), (200, 50)),
            text="Новая игра",
            manager=self.manager,
        )

        self.button_shop = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((screen_width // 2 - 100, 270), (200, 50)),
            text="Магазин",
            manager=self.manager,
        )

        self.button_exit = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((screen_width // 2 - 100, 340), (200, 50)),
            text="Выход",
            manager=self.manager,
        )

        self.mute_icon = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, screen_height - 120), (50, 50)),
            text="звук+",  # Иконка звука
            manager=self.manager,
        )

        self.difficulty_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=["Легко", "Средне", "Тяжело"],
            starting_option="Средне",
            relative_rect=pygame.Rect((80, screen_height - 120), (150, 40)),
            manager=self.manager,
        )

        self.set_skin_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=['1', '2', '3'],
            starting_option="1",
            relative_rect=pygame.Rect((800, screen_height - 120), (150, 40)),
            manager=self.manager,
        )

        self.best_score = self.load_best_score()
        self.record_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((screen_width // 2 - 100, 80), (200, 100)),
            text=f"Рекорд: {self.best_score[0]}\nДеньги: {self.best_score[1]}",
            manager=self.manager,
        )

    def check_skins(self):
        with open('./data/saved_inf') as file:
            ls = file.readlines()
            ls = [line.rstrip() for line in ls]
            self.skins = ls[1:-1]

    def load_best_score(self):
        try:
            with open("scores.txt", "r") as file:
                scores = [float(line.strip()) for line in file.readlines()]
                with open('./data/saved_inf') as file1:
                    return (max(scores) if scores else 0, int(file1.readlines()[0]))

        except FileNotFoundError:
            return 0
