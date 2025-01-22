import pygame.time
from all_sprites_group import all_sprites_group
from player import player
from bullet import *
from random import randint
from background import *
from camera import camera
from HUD import text_group
from HUD import font
from music import *

pygame.font.init()
enemy_group = pygame.sprite.Group()
loot_group = pygame.sprite.Group()

# Функция для сброса врагов (очистка группы врагов)
def enemy_reset():
    for sprite in enemy_group:
        sprite.kill()

# Функция для сброса лута (очистка группы лута)
def loot_reset():
    for sprite in loot_group:
        sprite.kill()

# Функция для сброса пуль (очистка групп пуль игрока и врагов)
def bullet_reset():
    for sprite in bullet_group:
        sprite.kill()
    for sprite in enemy_bullet_group:
        sprite.kill()

# Класс "Enemy" (враг) описывает общую логику врагов
class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__(enemy_group, all_sprites_group)
        # Анимация врага
        self.images = []  # Кадры анимации передвижения
        self.images_attack = []  # Кадры анимации атаки
        self.animation_offset = randint(0, 8)  # Смещение для начала анимации
        self.sheet_animation()  # Инициализация кадров анимации
        self.animation_sprites = []  # Активные кадры анимации
        self.image = self.images[0]  # Установка первого кадра
        self.is_attacking = False  # Флаг атаки
        self.attack_timer = 0  # Таймер для задержки атаки
        self.count_frames = 0  # Счётчик кадров анимации
        self.invincible = 0  # Время неуязвимости после получения урона
        self.health = 100  # Здоровье врага
        self.rareness = 0  # Редкость врага (для выпадения лута)

        self.collide = False  # Флаг столкновения

        self.rect = self.image.get_rect()
        self.rect.center = position  # Установка позиции врага

        self.direction = pygame.math.Vector2()  # Направление движения
        self.velocity = pygame.math.Vector2()  # Скорость движения
        self.speed = game_settings['ENEMY_SPEED']  # Скорость врага

        self.position = pygame.math.Vector2(position)  # Текущая позиция врага

        self.image_blood = pygame.image.load('sprites/player/blood.png').convert_alpha()  # Кровь для эффекта смерти

    # Логика преследования игрока
    def hunt_player(self):
        if self.is_attacking == 0:
            player_vector = pygame.math.Vector2(player.hitbox_rect.center)
            enemy_vector = pygame.math.Vector2(self.rect.center)
            distance = self.get_vector_distance(player_vector, enemy_vector)

            if distance > 0:
                self.direction = (player_vector - enemy_vector).normalize()
            else:
                self.direction = pygame.math.Vector2()

            self.velocity = self.direction * self.speed
            self.position += self.velocity

            self.rect.centerx = self.position.x
            self.rect.centery = self.position.y

    # Проверка столкновений с пулями или игроком
    def check_collision(self):
        if self.invincible <= 0:
            for sprite in bullet_group:
                if sprite.rect.colliderect(self.rect):
                    self.collide = True
                    sprite.kill()
                    self.health -= player.player_data['damage']  # Урон от пули игрока
                if self.health <= 0:
                    all_sprites_group.add(Loot(self.rect.x, self.rect.y, self.rareness))  # Спавн лута при смерти
                    player.player_data['enemy_killed'] += 1
                    self.kill()
                    enemy_death_sound.play()  # Звук смерти врага
                    background.texture.blit(self.image_blood, self.rect)  # Эффект крови
        else:
            self.invincible -= 1

        if self.rect.colliderect(player.hitbox_rect):  # Проверка столкновения с игроком
            self.is_attacking = True

            if pygame.time.get_ticks() - self.attack_timer > 1000:  # Задержка атаки
                self.attack_timer = pygame.time.get_ticks()
                if pygame.time.get_ticks() - player.get_hurt_time > 1000:
                    player.get_hurt_time = pygame.time.get_ticks()
                    player.player_hurt()  # Нанесение урона игроку

    # Рисование полоски здоровья врага
    def draw_enemy_health(self):
        if self.health > 60:
            col = game_settings['GREEN']
        elif self.health > 30:
            col = game_settings['YELLOW']
        else:
            col = game_settings['RED']
        width = int(self.rect.width * self.health / 100)
        pygame.draw.rect(screen, col, (self.rect.x - camera.offset.x,
                                       self.rect.y - camera.offset.y + self.rect.height, width, 3))
        #отрисовка относительно положения врага

    # Анимация врага (ходьба или атака)
    def animation(self, type, walk_speed=0., attack_speed=0.):
        if type == 'walk':
            self.animation_sprites = self.images
            self.count_frames += walk_speed
        elif type == 'attack':
            self.animation_sprites = self.images_attack
            self.count_frames += attack_speed
        self.count_frames += 0.1
        if self.count_frames > len(self.animation_sprites):
            self.is_attacking = False
            self.count_frames = 0
        if self.rect.centerx > player.hitbox_rect.centerx:
            self.image = pygame.transform.flip(self.animation_sprites[int(self.count_frames)], True, False)
        else:
            self.image = self.animation_sprites[int(self.count_frames)]

    # Расчёт расстояния между двумя векторами
    def get_vector_distance(self, vector_1, vector_2):
        return (vector_1 - vector_2).magnitude()

    # Обновление состояния врага (вызывается каждый кадр)
    def update(self):
        self.check_collision()
        self.hunt_player()
        if self.is_attacking:
            self.animation('attack', attack_speed=0.1)
        else:
            self.animation('walk')
        self.draw_enemy_health()




