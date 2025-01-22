import pygame.time
import pygame.mixer
import all_sprites_group
import player
from enemy import *
from player import *
from random import randint
from HUD import *

pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Just Shoot')
clock = pygame.time.Clock()

# Добавляем игрока в группу всех спрайтов
all_sprites_group.add(player)

# Цвет текста для интерфейса
text_color = (255, 0, 0)

# Изображения фонов для различных экранов (начало игры, конец игры, победа)
image_end = pygame.image.load('sprites/backgrounds/gameover.png')
image_win = pygame.image.load('sprites/backgrounds/win_background.png')
image_start = pygame.image.load('sprites/backgrounds/Just_shoot_start.png')
image_start_button = pygame.image.load('sprites/backgrounds/start_button.png')
image_quit_button = pygame.image.load('sprites/backgrounds/quit_button.png')

# Функция для проверки, находится ли враг за пределами камеры
def enemy_outside_camera(randomx, randomy):
    return not(camera.offset.x <= randomx <= camera.offset.x + WIDTH and
               camera.offset.y <= randomy <= camera.offset.y + HEIGHT)

# Функция для генерации случайных позиций на карте
def random_pos():
    return randint(0, WIDTH * 2), randint(0, HEIGHT * 2)

# Функция для спауна врагов
def enemy_spawn(spawn_speed, wave, call_count):
    """
    Функция для спавна врагов в зависимости от волны.
    В каждой волне скорость спауна врагов увеличивается.
    """
    # Изменение скорости спауна в зависимости от текущей волны
    if wave == 1:
        spawn_speed += 0.5
    elif wave == 2:
        spawn_speed += 2
    elif wave == 3:
        spawn_speed += 15
    if spawn_speed > 200:
        # Спавн Гоблинов в случайной позиции
        randomx, randomy = random_pos()
        if enemy_outside_camera(randomx, randomy):
            Goblin((randomx, randomy))
        spawn_speed = 0
    if call_count % 200 == 0:
        # Спавн Магов через каждые 200 кадров
        randomx, randomy = random_pos()
        if enemy_outside_camera(randomx, randomy):
            Mage((randomx, randomy))
    if call_count % 200 == 0 and wave >= 2:
        # Спавн Скелетов после волны 2 через каждые 200 кадров
        randomx, randomy = random_pos()
        if enemy_outside_camera(randomx, randomy):
            Skeleton((randomx, randomy))
    return spawn_speed

# Функция для отображения текста на экране
def display_text(text, resize, x, y):
    """
    Отображает текст на экране в заданном месте.
    text: текст для отображения
    resize: размер шрифта
    x, y: координаты центра текста
    """
    font_recreated = pygame.font.Font("font/PublicPixel.ttf", resize)
    text_surface = font_recreated.render(text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Функция для сброса всех игровых данных
def reset_all():
    """
    Сбрасывает все игровые данные: фон, игрока, врагов, пули, добычу.
    """
    background.get_texture_desert()
    player.player_reset()
    enemy_reset()
    bullet_reset()
    loot_reset()

# Основная игровая логика
def game():
    home_theme.stop()  # Останавливаем музыку для домашнего экрана
    reset_all()  # Сбрасываем данные
    call_count = 1  # Счётчик кадров
    spawn_speed = 40  # Начальная скорость спауна

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

        # Если здоровье игрока исчерпано, конец игры
        if player.player_data['get_hurt_count'] == player.player_data['health_amount']:
            return "game_end"

        # Переход на следующую волну через определённое количество кадров
        if call_count == 1500 and player.player_data['wave'] == 1:
            player.player_data['wave'] += 1
            call_count = 0
        if call_count == 2000 and player.player_data['wave'] == 2:
            player.player_data['wave'] += 1
            call_count = 0
        if call_count == 3000 and player.player_data['wave'] == 3:
            player.player_data['wave'] += 1
            call_count = 0

        # Если волна 4, то конец игры
        if player.player_data['wave'] == 4:
            return 'game_end'

        screen.fill((0, 0, 0))  # Очистка экрана
        camera.custom_draw()  # Отображение камеры
        spawn_speed = enemy_spawn(spawn_speed, player.player_data['wave'], call_count)  # Спавн врагов
        call_count += 1
        all_sprites_group.update()  # Обновление всех спрайтов

        pygame.display.update()
        clock.tick(FPS)  # Ожидание следующего кадра

# Экран старта игры
def game_start():
    """
    Отображает экран старта игры, где можно начать игру или выйти.
    """
    end_screenV.stop()
    end_screenF.stop()
    home_theme.play()  # Играет музыка на экране старта
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

        screen.blit(image_start, (0, 0))  # Отображаем стартовый фон

        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Кнопка старта
        if 440 <= mouse_x <= 820 and 280 <= mouse_y <= 420:
            screen.blit(image_start_button, (449, 284))
            if pygame.mouse.get_pressed()[0] == 1:
                return "game"
        # Кнопка выхода
        elif 480 <= mouse_x <= 820 and 455 <= mouse_y <= 600:
            screen.blit(image_quit_button, (465, 456))
            if pygame.mouse.get_pressed()[0] == 1:
                exit()

        pygame.display.update()
        clock.tick(FPS)

# Экран конца игры
def game_end():
    """
    Отображает экран конца игры. В зависимости от результата (победа/поражение) отображает соответствующий фон.
    """
    win_flag = player.player_data['wave'] == 4  # Проверка, выиграл ли игрок
    if win_flag:
        image = image_win  # Победный экран
        end_screenV.play()
    else:
        image = image_end  # Экран поражения
        end_screenF.play()

    score = player.player_data['score']  # Счёт игрока
    player.player_data['record'] = get_record('read')  # Получаем лучший рекорд
    if score > player.player_data['record']:
        get_record('write', score)  # Записываем новый рекорд
        player.player_data['record'] = score

    while True:
        #выход из игры
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Кнопка для перезапуска игры
        if pygame.mouse.get_pressed()[0] == 1 and 330 <= mouse_x <= 640 and 600 <= mouse_y <= 690:
            player.player_reset()
            return "game"
        # Кнопка для возврата на главный экран
        elif pygame.mouse.get_pressed()[0] == 1 and 720 <= mouse_x <= 990 and 580 <= mouse_y <= 700:
            player.player_reset()
            return "game_start"

        screen.blit(image, (0, 0))  # Отображаем фон конца игры
        display_text(str(player.player_data['score']), 32, 580, 305)  # Отображаем счёт
        display_text(str(player.player_data['enemy_killed']), 32, 580, 425)  # Количество убитых врагов
        display_text(str(player.player_data['record']), 32, 580, 525)  # Лучший рекорд
        pygame.display.update()
        clock.tick(FPS)

# Основной игровой цикл
current_screen = "game_start"
while True:
    if current_screen == "game_start":
        current_screen = game_start()
    elif current_screen == "game":
        current_screen = game()
    elif current_screen == "game_end":
        current_screen = game_end()
