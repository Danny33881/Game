import csv

# Создаем словарь для хранения данных
game_settings = {}

# Читаем данные из CSV файла
with open('game_settings.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        # Преобразуем значение в соответствующий тип данных (например, int, tuple)
        key, value = row[0], eval(row[1])
        game_settings[key] = value

WIDTH = game_settings['WIDTH']
HEIGHT = game_settings['HEIGHT']
FPS = game_settings['FPS']