class Mage(Enemy):
    #Обновленные атрибуты
    def __init__(self, position):
        super().__init__(position)
        self.rareness = 1
        self.health = 100
        self.images = []
        self.images_attack = []
        self.sheet_animation()
        self.image = self.images[0]


    def hunt_player(self): #растояние для атаки(новая логика)
        if self.is_attacking == 0:
            player_vector = pygame.math.Vector2(player.hitbox_rect.center)
            enemy_vector = pygame.math.Vector2(self.rect.center)
            distance = self.get_vector_distance(player_vector, enemy_vector)
            if distance <= 300:
                self.is_attacking = True
                self.shoot()
            else:
                super().hunt_player()

    def sheet_animation(self): #отрисовка злодея
        sprite_sheet = pygame.image.load('sprites/enemy/mage_run.png').convert_alpha()
        sprite_sheet_attack = pygame.image.load('sprites/enemy/mage_attack.png').convert_alpha()
        for i in range(8):
            sprite_rect = pygame.Rect((i + self.animation_offset) % 8 * 65, 0, 65, 63)
            sprite_image = sprite_sheet.subsurface(sprite_rect)
            self.images.append(pygame.transform.rotozoom(sprite_image.convert_alpha(), 0, 0.6))
        for i in range(7):
            sprite_rect = pygame.Rect(i * 138, 0, 138, 99)
            sprite_image = sprite_sheet_attack.subsurface(sprite_rect)
            self.images_attack.append(pygame.transform.rotozoom(sprite_image.convert_alpha(), 0, 0.6))

    def shoot(self): #логика стрельбы
        x_change_enemy_player = (player.rect.x - self.position.x)
        y_change_enemy_player = (player.rect.y - self.position.y)
        angle = math.degrees(math.atan2(y_change_enemy_player, x_change_enemy_player))
        bullet = Bullet(self.position.x, self.position.y, angle, 'enemy')
        enemy_bullet_group.add(bullet)
        all_sprites_group.add(bullet)
        mage_shoot_sound.play()


class Goblin(Enemy):
    # собственные характеристики и атрибуты
    def __init__(self, position):
        super().__init__(position)
        self.rareness = 0
        self.health = 80
        self.images = []
        self.images_attack = []
        self.sheet_animation()
        self.image = self.images[0]

    #логика движения и атаки
    def hunt_player(self):
        if self.is_attacking == 0:
            player_vector = pygame.math.Vector2(player.hitbox_rect.center)
            enemy_vector = pygame.math.Vector2(self.rect.center)
            distance = self.get_vector_distance(player_vector, enemy_vector)
            if distance <= 0:
                self.is_attacking = True
            else:
                super().hunt_player()
    #отрисовка
    def sheet_animation(self):
        sprite_sheet = pygame.image.load('sprites/enemy/goblin_run.png').convert_alpha()
        sprite_sheet_attack = pygame.image.load('sprites/enemy/goblin_attack.png').convert_alpha()
        for i in range(8):
            sprite_rect = pygame.Rect((i + self.animation_offset) % 8 * 35, 0, 35, 40)
            sprite_image = sprite_sheet.subsurface(sprite_rect)
            self.images.append(pygame.transform.rotozoom(sprite_image.convert_alpha(), 0, 1))
        for i in range(8):
            sprite_rect = pygame.Rect(i * 88, 0, 88, 46)
            sprite_image_attack = sprite_sheet_attack.subsurface(sprite_rect)
            self.images_attack.append(pygame.transform.rotozoom(sprite_image_attack.convert_alpha(), 0, 1))




