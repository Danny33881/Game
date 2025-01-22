from setting import *
import pygame.sprite
import math

# Группы для хранения пуль
bullet_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()


class Bullet(pygame.sprite.Sprite):
    """
    Класс для создания и управления пулями в игре.

    Атрибуты:
        images (list): Список кадров анимации пули.
        sprite_sheet (pygame.Surface): Спрайт-лист с изображениями пули.
        bullet_type (str): Тип пули ('player' или 'enemy').
        image (pygame.Surface): Текущий кадр анимации пули.
        rect (pygame.Rect): Прямоугольник, ограничивающий пулю.
        x, y (float): Текущие координаты пули.
        angle (float): Угол направления пули (в градусах).
        speed (float): Скорость пули.
        bullet_lifetime (int): Максимальное время жизни пули (в миллисекундах).
        count_frames (float): Счетчик кадров для анимации пули.
        spawn_time (int): Время появления пули (в миллисекундах).
        x_vel, y_vel (float): Изменение координат пули по x и y.
    """

    def __init__(self, x, y, angle, bullet_type):
        """
        Инициализация пули.

        Параметры:
            x (float): Начальная координата x пули.
            y (float): Начальная координата y пули.
            angle (float): Угол направления пули (в градусах).
            bullet_type (str): Тип пули ('player' или 'enemy').
        """
        super().__init__()

        # Загрузка спрайт-листа в зависимости от типа пули
        self.images = []
        if bullet_type == 'player':
            self.sprite_sheet = pygame.image.load('sprites/bullet/green_bullet.png').convert_alpha()
        else:
            self.sprite_sheet = pygame.image.load('sprites/bullet/fire_bullet.png').convert_alpha()

        # Разделение спрайт-листа на отдельные кадры
        for i in range(4):
            sprite_rect = pygame.Rect(i * 16, 0, 16, 16)
            sprite_image = self.sprite_sheet.subsurface(sprite_rect)
            self.images.append(pygame.transform.rotozoom(sprite_image.convert_alpha(), 0, 1.5))

        # Инициализация атрибутов
        self.bullet_type = bullet_type
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = game_settings['BULLET_SPEED']
        self.bullet_lifetime = game_settings['BULLET_LIFETIME']
        self.count_frames = 0
        self.spawn_time = pygame.time.get_ticks()

        # Вычисление скоростей по осям x и y на основе угла
        self.x_vel = math.cos(self.angle * (2 * math.pi / 360)) * self.speed
        self.y_vel = math.sin(self.angle * (2 * math.pi / 360)) * self.speed
        self.rect_player = ()

    def bullet_movement(self):
        """
        Управление движением пули.

        Вычисляет новые координаты пули на основе скоростей x_vel и y_vel.
        Уничтожает пулю, если время её существования превышает bullet_lifetime.
        """
        self.x += self.x_vel
        self.y += self.y_vel
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # Уничтожение пули, если она существует дольше указанного времени
        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()

    def bullet_animation(self):
        """
        Обновление анимации пули.

        Меняет текущий кадр пули на основе count_frames.
        """
        self.count_frames += 0.2
        if self.count_frames > 4:
            self.count_frames = 0
        self.image = self.images[int(self.count_frames)]

    def update(self):
        """
        Обновление состояния пули (движение и анимация).
        """
        self.bullet_movement()
        self.bullet_animation()
