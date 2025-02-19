import json
from sys import exit

from button import *
from settings_menu_component import settings_menu

WIDTH = 910
HEIGHT = 558
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chicken Invasion')
bg_icon = pygame.image.load('Content/logo.png').convert()
pygame.display.set_icon(bg_icon)
fps = 60
playing = True
overlay = pygame.Surface((WIDTH, HEIGHT))
overlay.fill((0, 0, 0))
overlay.set_alpha(100)
bg_image = pygame.transform.scale(pygame.image.load('Content/background/background.png').convert_alpha(),(WIDTH, HEIGHT))
bg_music = pygame.mixer.Sound('Content/Music/backgroundMap.ogg')
bg_music.set_volume(0.2)
quit_music = pygame.mixer.Sound('Content/Music/Quit.ogg')


def read_settings():
    with open("settings.json", "r") as file:
        return json.load(file)
    
settings = read_settings()


class Continue_game(Button):
    def render_text(self):
        self.image.fill((0,0,0,0))
        if self.hover:
            text_surface = self.font.render(self.text, True, self.color if settings['continue'] == "True" else (70, 70, 70, 200))
            pygame.draw.rect(self.image, (20, 20, 20, 200), (0, 0, self.width + 50, self.height + 30), border_radius=20)
        else:
            text_surface = self.font.render(self.text, True,
                                            self.color if settings['continue'] == "True" else (70, 70, 70, 200))
            pygame.draw.rect(self.image, (0, 0, 0, 200), (0, 0, self.width, self.height), border_radius=20)
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
    pass


class New_game(Button):
    @staticmethod
    def new_game():
        # start new game
        pass


continue_button = Continue_game(WIDTH // 2, 100, 200, 60, (0, 0, 0, 100), (255, 255, 255), 'Continue')
new_game_button = New_game(WIDTH // 2, 200, 200, 60, (0, 0, 0, 100), (255, 255, 255), 'New game')
setting_button = Setting(WIDTH // 2, 300, 200, 60, (0, 0, 0, 100), (255, 255, 255), 'Settings')
quit_button = Quit(WIDTH // 2, 400, 200, 60, (0, 0, 0, 100), (255, 255, 255), 'Quit')
button_group = pygame.sprite.Group()
button_group.add(continue_button, new_game_button, setting_button, quit_button)

clock = pygame.time.Clock()
if bg_music.get_num_channels() == 0 and settings['sound music'] == "True":
    bg_music.play(-1)

while playing:
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
                settings_menu(screen, bg_image, bg_music)
    screen.blit(bg_image, (0, 0))
    screen.blit(overlay, (0, 0))
    button_group.update()
    button_group.draw(screen)
    pygame.display.update()