class Skeleton(Enemy):
    # собственные характеристики и атрибуты
    def __init__(self, position):
        super().__init__(position)
        self.rareness = 3
        self.health = 140

        self.images = []
        self.images_attack = []
        self.sheet_animation()
        self.image = self.images[0]
    #Логика движения и атаки
    def hunt_player(self):
        if self.is_attacking == 0:
            player_vector = pygame.math.Vector2(player.hitbox_rect.center)
            enemy_vector = pygame.math.Vector2(self.rect.center)
            distance = self.get_vector_distance(player_vector, enemy_vector)
            if distance <= 5:
                self.is_attacking = True
                skeleton_attack_sound.play()
            else:
                super().hunt_player()
    #отрисовка
    def sheet_animation(self):
        sprite_sheet = pygame.image.load('sprites/enemy/skeleton_walk.png').convert_alpha()
        sprite_sheet_attack = pygame.image.load('sprites/enemy/skeleton_attack.png').convert_alpha()
        for i in range(4):
            sprite_rect = pygame.Rect((i + self.animation_offset) % 4 * 45, 0, 45, 51)
            sprite_image = sprite_sheet.subsurface(sprite_rect)
            self.images.append(pygame.transform.rotozoom(sprite_image.convert_alpha(), 0, 0.8))
        for i in range(8):
            sprite_rect = pygame.Rect(i * 150, 0, 150, 57)
            sprite_image = sprite_sheet_attack.subsurface(sprite_rect)
            self.images_attack.append(pygame.transform.rotozoom(sprite_image.convert_alpha(), 0, 0.8))


class AnimatedText(pygame.sprite.Sprite):
    count = 0

    def __init__(self, x, y, text, color):
        super().__init__(text_group, all_sprites_group)
        AnimatedText.count += 1
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.fadeout_duration = 1.5
        self.fadeout_timer = pygame.time.get_ticks() + self.fadeout_duration * 100

    def update(self):
        if pygame.time.get_ticks() > self.fadeout_timer:
            self.kill()
            AnimatedText.count -= 1


class Loot(pygame.sprite.Sprite):
    #отрисовка выпадения лута с мобов раскиданные по редкости мобов
    def __init__(self, x, y, rareness):
        super().__init__(loot_group, all_sprites_group)
        path = ''
        if rareness == 0:
            path = 'sprites/loot/gem02blue.gif'
            self.color = game_settings['BLUE']
            self.points = 1
        elif rareness == 1:
            path = 'sprites/loot/gem03yellow.gif'
            self.color = game_settings['YELLOW']
            self.points = 2
        elif rareness == 3:
            path = 'sprites/loot/gem05red.gif'
            self.color = game_settings['RED']
            self.points = 3
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x, self.speed_y = randint(-5, 5), randint(-5, 5) #вычисление до куда заспавнится лут после смерти моба

        self.spawn_time = pygame.time.get_ticks()

    def spawn_animation(self):
        #спавн частиц лута после смерти врага
        elapsed_time = pygame.time.get_ticks() - self.spawn_time
        if elapsed_time <= 100:
            self.rect.y += self.speed_y
            self.rect.x += self.speed_x

    def check_collision(self):
        #удаление частиц из мира, если игрок подобрал их
        for sprite in loot_group:
            if sprite.rect.colliderect(player.rect):
                player.player_data['score'] += sprite.points
                AnimatedText(player.rect.x, player.rect.y - 30, '+' + str(sprite.points), sprite.color)
                sprite.kill()

    def update(self):
        #обновление состояний
        self.check_collision()
        self.spawn_animation()
