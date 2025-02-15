import pygame
from sys import exit
import csv
pygame.init()
WIDTH = 910
HEIGHT = 558
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Chicken Invasion')
text_font = pygame.font.SysFont('comicsans' , 30 , bold=True)
fps = 60
playing = True
overlay = pygame.Surface((WIDTH, HEIGHT),pygame.SRCALPHA)
from button import Button
bg_icon =pygame.image.load('./chicken-invasion-game/chicken-invasion-game/Assets/logo.png').convert_alpha()
bg_image =pygame.transform.scale(pygame.image.load('./chicken-invasion-game/chicken-invasion-game/Assets/background/background.png').convert_alpha(),(WIDTH,HEIGHT))
bg_music = pygame.mixer.Sound('./chicken-invasion-game/chicken-invasion-game/Assets/Music/backgroundMap.ogg')
quit_music = pygame.mixer.Sound('./chicken-invasion-game/chicken-invasion-game/Assets/Music/Quit.ogg')
pygame.display.set_icon(bg_icon)
change = False
def read_settings():
    with open("./chicken-invasion-game/chicken-invasion-game/settings.csv", "r") as file:
        global settings
        reader = csv.DictReader(file)
        for line in reader:
            settings = line
read_settings()
class On_Off(Button):
    def __init__(self, x, y, width, height, bg_color, color, text, key, value):
        self.value = True if value == 'True' else False
        self.key = key
        super().__init__(x, y, width, height, bg_color, color, text)
        self.render_text()
    def render_text(self):
        self.image.fill((0, 0, 0, 0))  # Clear the surface with transparency
        if self.hover:
            text_surface = self.font.render(self.text if self.value else "OFF", True, self.color)
            pygame.draw.rect(self.image, (0, 230, 0, 150) if self.value else (230, 0, 0, 150), (0, 0, self.width, self.height), border_radius=20)
        else:
            text_surface = self.font.render(self.text if self.value else "OFF", True, self.color)
            pygame.draw.rect(self.image, (0, 250, 0) if self.value else (255, 0, 0), (0, 0, self.width, self.height), border_radius=20)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surface, text_rect)
    def change_value(self):
        global change
        coordinates = pygame.mouse.get_pos()
        if self.rect.collidepoint(coordinates):
            change = True
            settings[self.key] = not self.value
            self.value = not self.value
            self.render_text()
    def update(self):
        self.animate()
        self.render_text()
class Difficulty(Button):
    def __init__(self, x , y , width , height , bg_color , color , text , key , value):
        self.level = value
        self.key = key
        super().__init__(x , y , width , height , bg_color , color , text)
    def render_text(self):
        self.image.fill((0, 0, 0, 0))  # Clear the surface
        if self.hover:
            text_surface = self.font.render(self.text, True, self.color)
            pygame.draw.rect(self.image, (20, 20, 20, 200), (0, 0, self.width, self.height), border_radius=20)
        else:
            text_surface = self.font.render(self.text, True, self.color)
            pygame.draw.rect(self.image,  (50, 50, 50, 200) if int(settings['difficulty']) == self.level else (0,0,0,100), (0, 0, self.width, self.height), border_radius=20)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surface, text_rect)
    def change_value(self):
        global change
        coordinates = pygame.mouse.get_pos()
        if self.rect.collidepoint(coordinates):
            change = True
            settings[self.key] = self.level
    def update(self):
        self.animate()
        self.render_text()
class Save(Button):
    def save_file(self):
        global change
        coordinates = pygame.mouse.get_pos()
        if self.rect.collidepoint(coordinates) and change:
            with open('./chicken-invasion-game/chicken-invasion-game/settings.csv', 'w') as file:
                writer  = csv.writer(file)
                print(settings)
                writer.writerow(settings.keys())
                writer.writerow(settings.values())
            change = False
            print('saved')
    def render_text(self):
        self.image.fill((0, 0, 0, 0))  # Clear the surface
        if self.hover and change : 
            text_surface = self.font.render(self.text, True, self.color)
            pygame.draw.rect(self.image, (20, 20, 20, 200), (0, 0, self.width + 50, self.height + 30 ), border_radius=20)
        else:
            text_surface = self.font.render(self.text, True, self.color if change else (50,50,50,200))
            pygame.draw.rect(self.image, (0, 0, 0, 150) , (0, 0, self.width, self.height), border_radius=20)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surface, text_rect)
class Back(Button):
    def back(self):
        coordinates = pygame.mouse.get_pos()
        if self.rect.collidepoint(coordinates):
            global page
            from main_menu_component import menu
            menu()
    def render_text(self):
        self.image.fill((0, 0, 0, 0))  # Clear the surface
        if self.hover : 
            text_surface = self.font.render(self.text, True, self.color)
            pygame.draw.rect(self.image, (20, 20, 20, 200), (0, 0, self.width + 50, self.height + 30 ), border_radius=20)
        else:
            text_surface = self.font.render(self.text, True, self.color)
            pygame.draw.rect(self.image, (0, 0, 0, 200) , (0, 0, self.width, self.height), border_radius=20)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surface, text_rect)
def settings_menu():
    easy = Difficulty(WIDTH - 400,300,120,50 , (0,255,0)  , (255,255,255) , "Easy" , "difficulty" , 1)
    normal = Difficulty(WIDTH - 250,300,120,50 , (0,255,0)  , (255,255,255) , "Normal" ,"difficulty" , 2)
    hard = Difficulty(WIDTH - 100,300,120,50 , (0,255,0)  , (255,255,255) , "Hard" , "difficulty" , 3)
    difficulty = text_font.render('difficulty' , 1 , 'white')
    sound_music = text_font.render('sound effect' , 1 , 'white')
    sound_effect = text_font.render('sound music' , 1 , 'white')
    save_button = Save(300, 400 , 100,50 , (0,255,0) , (255,255,255) , "Save")
    back_button = Back(100, 400 , 100,50 , (0,255,0) , (255,255,255) , "Back")
    sound_music_button = On_Off(WIDTH - 100, 100 , 100,50 , (0,255,0) , (255,255,255) , "ON" , "sound music" , settings["sound music"])
    sound_effect_button = On_Off(WIDTH - 100, 200 , 100,50 , (0,255,0) , (255,255,255) , "ON" , "sound effect" , settings["sound effect"])
    group_buttons = pygame.sprite.Group([sound_music_button , sound_effect_button , easy , normal , hard , save_button , back_button])
    overlay.set_alpha(100) 
    overlay.fill((0, 0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                    sound_music_button.change_value()
                    sound_effect_button.change_value()
                    easy.change_value()
                    normal.change_value()
                    hard.change_value()
                    save_button.save_file()
                    back_button.back()
        
        screen.blit(bg_image , (0,0))
        screen.blit(overlay , (0,0))
        group_buttons.update()
        screen.blit(sound_music , sound_music.get_rect(midleft=(50, 100)))
        screen.blit(sound_effect , sound_effect.get_rect(midleft=(50, 200)))
        screen.blit(difficulty , difficulty.get_rect(midleft=(50, 300)))
        group_buttons.draw(screen)
        pygame.display.update()        