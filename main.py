import pygame
import pygame_gui

pygame.init()

# Размеры экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Меню игры")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (30, 30, 30)

manager = pygame_gui.UIManager((screen_width, screen_height), theme_path=None)
play = False

button_new_game = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((300, 200), (200, 50)),
    text="Новая игра",
    manager=manager,
)

button_shop = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((300, 270), (200, 50)),
    text="Магазин",
    manager=manager,
)

button_exit = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((300, 340), (200, 50)),
    text="Выход",
    manager=manager,
)

mute_icon = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((20, screen_height - 70), (50, 50)),
    text="🔊",  # Иконка звука
    manager=manager,
)

difficulty_dropdown = pygame_gui.elements.UIDropDownMenu(
    options_list=["Легко", "Средне", "Тяжело"],
    starting_option="Средне",
    relative_rect=pygame.Rect((80, screen_height - 65), (150, 40)),
    manager=manager,
)

clock = pygame.time.Clock()
running = True

while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button_new_game:
                print("Начата новая игра!")
                play = True
            elif event.ui_element == button_shop:
                print("Открыт магазин!")
            elif event.ui_element == button_exit:
                print("Выход из игры!")
                running = False
            elif event.ui_element == mute_icon:
                if mute_icon.text == "🔊":
                    mute_icon.set_text("🔇")
                    print("Звук выключен")
                else:
                    mute_icon.set_text("🔊")
                    print("Звук включен")

        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == difficulty_dropdown:
                print(f"Выбрана сложность: {difficulty_dropdown.selected_option}")
        manager.process_events(event)
    screen.fill(BACKGROUND_COLOR)
    if not play:
        manager.update(time_delta)
        manager.draw_ui(screen)
    else:
        button_new_game.kill()
        button_exit.kill()
        button_shop.kill()
        difficulty_dropdown.kill()
        mute_icon.kill()

    pygame.display.update()


pygame.quit()
