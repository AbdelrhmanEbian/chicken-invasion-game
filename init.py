import pygame
pygame.init()
WIDTH = 910
HEIGHT = 558
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Invasion")
bg_icon = pygame.image.load("Content/logo.png").convert()
pygame.display.set_icon(bg_icon)