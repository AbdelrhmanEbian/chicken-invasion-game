import pygame
from sys import exit
import csv
pygame.init()
WIDTH = 910
HEIGHT = 558
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Chicken Invasion')
fps = 60
playing = True
overlay = pygame.Surface((WIDTH, HEIGHT),pygame.SRCALPHA)
overlay.set_alpha(100)
overlay.fill((0, 0, 0))
from button import Button
from settings_menu_component import settings_menu
bg_icon =pygame.image.load('./chicken-invasion-game/chicken-invasion-game/Assets/logo.png').convert()
bg_image =pygame.transform.scale(pygame.image.load('./chicken-invasion-game/chicken-invasion-game/Assets/background/background.png').convert_alpha(),(WIDTH,HEIGHT))
bg_music = pygame.mixer.Sound('./chicken-invasion-game/chicken-invasion-game/Assets/Music/backgroundMap.ogg')
quit_music = pygame.mixer.Sound('./chicken-invasion-game/chicken-invasion-game/Assets/Music/Quit.ogg')
pygame.display.set_icon(bg_icon)
def read_settings():
    with open("./chicken-invasion-game/chicken-invasion-game/settings.csv", "r") as file:
        global settings
        reader = csv.DictReader(file)
        for line in reader:
            settings = line
read_settings()
class Continue_game(Button):
    def render_text(self):
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        if self.hover : 
            text_surface = self.font.render(self.text, True, self.color if settings['continue'] == "True" else (70,70,70,200))
            pygame.draw.rect(self.image, (20, 20, 20, 200) , (0, 0, self.width + 50, self.height + 30 ), border_radius=20)
        else:
            text_surface = self.font.render(self.text, True, self.color if settings['continue'] == "True" else (70,70,70,200))
            pygame.draw.rect(self.image, (0,0,0,200), (0, 0, self.width, self.height), border_radius=20)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surface, text_rect)
    @staticmethod
    def continue_game():
        # call play function
        pass 
class Quit(Button):
    @staticmethod
    def quit_game():
        global playing
        playing = False
        pygame.quit()
        exit()
class Setting(Button):
    @staticmethod
    def go_to_setting():
        settings_menu()
class New_game(Button):
    @staticmethod
    def new_game():
        # start new game
        pass
def menu():
    continue_button = Continue_game(WIDTH // 2, 100, 200, 60, (0,0,0,100), (255, 255, 255), 'Continue')
    new_game_button = New_game(WIDTH // 2, 200, 200, 60, (0,0,0,100), (255, 255, 255), 'New game')
    setting_button = Setting(WIDTH // 2, 300, 200, 60, (0,0,0,100), (255, 255, 255), 'Settings')
    quit_button = Quit(WIDTH // 2, 400, 200, 60, (0,0,0,100), (255, 255, 255), 'Quit')
    button_group = pygame.sprite.Group()
    button_group.add(continue_button,new_game_button,setting_button,quit_button)
    global playing
    clock = pygame.time.Clock()
    bg_music.play(-1)
    while playing :
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.rect.collidepoint(event.pos):
                    bg_music.stop()
                    quit_music.play()
                    pygame.time.delay(500)
                    quit_button.quit_game()
                if setting_button.rect.collidepoint(event.pos):
                    setting_button.go_to_setting()
        screen.blit(bg_image , (0,0))
        screen.blit(overlay , (0,0))
        button_group.update()
        button_group.draw(screen)
        pygame.display.update()
menu()