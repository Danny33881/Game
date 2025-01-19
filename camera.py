from background import *
from HUD import *


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        # Получаем прямоугольник пола из текстуры фона
        self.floor_rect = background.texture.get_rect(topleft=(0, 0))

    def custom_draw(self):
        # Вычисление положения камеры с учетом того, что игрок должен находиться посередине экрана
        self.offset.x = player.rect.centerx - (WIDTH // 2)
        self.offset.y = player.rect.centery - (HEIGHT // 2)

        # Отрисовка пола
        floor_offset_pos = self.floor_rect.topleft - self.offset
        screen.blit(background.texture, floor_offset_pos)

        # Отрисовка всех спрайтов в all_sprites_group с учетом их положения по нижнему краю y
        for sprite in sorted(all_sprites_group, key=lambda sp: sp.rect.bottom):
            # Вычисление их смещения относительно положения камеры
            offset_pos = sprite.rect.topleft - self.offset

            # Отрисовка спрайта на экране
            screen.blit(sprite.image, offset_pos)
        # Отрисовка HUD
        HUD_main.update()
        screen.blit(HUD_main.HUD_surface, (0, 0))


camera = Camera()
