import pygame
import json
from init import *
from enemy_groups import ChickenGroup, BossGroup
from button import text_font
from utils import read_settings
SOUND_MUSIC = read_settings()['sound music']
class Wave(pygame.sprite.Sprite):
    """Represents a wave of enemies."""
    def __init__(self, level, wave):
        super().__init__()
        self.current_level = level
        self.current_wave_number = wave
        self.data = {}
        self.read_wave_data()
        self.wave_type = self.data["wave type"]
        self.number_of_groups = len(self.data["waves"])
        self.waves = self.data["waves"]
        self.groups = []
        if self.wave_type == 'normal':
            self.total_chickens = sum(
                [group["number of chicken"] for group in self.data["waves"]])
            self.generate_groups__of_chickens()
        elif self.wave_type == 'boss':
            self.generate_boss_group()
        self.wave_ended = False

    def read_wave_data(self):
        """Reads wave data from the JSON file."""
        with open(
                f"levels_data/level_{self.current_level}_data/waves/wave_{self.current_wave_number}_data.json",
                "r",
        ) as file:
            data = json.load(file)
            self.data = data

    def generate_groups__of_chickens(self):
        """Generates groups of chickens for the wave."""
        chicken_wave = [
            ChickenGroup(
                x=group["final x"],
                y=group["final y"],
                chicken_type=group["type"],
                number_of_chickens=group["number of chicken"],
                chicken_per_row=group["number of chicken per row"],
                initial_x=group["initial x"],
                initial_y=group["initial y"],
                group_order=index,
                hidden=group["hidden"],
                number_of_parachute_chickens=group["number of parachute chickens"],
            )
            for index, group in enumerate(self.waves)
        ]
        self.groups = chicken_wave

    def generate_boss_group(self):
        """Generates a boss group for the wave."""
        boss_wave = BossGroup(self.waves)
        self.groups = [boss_wave]

    def get_groups(self):
        """Returns the groups of enemies in the wave."""
        return self.groups

    def draw_level_and_wave(self):
        """Displays a message when a wave is completed."""
        text = text_font.render(
            f"you have finished level {self.current_level} wave {self.current_wave_number}",
            True,
            (255, 255, 255),
        )
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    def update(self):
        """Updates the wave's state (e.g., enemy movement, collisions)."""
        if len(self.groups) == 0:
            self.wave_ended = True
            return
        if self.wave_type == 'normal':
            move_randomly = [chicken_group.drop for chicken_group in self.groups]
            for chicken_group in self.groups:
                chicken_group.update(False if False in move_randomly else True , self.groups)
        elif self.wave_type == 'boss':
            for boss_group in self.groups:
                boss_group.update(self.groups)


class Level:
    """Represents a level in the game."""
    def __init__(self, level: int, wave: int):
        self.current_level = level
        self.data = {}
        self.current_wave_number = wave
        current_wave = self.generate_wave()
        self.current_wave = current_wave
        self.level_ended = False
        self.read_level_data()
        self.chicken_per_wave = self.data["number of chickens in each wave"]
        self.number_of_waves = self.data["number of waves"]
        self.music_played = False
        self.change_save_button = False
        self.game_finished = False
        self.change_wave_and_level  = False

    def generate_wave(self):
        """Generates a wave for the level."""
        wave = Wave(self.current_level, self.current_wave_number)
        return wave

    def read_level_data(self):
        """Reads level data from the JSON file."""
        with open(
                f"levels_data/level_{self.current_level}_data/level_data.json", "r"
        ) as file:
            data = json.load(file)
            self.data = data

    def get_current_wave(self):
        """Returns the current wave."""
        return self.current_wave.get_groups()
    def stop_music(self):
        if self.music_played:
            self.music.stop()
    def update(self):
        """Updates the level's state (e.g., wave progression)."""
        if self.current_wave.wave_ended:
            if not hasattr(self, "wave_end_time"):
                self.wave_end_time = pygame.time.get_ticks()
                self.music = pygame.mixer.Sound("Content/Music/Gamewin.ogg")
                if SOUND_MUSIC :
                    self.music.play()
                    self.music_played = True
            if not self.change_wave_and_level:
                if self.current_wave_number == self.number_of_waves :
                    if self.current_level == 2:
                        self.game_finished = True
                        return
                    self.current_level += 1
                    self.current_wave_number = 1
                    self.level_ended = True
                else:
                    self.current_wave_number += 1
            self.change_wave_and_level = True
            self.change_save_button = True
            elapsed_time = pygame.time.get_ticks() - self.wave_end_time
            if elapsed_time >= 3000:
                self.music.stop()
                if self.level_ended:
                    self.read_level_data()
                del self.current_wave
                self.current_wave = self.generate_wave()
                del self.wave_end_time
                self.music_played = False
                self.change_wave_and_level = False
            else:
                self.current_wave.draw_level_and_wave()
        else:
            self.current_wave.update()