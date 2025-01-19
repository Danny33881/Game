import pygame.sprite
import pygame.font
from player import player
from setting import *

pygame.font.init()
text_group = pygame.sprite.Group()
font = pygame.font.Font("font/PublicPixel.ttf", 15)
hud_group = pygame.sprite.Group()


class HUD(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.HUD_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA).convert_alpha()
        self.health_full_image = pygame.image.load('sprites/player/health_full.png')
        self.health_empty_image = pygame.image.load('sprites/player/health_empty.png')
        self.health_rect = self.health_full_image.get_rect()

    def health_draw(self):
        self.HUD_surface.blit(self.health_empty_image, (10, HEIGHT - self.health_rect.height - 50))
        repeat = 3 - player.player_data['get_hurt_count']
        for i in range(repeat):
            sprite_rect = pygame.Rect(i * 43, 0, 43, 37)
            one_heart_image = self.health_full_image.subsurface(sprite_rect)
            self.HUD_surface.blit(one_heart_image, (10 + i * 43, HEIGHT - self.health_rect.height - 50))

    def text_draw(self):
        text_image_score = font.render('score:' + str(player.player_data['score']), True, game_settings['WHITE'])
        text_image_wave = font.render('wave:' + str(player.player_data['wave']), True, game_settings['WHITE'])
        self.HUD_surface.blit(text_image_score, (10, 30))
        self.HUD_surface.blit(text_image_wave, (10, 60))

    def update(self):
        self.HUD_surface.fill((0, 0, 0, 0))
        self.health_draw()
        self.text_draw()


HUD_main = HUD()
