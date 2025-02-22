import json
from sys import exit
from button import *
from settings_menu_component import settings_menu
WIDTH = 910
HEIGHT = 558
change = False
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Invasion")
bg_icon = pygame.image.load("Content/logo.png").convert()
pygame.display.set_icon(bg_icon)
fps = 60
playing = True
overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
overlay.set_alpha(100)
overlay.fill((0, 0, 0))
bg_image = pygame.transform.scale(
    pygame.image.load("Content/background/background.png").convert_alpha(),
    (WIDTH, HEIGHT),
)
bg_music = pygame.mixer.Sound("Content/Music/backgroundMap.ogg")
bg_music.set_volume(0.2)
quit_music = pygame.mixer.Sound("Content/Music/Quit.ogg")
def read_settings():
    with open("settings.json", "r") as file:
        return json.load(file)
settings = read_settings()
class ContinueGame(Button):
    def render_text(self):
        self.image.fill((0, 0, 0, 0))
        if self.hover:
            text_surface = self.font.render(
                self.text,
                True,
                self.color if settings["continue"] else (70, 70, 70, 200),
            )
            pygame.draw.rect(
                self.image,
                (20, 20, 20, 200),
                (0, 0, self.width + 50, self.height + 30),
                border_radius=20,
            )
        else:
            text_surface = self.font.render(
                self.text,
                True,
                self.color if settings["continue"] else (70, 70, 70, 200),
            )
            pygame.draw.rect(
                self.image,
                (0, 0, 0, 200),
                (0, 0, self.width, self.height),
                border_radius=20,
            )
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surface, text_rect)

    @staticmethod
    def continue_game():
        # call play function
        last_game = {}
        with open("saved game.json", "r") as file:  # read last game
            last_game = json.load(file)
        from play import play_fun

        return_value = play_fun(**last_game , screen=screen , bg_image=bg_image)
        global change
        if not settings["continue"] == return_value:
            settings["continue"] = return_value
            change = True
        print(settings["continue"])

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)

        # Only re-render if hover state changes
        if self.hover or change:
            self.render_text()


class Quit(Button):
    @staticmethod
    def quit_game():
        global playing
        playing = False
        pygame.quit()
        exit()


class Setting(Button):
    pass


class NewGame(Button):
    @staticmethod
    def new_game():
        with open("saved game.json", "w") as file:
            default_game = {
                "current level": 1,
                "current wave": 1,
                "bullet level": 1,
                "bullet type": "a",
            }
            json.dump(default_game, file)
        global settings
        settings["continue"] = False
        with open("settings.json", "w") as file:
            json.dump(settings, file)
        from play import play_fun

        return_value = play_fun(screen=screen , bg_image=bg_image)
        global change
        if not settings["continue"] == return_value:
            settings["continue"] = return_value
            change = True
        print(settings["continue"])


continue_button = ContinueGame(
    WIDTH // 2, 100, 200, 60, (0, 0, 0, 200), (255, 255, 255), "Continue"
)
new_game_button = NewGame(
    WIDTH // 2, 200, 200, 60, (0, 0, 0, 200), (255, 255, 255), "New game"
)
setting_button = Setting(
    WIDTH // 2, 300, 200, 60, (0, 0, 0, 200), (255, 255, 255), "Settings"
)
quit_button = Quit(WIDTH // 2, 400, 200, 60, (0, 0, 0, 200), (255, 255, 255), "Quit")
button_group = pygame.sprite.Group()
button_group.add(continue_button, new_game_button, setting_button, quit_button)
clock = pygame.time.Clock()
if bg_music.get_num_channels() == 0 and settings["sound music"]:
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
            elif setting_button.rect.collidepoint(event.pos):
                settings_menu(screen, bg_image, bg_music)
            elif new_game_button.rect.collidepoint(event.pos):
                new_game_button.new_game()
            elif continue_button.rect.collidepoint(event.pos):
                continue_button.continue_game()
    screen.blit(bg_image, (0, 0))
    screen.blit(overlay, (0, 0))
    button_group.update()
    button_group.draw(screen)
    pygame.display.update()
