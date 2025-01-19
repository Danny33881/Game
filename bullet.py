from setting import *
import pygame.sprite
import math


bullet_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, bullet_type):
        super().__init__()
        # загрузка sprite sheet и его обрезка для последующей анимации пули
        self.images = []
        if bullet_type == 'player':
            self.sprite_sheet = pygame.image.load('sprites/bullet/green_bullet.png').convert_alpha()
        else:
            self.sprite_sheet = pygame.image.load('sprites/bullet/fire_bullet.png').convert_alpha()
        for i in range(4):
            sprite_rect = pygame.Rect(i * 16, 0, 16, 16)
            sprite_image = self.sprite_sheet.subsurface(sprite_rect)
            self.images.append(pygame.transform.rotozoom(sprite_image.convert_alpha(), 0, 1.5))
        # инициализация нужных переменных
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
        # вычисление x_vel и y_vel, характеризующих изменение положения пули по x и y
        self.x_vel = math.cos(self.angle * (2*math.pi/360)) * self.speed
        self.y_vel = math.sin(self.angle * (2*math.pi/360)) * self.speed
        self.rect_player = ()

    def bullet_movement(self):
        # вычисление новых координат пули с учетом x_vel и y_vel
        self.x += self.x_vel
        self.y += self.y_vel
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # уничтожение пули, если она существует дольше чем bullet_lifetime
        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()

    def bullet_animation(self):
        self.count_frames += 0.2
        if self.count_frames > 4:
            self.count_frames = 0
        self.image = self.images[int(self.count_frames)]

    def update(self):
        self.bullet_movement()
        self.bullet_animation()
