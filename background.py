import pygame.sprite
from random import randint
from all_sprites_group import all_sprites_group
from setting import *


# класс для "активных" спрайтов
class ActiveSpriteStatic(pygame.sprite.Sprite):
    def __init__(self, pos, group, path):
        super().__init__(group)
        self.image = pygame.transform.rotozoom(pygame.image.load(path).convert_alpha(), 0, 0.3)
        self.rect = self.image.get_rect(topleft=pos)


class Background:
    def __init__(self):

        self.screen_width, self.screen_height = map(lambda x: x * 2, screen.get_size())

        self.texture = pygame.Surface((self.screen_width, self.screen_height)).convert_alpha()

    # заполнить фон(texture) картинкой
    def texture_fill_picture(self, path):
        self.texture = pygame.image.load(path).convert_alpha()

    # заполнить с помощью одной картинки
    def texture_fill_main(self, path):
        texture_main = pygame.image.load(path).convert_alpha()
        texture_width, texture_height = texture_main.get_size()
        repeat_x = self.screen_width // texture_width
        repeat_y = self.screen_height // texture_height

        for x in range(repeat_x):
            for y in range(repeat_y):
                self.texture.blit(texture_main, (x * texture_width, y * texture_height))

    # добавление в фон второстепенных изображений(камни, кусты...)
    def texture_fill_secondary(self, path, amount, size=1.0):
        image = pygame.transform.rotozoom(pygame.image.load(path).convert_alpha(), 0, size)

        for _ in range(amount):
            self.texture.blit(image, (randint(0, self.screen_width), randint(0, self.screen_height)))

    # добавление в группу all_sprites_group "активных" спрайтов (обновляются в зависимости от их координаты y)
    def sprite_active(self, path, amount):
        for _ in range(amount):
            ActiveSpriteStatic((randint(60, self.screen_width - 60), randint(60, self.screen_height - 60)),
                               all_sprites_group, path)

    def draw(self):
        screen.blit(self.texture, (0, 0))

    def get_texture_desert(self):
        self.texture_fill_main('sprites/backgrounds/tile1.png')
        self.texture_fill_secondary('sprites/backgrounds/tile2.png', 20)
        self.texture_fill_secondary('sprites/backgrounds/tile3.png', 20)
        self.texture_fill_secondary('sprites/backgrounds/tile4.png', 20)
        self.texture_fill_secondary('sprites/PNG/greenery_6.png', 20, 0.5)
        self.sprite_active('sprites/PNG/greenery_1.png', 15)
        self.sprite_active('sprites/PNG/decor_8.png', 1)
        self.sprite_active('sprites/PNG/decor_2.png', 1)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = Background()
background.get_texture_desert()
