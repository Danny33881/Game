import pygame.mixer
pygame.init()
pygame.mixer.init()
# Загрузка звуков
shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')
step_sound1 = pygame.mixer.Sound('sounds/step.wav')
step_sound2 = pygame.mixer.Sound('sounds/step2.mp3')
damage_sound = pygame.mixer.Sound('sounds/damage.mp3')
mage_shoot_sound = pygame.mixer.Sound('sounds/mage_shoot.mp3')
skeleton_attack_sound = pygame.mixer.Sound('sounds/skeleton_attack.mp3')
home_theme = pygame.mixer.Sound('sounds/home_theme.mp3')
end_screenF = pygame.mixer.Sound('sounds/Failure.mp3')
end_screenV = pygame.mixer.Sound('sounds/Victory.mp3')
goblin_attack_sound = pygame.mixer.Sound('sounds/goblin_attack.mp3')
enemy_death_sound = pygame.mixer.Sound('sounds/enemy_death.mp3')
level_up_sound = pygame.mixer.Sound('sounds/levelup.mp3')

# Настройка громкости звуков (по желанию)
shoot_sound.set_volume(0.1)  # От 0.0 до 1.0
step_sound1.set_volume(0.4)
mage_shoot_sound.set_volume(0.1)
end_screenV.set_volume(0.5)

