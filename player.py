import pygame
import math
from music import *
from bullet import *
from background import *
import random


def get_record(command, new_record=0):
    """
    Функция для работы с записью рекорда.

    :param command: Строка, указывающая, что нужно сделать с файлом рекорда:
                    'write' — записать новый рекорд, 'read' — прочитать текущий рекорд.
    :param new_record: Новый рекорд, который нужно записать в файл (только для 'write').
    :return: Текущий рекорд из файла (только для 'read').
    """
    file_path = 'record.txt'

    if command == 'write':
        with open(file_path, 'w') as f:
            f.write(f'record = {new_record}\n')
    elif command == 'read':
        with open(file_path, 'r') as f:
            record = f.readline()
            return int(record.split('=')[1].strip())


class Player(pygame.sprite.Sprite):
    """
    Класс, представляющий игрока. Этот класс управляет всеми действиями игрока,
    включая движение, стрельбу, здоровье, перезарядку и повышение уровня.

    Атрибуты:
    - pos: Позиция игрока на экране.
    - image: Изображение игрока.
    - hitbox_rect: Прямоугольник, ограничивающий игрока для столкновений.
    - player_data: Словарь с данными игрока (например, здоровье, очки, уровень).
    - invincible: Признак бессмертия игрока (пока не используется).
    - get_hurt_time: Время, когда игрок был ранен.
    - death: Признак смерти игрока.
    - reload_timer: Таймер для отсчета времени перезарядки.
    """

    def __init__(self):
        """
        Конструктор класса, инициализирует все параметры игрока, включая позицию,
        изображение, урон, скорость и другие данные.
        """
        super().__init__()
        self.pos = pygame.math.Vector2(game_settings['player_start_x'], game_settings['player_start_y'])
        self.image = pygame.transform.rotozoom(pygame.image.load("sprites/player/wizard.png").convert_alpha(), 0, 0.5)
        self.base_image = self.image
        self.hitbox_rect = self.base_image.get_rect(center=self.pos)
        self.rect = self.hitbox_rect.copy()
        self.shoot = False

        # Инициализация данных игрока
        self.player_data = {'score': 0, 'record': 0, 'get_hurt_count': 0, 'health_amount': 3, 'shoot_cooldown': 0,
                            'speedx': 6, 'speedy': 6, 'enemy_killed': 0, 'wave': 1,
                            'damage': game_settings['PLAYER_DAMAGE'],
                            'level': 1, 'ammo': 10, 'max_ammo': 10}

        self.invincible = 0
        self.get_hurt_time = 0
        self.death = False
        self.image_blood = pygame.image.load('sprites/player/blood.png').convert_alpha()

        # Механика перезарядки
        self.reloading = False
        self.reload_time = 100
        self.reload_timer = 0

        self.velocity_x = 0
        self.velocity_y = 0
        self.angle = 0

        self.step_sound_timer = 0

    def player_rotation(self):
        """
        Ориентирует игрока в сторону мыши, вращая его изображение в зависимости от угла.
        """
        mouse_coords = pygame.mouse.get_pos()
        x_change_mouse_player = (mouse_coords[0] - WIDTH // 2)
        y_change_mouse_player = (mouse_coords[1] - HEIGHT // 2)
        self.angle = math.degrees(math.atan2(y_change_mouse_player, x_change_mouse_player))
        self.image = pygame.transform.rotate(self.base_image, -self.angle)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)

    def user_input(self):
        """
        Обрабатывает ввод с клавиатуры и мыши для движения, стрельбы и перезарядки.
        """
        keys = pygame.key.get_pressed()
        moving = False

        if keys[pygame.K_w]:
            self.velocity_y = -self.player_data['speedy']
            moving = True
        if keys[pygame.K_s]:
            self.velocity_y = self.player_data['speedy']
            moving = True
        if keys[pygame.K_d]:
            self.velocity_x = self.player_data['speedx']
            moving = True
        if keys[pygame.K_a]:
            self.velocity_x = -self.player_data['speedx']
            moving = True

        if keys[pygame.K_r]:
            self.start_reload()

        # Нормализация движения по диагонали
        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

        #стрельба на пробел или ЛКМ
        if pygame.mouse.get_pressed() == (1, 0, 0) or keys[pygame.K_SPACE]:
            self.shoot = True
            self.is_shooting()
        else:
            self.shoot = False

        #для возспроизведения звука шагов с задержкой
        if moving and self.step_sound_timer == 0:
            step_sound1.play()
            self.step_sound_timer = 15

    def is_shooting(self):
        """
        Проверяет, можно ли стрелять, и если да, создает пулю и выстреливает.
        """
        if self.player_data['shoot_cooldown'] == 0 and self.player_data['ammo'] > 0:
            self.player_data['ammo'] -= 1
            self.player_data['shoot_cooldown'] = game_settings['SHOOT_COOLDOWN']
            spawn_bullet_pos = self.pos
            bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, 'player')
            bullet_group.add(bullet)
            all_sprites_group.add(bullet)
            shoot_sound.play()

    def start_reload(self):
        """
        Начинает процесс перезарядки, если игрок не находится в процессе перезарядки.
        """
        reload_sound.stop()
        reload_sound.play()
        if not self.reloading:
            self.reloading = True
            self.reload_timer = self.reload_time

    def move(self):
        """
        Обновляет позицию игрока на экране, двигаясь в соответствии с текущими скоростями.
        """
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center

    def limit(self):
        """
        Ограничивает движение игрока, чтобы он не выходил за пределы экрана.
        """
        if self.pos[0] <= 0:
            self.pos[0] = 0
        if self.pos[1] <= 0:
            self.pos[1] = 0
        if self.pos[0] >= WIDTH * 2:
            self.pos[0] = WIDTH * 2
        if self.pos[1] >= HEIGHT * 2:
            self.pos[1] = HEIGHT * 2

    def check_bullet_collision(self):
        """
        Проверяет, столкнулся ли игрок с вражеской пулей.
        """
        for sprite in enemy_bullet_group:
            if sprite.rect.colliderect(self.rect):
                sprite.kill()
                self.player_hurt()
                break

    def player_hurt(self):
        """
        Обрабатывает попадание пули по игроку, уменьшает здоровье и отображает эффект крови.
        """
        background.texture.blit(self.image_blood, self.rect)
        self.player_data['get_hurt_count'] += 1
        damage_sound.play()

    def level_up(self):
        """
        Повышает уровень игрока в зависимости от его очков. Увеличивает урон и максимальное количество патронов.
        """
        if self.player_data['score'] >= 20 and self.player_data['level'] == 1:
            level_up_sound.play()
            self.player_data['level'] += 1
            self.player_data['damage'] += 5
            self.player_data['max_ammo'] += 5

        if self.player_data['score'] >= 50 and self.player_data['level'] == 2:
            level_up_sound.play()
            self.player_data['level'] += 1
            self.player_data['max_ammo'] += 5
            self.player_data['damage'] += 10

        if self.player_data['score'] >= 90 and self.player_data['level'] == 3:
            level_up_sound.play()
            self.player_data['level'] += 1
            self.player_data['max_ammo'] += 5
            self.player_data['damage'] += 10

        if self.player_data['score'] >= 140 and self.player_data['level'] == 4:
            self.player_data['level'] += 1
            level_up_sound.play()
            self.player_data['damage'] += 10
            self.player_data['max_ammo'] += 10

    def player_reset(self):
        """
        Сбрасывает данные игрока (очки, уровень, здоровье и т.д.) к исходным значениям.
        """
        self.player_data = {'score': 0, 'record': 0, 'get_hurt_count': 0, 'health_amount': 3, 'shoot_cooldown': 0,
                            'speedx': 6, 'speedy': 6, 'enemy_killed': 0, 'wave': 1,
                            'damage': game_settings['PLAYER_DAMAGE'], 'level': 1, 'ammo': 10, 'max_ammo': 10}
        self.pos = pygame.math.Vector2(game_settings['player_start_x'], game_settings['player_start_y'])

    def update(self):
        """
        Обновляет состояние игрока (проверка столкновений, движение, стрельба, перезарядка, повышение уровня).
        """
        self.check_bullet_collision()
        self.player_rotation()
        self.user_input()
        self.move()
        self.limit()
        self.level_up()

        if self.player_data['shoot_cooldown'] > 0:
            self.player_data['shoot_cooldown'] -= 1

        if self.reloading:
            self.reload_timer -= 1
            if self.reload_timer <= 0:
                self.reloading = False
                self.player_data['ammo'] = self.player_data['max_ammo']

        if self.step_sound_timer > 0:
            self.step_sound_timer -= 1


# Создание объекта игрока
player = Player()
