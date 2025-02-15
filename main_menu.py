import pygame
pygame.init()
from main_menu_component import main_menu_fun
from settings_menu_component import settings_menu
WIDTH = 910
HEIGHT = 558
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Chicken Invasion')
text_font = pygame.font.SysFont('comicsans' , 30 , bold=True)
fps = 60
playing = True
overlay = pygame.Surface((WIDTH, HEIGHT))
overlay.fill((0, 0, 0))
page = "main menu"
bg_icon =pygame.image.load('./chicken-invasion-game/chicken-invasion-game/Assets/logo.png').convert_alpha()
bg_image =pygame.transform.scale(pygame.image.load('./chicken-invasion-game/chicken-invasion-game/Assets/background/background.png').convert_alpha(),(WIDTH,HEIGHT))
bg_music = pygame.mixer.Sound('./chicken-invasion-game/chicken-invasion-game/Assets/Music/backgroundMap.ogg')
quit_music = pygame.mixer.Sound('./chicken-invasion-game/chicken-invasion-game/Assets/Music/Quit.ogg')
pygame.display.set_icon(bg_icon)

class Button(pygame.sprite.Sprite):
    def __init__(self , x , y , width , height , bg_color , color , text):
        super().__init__()
        self.color = color
        self.bg_color = bg_color
        self.current_bg_color = self.bg_color
        self.font = text_font
        self.text = text
        self.width = width
        self.height = height
        self.image = pygame.Surface((width , height),pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x,y))
        self.hover = False
        self.render_text()
    def render_text(self):
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        if self.hover : 
            text_surface = self.font.render(self.text, True, (0,0,0))
            pygame.draw.rect(self.image, self.current_bg_color, (0, 0, self.width + 50, self.height + 30 ), border_radius=20)
        else:
            text_surface = self.font.render(self.text, True, self.color)
            pygame.draw.rect(self.image, (0,0,0,200), (0, 0, self.width, self.height), border_radius=20)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surface, text_rect)
    def animate(self):
        coordinates = pygame.mouse.get_pos()
        if self.rect.collidepoint(coordinates):
            self.hover = True
            self.current_bg_color = self.hover_bg_color
        else:
            self.hover = False
            self.current_bg_color = self.bg_color
    def update(self):
        self.animate()
        self.render_text()
def main():
    if page == "main menu":
        main_menu_fun()
    else:
        settings_menu()
main()