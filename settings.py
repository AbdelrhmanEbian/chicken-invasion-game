import json


class Settings:
    def __init__(self):
        self.continue_game = None
        self.difficulty = None
        self.sound_music = None
        self.sound_effects = None
        self.is_game_pause = True
        self.game_finished = False
        self.is_winner = False
        self.read_settings()

    def read_settings(self):
        with open("settings.json", "r") as file:
            data = json.load(file)
            self.continue_game = data['continue_game']
            self.difficulty = data['difficulty']
            self.sound_music = data['sound_music']
            self.sound_effects = data['sound_effects']
