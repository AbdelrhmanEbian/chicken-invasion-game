import pygame
from main_menu_component import menu
from settings_menu_component import settings_menu
pygame.init()
WIDTH = 910
HEIGHT = 558
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Chicken Invasion')
text_font = pygame.font.SysFont('comicsans' , 30 , bold=True)
fps = 60
playing = True
overlay = pygame.Surface((WIDTH, HEIGHT) , pygame.SRCALPHA)
overlay.fill((0, 0, 0 , 180))
page = "main menu"
bg_icon =pygame.image.load('./chicken-invasion-game/chicken-invasion-game/Assets/logo.png').convert_alpha()
bg_image =pygame.transform.scale(pygame.image.load('./chicken-invasion-game/chicken-invasion-game/Assets/background/background.png').convert_alpha(),(WIDTH,HEIGHT))
bg_music = pygame.mixer.Sound('./chicken-invasion-game/chicken-invasion-game/Assets/Music/backgroundMap.ogg')
quit_music = pygame.mixer.Sound('./chicken-invasion-game/chicken-invasion-game/Assets/Music/Quit.ogg')
pygame.display.set_icon(bg_icon)
def main():
    if page == "main menu":
        menu()
    elif page == "settings":
        settings_menu()
while True:
    main()