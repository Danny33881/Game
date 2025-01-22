import pygame.sprite
import pygame.font
from player import player
from setting import *

pygame.font.init()

# Создаем группы спрайтов для текста и HUD
text_group = pygame.sprite.Group()
font = pygame.font.Font("font/PublicPixel.ttf", 15)  # Шрифт для текста
hud_group = pygame.sprite.Group()


class HUD(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Поверхность для отображения HUD
        self.HUD_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA).convert_alpha()

        # Загружаем изображения для здоровья (полное и пустое)
        self.health_full_image = pygame.image.load('sprites/player/health_full.png')
        self.health_empty_image = pygame.image.load('sprites/player/health_empty.png')

        # Прямоугольник для полного здоровья
        self.health_rect = self.health_full_image.get_rect()

    def health_draw(self):
        """
        Отображает индикатор здоровья игрока на экране.
        - Сначала рисуется пустая шкала здоровья.
        - Затем рисуются "здоровые сердечки", в зависимости от количества здоровья.
        """
        # Отображаем пустое здоровье
        self.HUD_surface.blit(self.health_empty_image, (10, HEIGHT - self.health_rect.height - 50))

        # Подсчитываем количество "здоровых сердечек"
        repeat = 3 - player.player_data['get_hurt_count']  # Максимум 3 сердечка
        for i in range(repeat):
            # Вырезаем отдельное сердечко и рисуем его
            sprite_rect = pygame.Rect(i * 43, 0, 43, 37)
            one_heart_image = self.health_full_image.subsurface(sprite_rect)
            self.HUD_surface.blit(one_heart_image, (10 + i * 43, HEIGHT - self.health_rect.height - 50))

    def text_draw(self):
        """
        Отображает текстовые данные: счёт, волну, уровень и ману.
        """
        # Отображение текста для различных данных
        text_image_score = font.render('score:' + str(player.player_data['score']), True, game_settings['WHITE'])
        text_image_wave = font.render('wave:' + str(player.player_data['wave']), True, game_settings['WHITE'])
        text_image_ammo = font.render(f"mana:{player.player_data['ammo']}/{player.player_data['max_ammo']}", True,
                                      game_settings['WHITE'])
        text_image_level = font.render('level:' + str(player.player_data['level']), True, game_settings['WHITE'])

        # Размещение текста на поверхности HUD
        self.HUD_surface.blit(text_image_score, (10, 30))
        self.HUD_surface.blit(text_image_wave, (10, 60))
        self.HUD_surface.blit(text_image_level, (10, 90))
        self.HUD_surface.blit(text_image_ammo, (10, 120))

    def update(self):
        """
        Обновляет содержание HUD:
        - Очищает поверхность HUD.
        - Вызывает методы для рисования здоровья и текста.
        """
        self.HUD_surface.fill((0, 0, 0, 0))  # Очищаем поверхность
        self.health_draw()  # Рисуем здоровье
        self.text_draw()  # Рисуем текстовые данные


# Создание главного объекта HUD
HUD_main = HUD()

