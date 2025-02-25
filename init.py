import pygame
from settings import Settings
pygame.init()
WIDTH = 910
HEIGHT = 558
fps = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Invasion")
bg_icon = pygame.image.load("Content/logo.png").convert()
pygame.display.set_icon(bg_icon)
bk_ground = pygame.image.load("Content/background/background.png").convert()
overlay = pygame.Surface((WIDTH, HEIGHT))
overlay.set_alpha(100)
overlay.fill((0, 0, 0))
fade_speed = 8  # Speed of fade-in effect
settings = Settings()