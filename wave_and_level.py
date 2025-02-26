import json
import random

from button import text_font
from enemies import ChickenParachute
from enemy_groups import ChickenGroup
from init import *
from player import Player
from sprite_groups import chicken_parachute_group


class Wave():
    """Represents a wave of enemies."""

    def __init__(self, level, wave):
        super().__init__()
        self.current_level = level
        self.current_wave_number = wave
        self.data = {}
        self.read_wave_data()
        self.number_of_groups = len(self.data["waves"])
        self.waves = self.data["waves"]
        self.groups = []
        self.generate_groups__of_chickens()
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
        for group in self.waves:
            self.groups.append(
                ChickenGroup(
                    x=group["final x"],
                    y=group["final y"],
                    chicken_type=group["type"],
                    number_of_chickens=group["number of chicken"] if "number of chicken" in group else None,
                    chicken_per_row=group[
                        "number of chicken per row"] if "number of chicken per row" in group else None,
                    initial_x=group["initial x"],
                    initial_y=group["initial y"],
                    hidden=group["hidden"],
                    move_randomly=group["move randomly"] if "move randomly" in group else None,
                ))

    def get_groups(self):
        """Returns the groups of enemies in the wave."""
        return self.groups

    def draw_level_and_wave(self):
        """Displays a message when a wave is completed."""
        text = text_font.render(f"you have finished level {self.current_level}", True, (255, 255, 255), )
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    def update(self):
        """Updates the wave's state (e.g., enemy movement, collisions)."""
        if len(self.groups) == 0:
            self.wave_ended = True
            return
        for group in self.groups:
            group.update(self.groups)


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
        self.number_of_waves = self.data["number of waves"]
        self.music_played = False
        self.music = self.music = pygame.mixer.Sound("Content/Music/Gamewin.ogg")
        self.change_wave_and_level = False
        self.is_generate_chicken_parachute = True
        self.player = None
        self.number_of_levels = level_number
        self.game_ended = False

    def generate_chicken_parachute(self, rate=180):
        if self.is_generate_chicken_parachute:
            if not random.randint(0, rate):
                parachute_chicken = ChickenParachute()
                chicken_parachute_group.add(parachute_chicken)

    def generate_wave(self):
        """Generates a wave for the level."""
        wave = Wave(self.current_level, self.current_wave_number)
        return wave

    def read_level_data(self):
        """Reads level data from the JSON file."""
        with open(f"levels_data/level_{self.current_level}_data/level_data.json", "r") as file:
            data = json.load(file)
            self.data = data
            self.number_of_waves = data["number of waves"]

    def get_current_wave(self):
        """Returns the current wave."""
        return self.current_wave.get_groups()

    def stop_music(self):
        if self.music_played:
            self.music.stop()

    def save_game(self):
        settings.continue_game = True
        if settings.game_finished:
            settings.continue_game = False
            self.current_level = 1
            self.current_wave_number = 1
            self.player.sprite.bullet_lvl = 1
            self.player.sprite.bull_type = 'a'
            self.player.sprite.score = 0
            self.player.sprite.health = 3
        with open("saved game.json", "w") as file:
            saved_game = {
                "current_level_parameter": self.current_level,
                "current_wave_parameter": self.current_wave_number,
                "bullet_level": self.player.sprite.bullet_lvl,
                "bullet_type": self.player.sprite.bull_type,
                "score": self.player.sprite.score,
                "health": self.player.sprite.health
            }
            json.dump(saved_game, file)
        settings_dic = settings.__dict__.copy()
        del settings_dic['is_game_pause'], settings_dic['game_finished'], settings_dic['is_winner']
        with open("settings.json", "w") as file:
            json.dump(settings_dic, file)

    def generate_player(self, bullet_level, bullet_type, score, health):
        """Generates a player for the level."""
        player = pygame.sprite.GroupSingle(
            Player(bullet_level=bullet_level, bullet_type=bullet_type, score=score, health=health)
        )
        self.player = player

    def update(self):
        """Updates the level's state (e.g., wave progression)."""
        if self.current_wave.wave_ended and len(chicken_parachute_group) == 0:
            self.is_generate_chicken_parachute = False
            if not hasattr(self, "wave_end_time"):
                self.wave_end_time = pygame.time.get_ticks()
                if settings.sound_music:
                    self.music.play()
                    self.music_played = True
            elapsed_time = pygame.time.get_ticks() - self.wave_end_time
            if not self.change_wave_and_level or self.game_ended:
                if self.current_wave_number == self.number_of_waves:
                    if self.current_level == self.number_of_levels:
                        if self.game_ended and elapsed_time >= 3000:
                            settings.game_finished = True
                            settings.is_game_pause = True
                            self.music.stop()
                            self.save_game()
                        settings.is_winner = True
                        self.game_ended = True
                        self.current_wave.draw_level_and_wave()
                        return
                    self.current_level += 1
                    self.current_wave_number = 1
                    self.level_ended = True
                    self.player.sprite.level_transition = True
                else:
                    self.current_wave_number += 1
                self.save_game()
            self.change_wave_and_level = True
            if not self.player.sprite.level_transition:
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
            self.is_generate_chicken_parachute = False if self.current_wave.wave_ended else True
            if int(settings.difficulty) > 1:
                self.generate_chicken_parachute(180 * (2 if settings.difficulty == '3' else 1))
            self.current_wave.update()
