import json
from button import *


def read_settings():
    with open("settings.json", "r") as file:
        return json.load(file)
settings = read_settings()
change = False


class OnOffButton(Button):
    """Toggle button for sound/music settings"""

    def __init__(self, x, y, width, height, color, text, key):
        self.key = key
        self.value = settings[self.key]
        super().__init__(x, y, width, height, (0, 255, 0), color, text)
        self.render_text()

    def render_text(self):
        """Updates button appearance based on state."""
        self.image.fill((0, 0, 0, 0))
        bg_color = (0, 230, 0, 150) if self.value else (230, 0, 0, 150)
        pygame.draw.rect(self.image, bg_color, (0, 0, self.width, self.height), border_radius=20)
        text = self.text if self.value else "OFF"
        text_surface = self.font.render(text, True, self.color)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surface, text_rect)

    def toggle(self):
        global change
        change = True
        self.value = not self.value
        settings[self.key] = self.value
        self.render_text()


class DifficultyButton(Button):
    """Button to set game difficulty"""
    all_difficulty_buttons = []

    def __init__(self, x, y, width, height, color, text, key, level):
        self.key = key
        self.level = level
        super().__init__(x, y, width, height, (50, 50, 50, 200), color, text)
        DifficultyButton.all_difficulty_buttons.append(self)

    def render_text(self):
        self.image.fill((0, 0, 0, 0))
        bg_color = (20, 20, 20, 200) if self.hover and not int(
            settings[self.key]) == self.level else (50, 50, 50, 200) if int(
            settings[self.key]) == self.level else (0, 0, 0, 100)
        pygame.draw.rect(self.image, bg_color, (0, 0, self.width, self.height), border_radius=20)
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surface, text_rect)

    def select(self):
        global change
        change = True
        settings[self.key] = str(self.level)
        for button in DifficultyButton.all_difficulty_buttons:
            button.render_text()


class SaveButton(Button):
    """Button to save settings to file"""
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
    @staticmethod
    def save():
        global change
        with open("settings.json", "w") as file:
            change = False
            json.dump(settings, file)
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)

        # Only re-render if hover state changes
        if self.hover or change :
            self.render_text()


class BackButton(Button):
    pass


def settings_menu(screen, bg_image, bg_music):
    """Displays the settings menu using the shared screen and resources."""
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.set_alpha(100)
    overlay.fill((0, 0, 0))

    easy = DifficultyButton(510, 300, 120, 50, (255, 255, 255), "Easy", "difficulty", 1)
    normal = DifficultyButton(660, 300, 120, 50, (255, 255, 255), "Normal", "difficulty", 2)
    hard = DifficultyButton(810, 300, 120, 50, (255, 255, 255), "Hard", "difficulty", 3)

    sound_music_button = OnOffButton(810, 100, 100, 50, (255, 255, 255), "ON", "sound music")
    sound_effect_button = OnOffButton(810, 200, 100, 50, (255, 255, 255), "ON", "sound effects")

    save_button = SaveButton(810, 400, 100, 50, (0, 0, 0, 200), (255, 255, 255), "Save")
    back_button = BackButton(460, 558 - 85, 150, 75, (0, 0, 0, 200), (255, 255, 255), "Back")

    buttons = pygame.sprite.Group(
        [sound_music_button, sound_effect_button, easy, normal, hard, save_button, back_button])

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.rect.collidepoint(mouse_pos):
                        if isinstance(button, OnOffButton):
                            button.toggle()
                        elif isinstance(button, DifficultyButton):
                            button.select()
                        elif isinstance(button, SaveButton):
                            button.save()
                            if bg_music.get_num_channels() == 0 and settings['sound music']:
                                bg_music.play(-1)
                            elif not settings['sound music']:
                                bg_music.stop()
                        elif isinstance(button, BackButton):
                            return # return to main menu

        screen.blit(bg_image, (0, 0))
        screen.blit(overlay, (0, 0))

        labels = [("Sound Music", 50, 100), ("Sound Effect", 50, 200), ("Difficulty", 50, 300)]
        for text, x, y in labels:
            label = text_font.render(text, True, 'white')
            screen.blit(label, label.get_rect(midleft=(x, y)))

        buttons.update()
        buttons.draw(screen)
        pygame.display.update()


if __name__ == "__main__":
    WIDTH, HEIGHT = 910, 558
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Test Settings Menu")
    bg_music = pygame.mixer.Sound('Content/Music/backgroundMap.ogg')
    bg_music.set_volume(0.2)
    bg_image = pygame.transform.scale(
        pygame.image.load("Content/background/background.png").convert_alpha(),
        (WIDTH, HEIGHT)
    )
    settings_menu(screen, bg_image, bg_music)
