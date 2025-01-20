from music import *
from bullet import *
from background import *
import random


def get_record(command, new_record=0):
    file_path = 'record.txt'

    if command == 'write':
        with open(file_path, 'w') as f:
            f.write(f'record = {new_record}\n')
    elif command == 'read':
        with open(file_path, 'r') as f:
            record = f.readline()
            return int(record.split('=')[1].strip())


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pygame.math.Vector2(game_settings['player_start_x'], game_settings['player_start_y'])
        self.image = pygame.transform.rotozoom(pygame.image.load("sprites/player/wizard.png").convert_alpha(), 0, 0.5)
        self.base_image = self.image
        self.hitbox_rect = self.base_image.get_rect(center=self.pos)
        self.rect = self.hitbox_rect.copy()
        self.shoot = False
        damage = game_settings['PLAYER_DAMAGE']

        self.player_data = {'score': 0, 'record': 0, 'get_hurt_count': 0, 'health_amount': 3, 'shoot_cooldown': 0,
                            'speedx': 6, 'speedy': 6, 'enemy_killed': 0, 'wave': 1, 'damage': damage}

        self.invincible = 0
        self.get_hurt_time = 0
        self.death = False
        self.image_blood = pygame.image.load('sprites/player/blood.png').convert_alpha()

        self.velocity_x = 0
        self.velocity_y = 0
        self.angle = 0

        self.level = 1

        self.step_sound_timer = 0

    def player_rotation(self):
        mouse_coords = pygame.mouse.get_pos()
        x_change_mouse_player = (mouse_coords[0] - WIDTH // 2)
        y_change_mouse_player = (mouse_coords[1] - HEIGHT // 2)
        self.angle = math.degrees(math.atan2(y_change_mouse_player, x_change_mouse_player))
        self.image = pygame.transform.rotate(self.base_image, -self.angle)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)

    def user_input(self):
        keys = pygame.key.get_pressed()
        moving = False

        if keys[pygame.K_w]:
            self.velocity_y = -self.player_data['speedy']
            moving = True
        if keys[pygame.K_s]:
            self.velocity_y = self.player_data['speedy']
            moving =True
        if keys[pygame.K_d]:
            self.velocity_x = self.player_data['speedx']
            moving = True
        if keys[pygame.K_a]:
            self.velocity_x = -self.player_data['speedx']
            moving = True

        if self.velocity_x != 0 and self.velocity_y != 0:  # moving diagonally
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

        if pygame.mouse.get_pressed() == (1, 0, 0) or keys[pygame.K_SPACE]:
            self.shoot = True
            self.is_shooting()
        else:
            self.shoot = False

        if moving and self.step_sound_timer == 0:
            f = [step_sound1, step_sound2]
            random.choice(f).play()
            self.step_sound_timer = 15

    def is_shooting(self):
        if self.player_data['shoot_cooldown'] == 0:
            self.player_data['shoot_cooldown'] = game_settings['SHOOT_COOLDOWN']
            spawn_bullet_pos = self.pos
            bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, 'player')
            bullet_group.add(bullet)
            all_sprites_group.add(bullet)
            shoot_sound.play()

    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center

    def limit(self):
        if self.pos[0] <= 0:
            self.pos[0] = 0
        if self.pos[1] <= 0:
            self.pos[1] = 0
        if self.pos[0] >= WIDTH * 2:
            self.pos[0] = WIDTH * 2
        if self.pos[1] >= HEIGHT * 2:
            self.pos[1] = HEIGHT * 2

    def check_bullet_collision(self):
        for sprite in enemy_bullet_group:
            if sprite.rect.colliderect(self.rect):
                sprite.kill()
                self.player_hurt()
                break

    def player_hurt(self):
        background.texture.blit(self.image_blood, self.rect)
        self.player_data['get_hurt_count'] += 1
        damage_sound.play()

    def level_up(self):
        if self.player_data['score'] >= 20 and self.level == 1:
            self.level += 1
            level_up_sound.play()
            self.player_data['damage'] += 5
        if self.player_data['score'] >= 50 and self.level == 2:
            self.level += 1
            level_up_sound.play()
            self.player_data['damage'] += 5
        if self.player_data['score'] >= 90 and self.level == 3:
            self.level += 1
            level_up_sound.play()
            self.player_data['damage'] += 10
        if self.player_data['score'] >= 140 and self.level == 4:
            self.level += 1
            level_up_sound.play()
            self.player_data['damage'] += 10

    def player_reset(self):
        self.player_data = {'score': 0, 'record': 0, 'get_hurt_count': 0, 'health_amount': 3, 'shoot_cooldown': 0,
                            'speedx': 6, 'speedy': 6, 'enemy_killed': 0, 'wave': 1, 'damage': game_settings['PLAYER_DAMAGE']}
        self.pos = pygame.math.Vector2(game_settings['player_start_x'], game_settings['player_start_y'])

    def update(self):
        self.check_bullet_collision()
        self.player_rotation()
        self.user_input()
        self.move()
        self.limit()
        self.level_up()

        if self.player_data['shoot_cooldown'] > 0:
            self.player_data['shoot_cooldown'] -= 1

        if self.step_sound_timer > 0:
            self.step_sound_timer -= 1


player = Player()
