import csv

import pygame

pygame.init()

from button import Button


def read_settings():
    with open("settings.csv", "r") as file:
        reader = csv.DictReader(file)
        return next(reader, {})  # Read first row or return empty dictionary


settings = read_settings()


class OnOffButton(Button):
    """Toggle button for sound/music settings"""

    def __init__(self, x, y, width, height, color, text, key):
        self.key = key
        self.value = settings.get(self.key, "True") == "True"
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
        self.value = not self.value
        settings[self.key] = str(self.value)
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
        bg_color = (20, 20, 20, 200) if self.hover else (50, 50, 50, 200) if int(
            settings[self.key]) == self.level else (0, 0, 0, 100)
        pygame.draw.rect(self.image, bg_color, (0, 0, self.width, self.height), border_radius=20)
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surface, text_rect)

    def select(self):
        settings[self.key] = str(self.level)
        for button in DifficultyButton.all_difficulty_buttons:
            button.render_text()


class SaveButton(Button):
    """Button to save settings to file"""

    @staticmethod
    def save():
        with open("settings.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(settings.keys())
            writer.writerow(settings.values())
        print("Settings saved!")


class BackButton(Button):
    """Button to return to main menu"""

    @staticmethod
    def back():
        from main_menu_component import menu
        menu()


def settings_menu(screen, text_font, bg_image):
    """Displays the settings menu using the shared screen and resources."""
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.set_alpha(100)
    overlay.fill((0, 0, 0))

    easy = DifficultyButton(510, 300, 120, 50, (255, 255, 255), "Easy", "difficulty", 1)
    normal = DifficultyButton(660, 300, 120, 50, (255, 255, 255), "Normal", "difficulty", 2)
    hard = DifficultyButton(810, 300, 120, 50, (255, 255, 255), "Hard", "difficulty", 3)

    sound_music_button = OnOffButton(810, 100, 100, 50, (255, 255, 255), "ON", "sound music")
    sound_effect_button = OnOffButton(810, 200, 100, 50, (255, 255, 255), "ON", "sound effect")

    save_button = SaveButton(300, 400, 100, 50, (0, 255, 0), (255, 255, 255), "Save")
    back_button = BackButton(100, 400, 100, 50, (0, 255, 0), (255, 255, 255), "Back")

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
                        elif isinstance(button, BackButton):
                            return  # Exit settings

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

    text_font = pygame.font.SysFont('comicsans', 30, bold=True)
    bg_image = pygame.transform.scale(
        pygame.image.load("Content/background/background.png").convert_alpha(),
        (WIDTH, HEIGHT)
    )
    while True:
        settings_menu(screen, text_font, bg_image)
