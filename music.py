import pygame.mixer
pygame.init()
pygame.mixer.init()
# Загрузка звуков
shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')
step_sound = pygame.mixer.Sound('sounds/step.wav')
damage_sound = pygame.mixer.Sound('sounds/damage.mp3')
mage_shoot_sound = pygame.mixer.Sound('sounds/mage_shoot.mp3')
skeleton_attack_sound = pygame.mixer.Sound('sounds/skeleton_attack.mp3')
home_theme = pygame.mixer.Sound('sounds/home_theme.mp3')
end_screenF = pygame.mixer.Sound('sounds/Failure.mp3')
end_screenV = pygame.mixer.Sound('sounds/Victory.mp3')

# Настройка громкости звуков (по желанию)
shoot_sound.set_volume(0.2)  # От 0.0 до 1.0
step_sound.set_volume(0.3)
mage_shoot_sound.set_volume(0.1)
end_screenV.set_volume(0.5)
