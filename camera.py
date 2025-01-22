from background import *
from HUD import *


class Camera(pygame.sprite.Group):
    """
    Класс для управления виртуальной камерой, которая обеспечивает смещение сцены так, чтобы игрок всегда оставался в центре экрана.

    Атрибуты:
        offset (pygame.math.Vector2): Вектор смещения камеры.
        floor_rect (pygame.Rect): Прямоугольник, представляющий пол сцены, полученный из текстуры фона.
    """

    def __init__(self):
        """
        Инициализация камеры.
        """
        super().__init__()
        self.offset = pygame.math.Vector2()
        # Получаем прямоугольник пола из текстуры фона
        self.floor_rect = background.texture.get_rect(topleft=(0, 0))

    def custom_draw(self):
        """
        Отрисовка сцены с учетом положения камеры.

        1. Вычисляет смещение камеры, чтобы игрок находился в центре экрана.
        2. Отрисовывает фон (пол) с учетом смещения.
        3. Отрисовывает все спрайты из группы all_sprites_group, отсортированные по их нижнему краю (y).
        4. Отрисовывает HUD поверх всей сцены.
        """
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


# Создание экземпляра камеры
camera = Camera()
