import pygame_gui
import pygame


class ShopUI:
    def __init__(self, screen, manager, skin_images, skin_prices):
        self.screen = screen
        self.manager = manager
        # Увеличиваем изображения в 3 раза
        self.skin_images = [pygame.transform.scale(image, (image.get_width() * 3, image.get_height() * 3)) for image in skin_images]
        self.skin_prices = skin_prices
        self.buttons = []
        self.create_ui()
        with open('./data/saved_inf', 'r') as file:
            ls = file.readlines()
            ls = [line.rstrip() for line in ls]
            self.money = int(ls[0])
            self.skins = ls[1:-1]

    def create_ui(self):
        button_width = 150
        button_height = 50
        button_y = 500  # Сдвигаем кнопки на 100 пикселей ниже
        spacing = 50

        for i, (image, price) in enumerate(zip(self.skin_images, self.skin_prices)):
            button_x = 100 + i * (button_width + spacing)
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((button_x, button_y), (button_width, button_height)),
                text=f'Купить за {price}',
                manager=self.manager
            )
            self.buttons.append(button)

    def draw(self):
        for i, (image, button) in enumerate(zip(self.skin_images, self.buttons)):
            image_x = button.rect.centerx - image.get_width() // 2
            image_y = button.rect.y - image.get_height() - 10
            self.screen.blit(image, (image_x, image_y))

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            for i, button in enumerate(self.buttons):
                if event.ui_element == button:
                    if self.buy_skin(i):
                        print(f"Скин {i + 1} куплен!")
                    else:
                        print("Недостаточно денег!")

    def buy_skin(self, skin_index):
        if skin_index not in self.skins:
            if self.skin_prices[skin_index] <= self.money:
                self.money -= 100
                self.skins.append(skin_index)
                self.write_current_skin(skin_index)
                return True
        return False

    def write_current_skin(self, skin_num):
        with open('./data/saved_inf', 'r') as file:
            lines = file.readlines()

        # Меняем первую строку
        lines[-1] = f"cur_skin: {skin_num}"
        lines[0] = f"{self.money}\n"

        # Записываем обратно в файл
        with open('./data/saved_inf', 'w') as file:
            file.writelines(lines)