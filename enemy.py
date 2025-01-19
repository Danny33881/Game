import pygame.time
from all_sprites_group import all_sprites_group
from player import player
from bullet import *
from random import randint
from background import screen
from camera import camera
from HUD import text_group
from HUD import font

pygame.font.init()
enemy_group = pygame.sprite.Group()
loot_group = pygame.sprite.Group()


def enemy_reset():
    for sprite in enemy_group:
        sprite.kill()


def loot_reset():
    for sprite in loot_group:
        sprite.kill()


def bullet_reset():
    for sprite in bullet_group:
        sprite.kill()
    for sprite in enemy_bullet_group:
        sprite.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__(enemy_group, all_sprites_group)
        # Для анимации
        self.images = []
        self.images_attack = []
        self.animation_offset = randint(0, 8)
        self.sheet_animation()
        self.animation_sprites = []
        self.image = self.images[0]
        self.is_attacking = False
        self.attack_timer = 0
        self.count_frames = 0

        self.health = 100
        self.invincible = 0
        self.rareness = 0

        self.collide = False

        self.rect = self.image.get_rect()
        self.rect.center = position

        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()
        self.speed = game_settings['ENEMY_SPEED']

        self.position = pygame.math.Vector2(position)

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

    def check_collision(self):
        if self.invincible <= 0:
            for sprite in bullet_group:
                if sprite.rect.colliderect(self.rect):
                    self.collide = True
                    sprite.kill()
                    self.health -= game_settings['PLAYER_DAMAGE']
                if self.health <= 0:
                    all_sprites_group.add(Loot(self.rect.x, self.rect.y, self.rareness))
                    player.player_data['enemy_killed'] += 1
                    self.kill()

        else:
            self.invincible -= 1

        if self.rect.colliderect(player.hitbox_rect):
            self.is_attacking = True

            if pygame.time.get_ticks() - self.attack_timer > 1000:
                self.attack_timer = pygame.time.get_ticks()
                if pygame.time.get_ticks() - player.get_hurt_time > 1000:
                    player.get_hurt_time = pygame.time.get_ticks()
                    player.player_hurt()

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

    def get_vector_distance(self, vector_1, vector_2):
        return (vector_1 - vector_2).magnitude()

    def update(self):
        self.check_collision()
        self.hunt_player()
        if self.is_attacking:
            self.animation('attack', attack_speed=0.1)
        else:
            self.animation('walk')
        self.draw_enemy_health()


class Mage(Enemy):
    def __init__(self, position):
        super().__init__(position)
        self.rareness = 1
        self.images = []
        self.images_attack = []
        self.sheet_animation()
        self.image = self.images[0]

    def hunt_player(self):
        if self.is_attacking == 0:
            player_vector = pygame.math.Vector2(player.hitbox_rect.center)
            enemy_vector = pygame.math.Vector2(self.rect.center)
            distance = self.get_vector_distance(player_vector, enemy_vector)
            if distance <= 300:
                self.is_attacking = True
                self.shoot()
            else:
                super().hunt_player()

    def sheet_animation(self):
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

    def shoot(self):
        x_change_enemy_player = (player.rect.x - self.position.x)
        y_change_enemy_player = (player.rect.y - self.position.y)
        angle = math.degrees(math.atan2(y_change_enemy_player, x_change_enemy_player))
        bullet = Bullet(self.position.x, self.position.y, angle, 'enemy')
        enemy_bullet_group.add(bullet)
        all_sprites_group.add(bullet)


class Skeleton(Enemy):
    def __init__(self, position):
        super().__init__(position)
        self.rareness = 3
        self.health = 125

        self.images = []
        self.images_attack = []
        self.sheet_animation()
        self.image = self.images[0]

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
        self.speed_x, self.speed_y = randint(-5, 5), randint(-5, 5)

        self.spawn_time = pygame.time.get_ticks()

    def spawn_animation(self):
        elapsed_time = pygame.time.get_ticks() - self.spawn_time
        if elapsed_time <= 100:
            self.rect.y += self.speed_y 
            self.rect.x += self.speed_x

    def check_collision(self):
        for sprite in loot_group:
            if sprite.rect.colliderect(player.rect):
                player.player_data['score'] += sprite.points
                AnimatedText(player.rect.x, player.rect.y - 30, '+' + str(sprite.points), sprite.color)
                sprite.kill()

    def update(self):
        self.check_collision()
        self.spawn_animation()
