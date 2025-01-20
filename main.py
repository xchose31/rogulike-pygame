import pygame
import pygame_gui

pygame.init()
screen = pygame.display.set_mode((800, 600))
manager = pygame_gui.UIManager((800, 600))

button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((350, 275), (100, 50)),
    text="Нажми меня",
    manager=manager
)

clock = pygame.time.Clock()
running = True

while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)

    manager.update(time_delta)
    screen.fill((0, 0, 0))
    manager.draw_ui(screen)
    pygame.display.update()
