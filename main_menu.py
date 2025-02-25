import json
from sys import exit
from button import *
from settings_menu import settings_menu
playing = True
bg_music = pygame.mixer.Sound("Content/Music/backgroundMap.ogg")
bg_music.set_volume(0.5)
quit_music = pygame.mixer.Sound("Content/Music/Quit.ogg")
class ContinueGame(ControlButton):
    def __init__(self , x, y, width, height, bg_color, color, text):
        self.active = settings.continue_game
        super().__init__(x = x, y = y ,width=width , height=height , bg_color=bg_color , color=color , text=text)
    def control(self):
        if not settings.continue_game:
            return
        # call play function
        last_game = {}
        with open("saved game.json", "r") as file:  # read last game
            last_game = json.load(file)
        from play_test import play_fun
        bg_music.stop()
        settings.is_game_pause = False
        return_value = play_fun(**last_game)
        bg_music.play()
        if not (settings.continue_game == return_value):
            settings.continue_game = return_value
        self.is_changed = True
        settings.read_settings()
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
                "health":3
            }
            json.dump(default_game, file)
        settings.continue_game = False
        with open("settings.json", "w") as file:
            settings_dic = settings.__dict__.copy()
            del settings_dic['is_game_pause'] , settings_dic['game_finished'] , settings_dic['is_winner']
            json.dump(settings_dic, file)
        from play_test import play_fun
        bg_music.stop()
        settings.is_game_pause = False
        settings.game_finished = False
        return_value = play_fun()
        bg_music.play()
        if not settings.continue_game == return_value:
            settings.continue_game = return_value
        ControlButton.control_buttons[1].is_changed  = True
        settings.read_settings()

continue_button = ContinueGame(
    WIDTH // 2, 100, 200, 60, (0, 0, 0, 200), (255, 255, 255), "Continue"
)
new_game_button = NewGame(
    WIDTH // 2, 200, 200, 60, (0, 0, 0, 200), (255, 255, 255), "New game"
)
setting_button = Setting(
    WIDTH // 2, 300, 200, 60, (0, 0, 0, 200), (255, 255, 255), "Settings"
)
ControlButton.control_buttons [1] = continue_button
quit_button = Quit(WIDTH // 2, 400, 200, 60, (0, 0, 0, 200), (255, 255, 255), "Quit")
button_group = pygame.sprite.Group()
button_group.add(continue_button, new_game_button, setting_button, quit_button)
clock = pygame.time.Clock()
if bg_music.get_num_channels() == 0 and settings.sound_music:
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
                settings_menu(screen, bk_ground, bg_music)
            elif new_game_button.rect.collidepoint(event.pos):
                new_game_button.new_game()
    screen.blit(bk_ground, (0, 0))
    screen.blit(overlay, (0, 0))
    button_group.update()
    button_group.draw(screen)
    pygame.display.update()