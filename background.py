import pygame.sprite
from random import randint
from all_sprites_group import all_sprites_group
from setting import *

# Класс для "активных" спрайтов
class ActiveSpriteStatic(pygame.sprite.Sprite):
    """
    Класс, представляющий статические "активные" спрайты.
    Эти спрайты добавляются в указанную группу и могут обновляться в зависимости от их координаты y.

    Атрибуты:
        image (pygame.Surface): Изображение спрайта.
        rect (pygame.Rect): Прямоугольник, ограничивающий спрайт.
    """
    def __init__(self, pos, group, path):
        """
        Инициализация спрайта.

        Параметры:
            pos (tuple): Координаты (x, y) верхнего левого угла спрайта.
            group (pygame.sprite.Group): Группа, в которую добавляется спрайт.
            path (str): Путь к изображению спрайта.
        """
        super().__init__(group)
        self.image = pygame.transform.rotozoom(pygame.image.load(path).convert_alpha(), 0, 0.3)
        self.rect = self.image.get_rect(topleft=pos)

# Класс для работы с фоном
class Background:
    """
    Класс для создания и управления текстурированным фоном и добавления активных спрайтов.

    Атрибуты:
        screen_width (int): Ширина экрана.
        screen_height (int): Высота экрана.
        texture (pygame.Surface): Поверхность для текстуры фона.
    """
    def __init__(self):
        """
        Инициализация фона.
        """
        self.screen_width, self.screen_height = map(lambda x: x * 2, screen.get_size())
        self.texture = pygame.Surface((self.screen_width, self.screen_height)).convert_alpha()

    def texture_fill_picture(self, path):
        """
        Заполнить фон единой картинкой.

        Параметры:
            path (str): Путь к изображению.
        """
        self.texture = pygame.image.load(path).convert_alpha()

    def texture_fill_main(self, path):
        """
        Заполнить фон повторяющейся текстурой.

        Параметры:
            path (str): Путь к изображению текстуры.
        """
        texture_main = pygame.image.load(path).convert_alpha()
        texture_width, texture_height = texture_main.get_size()
        repeat_x = self.screen_width // texture_width
        repeat_y = self.screen_height // texture_height

        for x in range(repeat_x):
            for y in range(repeat_y):
                self.texture.blit(texture_main, (x * texture_width, y * texture_height))

    def texture_fill_secondary(self, path, amount, size=1.0):
        """
        Добавить дополнительные изображения (например, камни или кусты) поверх фона.

        Параметры:
            path (str): Путь к изображению.
            amount (int): Количество изображений.
            size (float): Масштаб изображения (по умолчанию 1.0).
        """
        image = pygame.transform.rotozoom(pygame.image.load(path).convert_alpha(), 0, size)

        for _ in range(amount):
            self.texture.blit(image, (randint(0, self.screen_width), randint(0, self.screen_height)))

    def sprite_active(self, path, amount):
        """
        Добавить "активные" спрайты в группу all_sprites_group.

        Параметры:
            path (str): Путь к изображению спрайта.
            amount (int): Количество спрайтов.
        """
        for _ in range(amount):
            ActiveSpriteStatic((randint(60, self.screen_width - 60), randint(60, self.screen_height - 60)),
                               all_sprites_group, path)

    def draw(self):
        """Отрисовать фон на экране."""

        screen.blit(self.texture, (0, 0))

    def get_texture_desert(self):
        """Создать текстуру для пустынного биома с основными и дополнительными элементами."""

        self.texture_fill_main('sprites/backgrounds/tile1.png')
        self.texture_fill_secondary('sprites/backgrounds/tile2.png', 20)
        self.texture_fill_secondary('sprites/backgrounds/tile3.png', 20)
        self.texture_fill_secondary('sprites/backgrounds/tile4.png', 20)
        self.texture_fill_secondary('sprites/PNG/greenery_6.png', 20, 0.5)
        self.sprite_active('sprites/PNG/greenery_1.png', 15)
        self.sprite_active('sprites/PNG/decor_8.png', 1)
        self.sprite_active('sprites/PNG/decor_2.png', 1)


# Создание окна и инициализация фона
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = Background()
background.get_texture_desert()
