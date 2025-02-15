import pygame
import csv
from sys import exit

pygame.init()

# Screen dimensions
WIDTH = 910
HEIGHT = 558
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chicken Invasion')

# Fonts
text_font = pygame.font.SysFont('comicsans', 30, bold=True)

# Game state variables
playing = True
fps = 60
overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Load assets
bg_icon = pygame.image.load('./chicken-invasion-game/chicken-invasion-game/Assets/logo.png').convert_alpha()
bg_image = pygame.transform.scale(pygame.image.load('./chicken-invasion-game/chicken-invasion-game/Assets/background/background.png').convert_alpha(), (WIDTH, HEIGHT))
bg_music = pygame.mixer.Sound('./chicken-invasion-game/chicken-invasion-game/Assets/Music/backgroundMap.ogg')
quit_music = pygame.mixer.Sound('./chicken-invasion-game/chicken-invasion-game/Assets/Music/Quit.ogg')

pygame.display.set_icon(bg_icon)

# Load settings
settings = None
change = False

def read_settings():
    global settings
    with open("./chicken-invasion-game/chicken-invasion-game/settings.csv", "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            settings = line

read_settings()

# Button class
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, bg_color, color, text):
        super().__init__()
        self.color = color
        self.bg_color = bg_color
        self.current_bg_color = self.bg_color
        self.font = text_font
        self.text = text
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.hover = False
        self.render_text()

    def render_text(self):
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        if self.hover:
            text_surface = self.font.render(self.text, True, (0, 0, 0))
            pygame.draw.rect(self.image, self.current_bg_color, (0, 0, self.width + 50, self.height + 30), border_radius=20)
        else:
            text_surface = self.font.render(self.text, True, self.color)
            pygame.draw.rect(self.image, self.current_bg_color, (0, 0, self.width, self.height), border_radius=20)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surface, text_rect)

    def animate(self):
        coordinates = pygame.mouse.get_pos()
        if self.rect.collidepoint(coordinates):
            self.hover = True
        else:
            self.hover = False
            self.current_bg_color = self.bg_color

    def update(self):
        self.animate()
        self.render_text()

# Main menu buttons
class ContinueGame(Button):
    @staticmethod
    def continue_game():
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

class NewGame(Button):
    @staticmethod
    def new_game():
        pass

def main_menu():
    continue_button = ContinueGame(WIDTH // 2, 100, 200, 60, (0, 0, 0, 100), (255, 255, 255), 'Continue')
    new_game_button = NewGame(WIDTH // 2, 200, 200, 60, (0, 0, 0, 100), (255, 255, 255), 'New game')
    setting_button = Setting(WIDTH // 2, 300, 200, 60, (0, 0, 0, 100), (255, 255, 255), 'Settings')
    quit_button = Quit(WIDTH // 2, 400, 200, 60, (0, 0, 0, 100), (255, 255, 255), 'Quit')

    button_group = pygame.sprite.Group([continue_button, new_game_button, setting_button, quit_button])

    global playing
    clock = pygame.time.Clock()

    while playing:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.rect.collidepoint(event.pos):
                    bg_music.stop()
                    quit_music.play()
                    pygame.time.delay(500)
                    quit_button.quit_game()
                elif setting_button.rect.collidepoint(event.pos):
                    setting_button.go_to_setting()

        bg_music.play()
        overlay.fill((0, 0, 0, 180))
        screen.blit(bg_image, (0, 0))
        screen.blit(overlay, (0, 0))
        button_group.update()
        button_group.draw(screen)
        pygame.display.update()

    pygame.quit()

# Settings Menu
def settings_menu():
    easy = Button(WIDTH - 400, 300, 120, 50, (0, 255, 0), (255, 255, 255), "Easy")
    normal = Button(WIDTH - 250, 300, 120, 50, (0, 255, 0), (255, 255, 255), "Normal")
    hard = Button(WIDTH - 100, 300, 120, 50, (0, 255, 0), (255, 255, 255), "Hard")

    difficulty_text = text_font.render('Difficulty', 1, 'white')
    sound_music_text = text_font.render('Sound Music', 1, 'white')
    sound_effect_text = text_font.render('Sound Effect', 1, 'white')

    save_button = Button(300, 400, 100, 50, (0, 255, 0), (0, 0, 0), (255, 255, 255), "Save")
    back_button = Button(100, 400, 100, 50, (0, 255, 0), (0, 0, 0), (255, 255, 255), "Back")

    buttons = pygame.sprite.Group([easy, normal, hard, save_button, back_button])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.rect.collidepoint(event.pos):
                    return  # Return to main menu

        screen.fill((24, 24, 14))
        buttons.update()
        screen.blit(sound_music_text, sound_music_text.get_rect(center=(100, 100)))
        screen.blit(sound_effect_text, sound_effect_text.get_rect(center=(100, 200)))
        screen.blit(difficulty_text, difficulty_text.get_rect(center=(100, 300)))
        buttons.draw(screen)
        pygame.display.update()

# Start the game
if __name__ == "__main__":
    main_menu()
