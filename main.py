import pygame.time

import all_sprites_group
import player
from enemy import *
from player import *
from random import randint
from HUD import *

pygame.init()
pygame.display.set_caption('Just Shoot')
clock = pygame.time.Clock()

all_sprites_group.add(player)

text_color = (255, 0, 0)
image_end = pygame.image.load('sprites/backgrounds/gameover.png')
image_win = pygame.image.load('sprites/backgrounds/win_background.png')
image_start = pygame.image.load('sprites/backgrounds/Just_shoot_start.png')
image_start_button = pygame.image.load('sprites/backgrounds/start_button.png')
image_quit_button = pygame.image.load('sprites/backgrounds/quit_button.png')


def enemy_outside_camera(randomx, randomy):
    return not(camera.offset.x <= randomx <= camera.offset.x + WIDTH and
               camera.offset.y <= randomy <= camera.offset.y + HEIGHT)


def random_pos():
    return randint(0, WIDTH * 2), randint(0, HEIGHT * 2)


def enemy_spawn(spawn_speed, wave, call_count):
    if wave == 1:
        spawn_speed += 0.5
    elif wave == 2:
        spawn_speed += 2
    elif wave == 3:
        spawn_speed += 15
    if spawn_speed > 200:
        randomx, randomy = random_pos()
        if enemy_outside_camera(randomx, randomy):
            Enemy((randomx, randomy))
        spawn_speed = 0
    if call_count % 200 == 0:
        randomx, randomy = random_pos()
        if enemy_outside_camera(randomx, randomy):
            Mage((randomx, randomy))
    if call_count % 200 == 0 and wave == 2:
        randomx, randomy = random_pos()
        if enemy_outside_camera(randomx, randomy):
            Skeleton((randomx, randomy))
    return spawn_speed


def display_text(text, resize, x, y):
    font_recreated = pygame.font.Font("font/PublicPixel.ttf", resize)
    text_surface = font_recreated.render(text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


def reset_all():
    background.get_texture_desert()
    player.player_reset()
    enemy_reset()
    bullet_reset()
    loot_reset()


def game():
    reset_all()
    call_count = 1
    spawn_speed = 40

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

        if player.player_data['get_hurt_count'] == player.player_data['health_amount']:
            return "game_end"

        if call_count == 1500:
            player.player_data['wave'] += 1
            call_count = 0

        if player.player_data['wave'] == 4:
            return 'game_end'

        screen.fill((0, 0, 0))
        camera.custom_draw()
        spawn_speed = enemy_spawn(spawn_speed, player.player_data['wave'], call_count)
        call_count += 1
        all_sprites_group.update()

        pygame.display.update()
        clock.tick(FPS)


def game_start():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

        screen.blit(image_start, (0, 0))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if 440 <= mouse_x <= 820 and 280 <= mouse_y <= 420:
            screen.blit(image_start_button, (449, 284))
            if pygame.mouse.get_pressed()[0] == 1:
                return "game"
        elif 480 <= mouse_x <= 820 and 455 <= mouse_y <= 600:
            screen.blit(image_quit_button, (465, 456))
            if pygame.mouse.get_pressed()[0] == 1:
                exit()

        pygame.display.update()
        clock.tick(FPS)


def game_end():
    win_flag = player.player_data['wave'] == 4
    if win_flag:
        image = image_win
    else:
        image = image_end

    score = player.player_data['score']
    player.player_data['record'] = get_record('read')
    if score > player.player_data['record']:
        get_record('write', score)
        player.player_data['record'] = score

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1 and 330 <= mouse_x <= 640 and 600 <= mouse_y <= 690:
            player.player_reset()
            return "game"
        elif pygame.mouse.get_pressed()[0] == 1 and 720 <= mouse_x <= 990 and 580 <= mouse_y <= 700:
            player.player_reset()
            return "game_start"

        screen.blit(image, (0, 0))
        display_text(str(player.player_data['score']), 32, 580, 305)
        display_text(str(player.player_data['enemy_killed']), 32, 580, 425)
        display_text(str(player.player_data['record']), 32, 580, 525)
        pygame.display.update()
        clock.tick(FPS)


current_screen = "game_start"
while True:
    if current_screen == "game_start":
        current_screen = game_start()
    elif current_screen == "game":
        current_screen = game()
    elif current_screen == "game_end":
        current_screen = game_end()
