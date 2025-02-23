import json
from button import *
from player import Player
from wave_and_level import Level 
from init import *
from sprite_groups import (
    bullets_group,
    gifts_group,
    eggs_group,
    lvl_token_group,
    meat_group,
)
# Initialize game settings
def read_settings():
    """Reads the settings from the settings.json file."""
    with open("settings.json", "r") as file:
        return json.load(file)
settings = read_settings()
SOUND_EFFECT = settings["sound effects"]
SOUND_MUSIC = settings["sound music"]
# Initialize Pygame
WIDTH, HEIGHT = 910, 558
SHIP_SIZE = 50
SHIP_POS = [WIDTH / 2, HEIGHT - 20]
BULLET_COOLDOWN = 0.3
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Invasion")
score_font = pygame.font.Font("Content/7segment.ttf", 40)
bg_icon = pygame.image.load("Content/logo.png").convert()
pygame.display.set_icon(bg_icon)

bk_ground = pygame.image.load("Content/background/background.png").convert()
overlay = pygame.Surface((WIDTH, HEIGHT))
overlay.fill((0, 0, 0))
# Load assets
bg_ground = pygame.image.load("Content/background/background.png").convert()
health_icon = pygame.image.load("Content/background/heart.png").convert_alpha()
health_icon_scaled = pygame.transform.scale_by(health_icon, 0.1)

winner_music = pygame.mixer.Sound("Content/Music/Gamewin.ogg")

# Groups for game objects


class SaveGame(SaveButton):
    def render_text(self):
        self.image.fill((0, 0, 0, 0))  # Clear the surface
        if self.hover and level.change_save_button : 
            text_surface = self.font.render(self.text, True, self.color)
            pygame.draw.rect(self.image, (20, 20, 20, 200), (0, 0, self.width + 50, self.height + 30 ), border_radius=20)
        else:
            text_surface = self.font.render(self.text, True, self.color if level.change_save_button else (50,50,50,200))
            pygame.draw.rect(self.image, (0, 0, 0, 150) , (0, 0, self.width, self.height), border_radius=20)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surface, text_rect)
    def save(self):
        global settings
        with open("saved game.json", "w") as file:
            saved_game = {
                "current_level_parameter": level.current_level,
                "current_wave_parameter": level.current_wave_number,
                "bullet_level": player.sprite.bullet_lvl,
                "bullet_type": player.sprite.bull_type,
                "score": player.sprite.score,
                "health":player.sprite.health
            }
            json.dump(saved_game, file)
        level.change_save_button = False
        settings["continue"] = True
        with open("settings.json", "w") as file:
            json.dump(settings, file)
def play_fun(
    current_level_parameter=1,
    current_wave_parameter=1,
    bullet_level=1,
    bullet_type="a",
    score=0,
    health = 3
):
        """Main game loop."""
        global level, player, SOUND_EFFECT, SOUND_MUSIC, settings
        settings = read_settings()
        SOUND_EFFECT = settings["sound effects"]
        SOUND_MUSIC = settings["sound music"]
        level = Level(current_level_parameter, current_wave_parameter)
        player = pygame.sprite.GroupSingle(
            Player(bullet_level=bullet_level, bullet_type=bullet_type, score=score , health=health)
        )
        pause = False
        overlay_alpha = 0
        fade_speed = 8  # Speed of fade-in effect
        text_surface = text_font.render("Press 'ESC' to continue", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        save_button = SaveGame(
            WIDTH // 2,
            HEIGHT // 2 + 100,
            200,
            60,
            (0, 0, 0, 200),
            (255, 255, 255),
            "Save game",
        )
        back_button = Button(
            WIDTH // 2, HEIGHT - 100, 200, 60, (0, 0, 0, 200), (255, 255, 255), "Back"
        )
        button_group = pygame.sprite.Group()
        button_group.add(save_button)
        button_group.add(back_button)
        clock = pygame.time.Clock()
        pygame.time.delay(100)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:  # Pause the game by pressing ESC
                    if event.key == pygame.K_ESCAPE:
                        if not pause:
                            overlay_alpha = 0  # Reset alpha for smooth fade-in
                        pause = not pause
                if event.type == pygame.MOUSEBUTTONDOWN and pause:
                    mouse_pos = pygame.mouse.get_pos()
                    if back_button.rect.collidepoint(mouse_pos):
                        level.stop_music()
                        bullets_group.empty()
                        gifts_group.empty()
                        eggs_group.empty()
                        lvl_token_group.empty()
                        meat_group.empty()
                        return settings["continue"]  # Return to main menu

            # Screen
            screen.blit(bk_ground, (0, 0))
            if pause:
                # Gradually increase overlay opacity for fade-in effect
                if overlay_alpha < 180:
                    overlay_alpha += fade_speed
                    overlay_alpha = min(overlay_alpha, 180)  # Set to 180 at max
                pygame.mouse.set_visible(True)
                overlay.set_alpha(overlay_alpha)
                screen.blit(overlay, (0, 0))
                screen.blit(text_surface, text_rect)
                button_group.update( level.change_save_button , pause)
                button_group.draw(screen)
            elif level.game_finished:  # Check if the game has ended
                text = text_font.render("Winner", True, (255, 255, 255))
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(text, text_rect)
                if SOUND_MUSIC:
                    if winner_music.get_num_channels() == 0:
                        winner_music.play()  # Play the music
                pygame.display.update()
            elif not level.game_finished:  # Continue playing
                pygame.mouse.set_visible(False)
                # Update and draw game objects
                gifts_group.update()
                gifts_group.draw(screen)
                lvl_token_group.update()
                lvl_token_group.draw(screen)
                for i in range(player.sprite.health):
                    screen.blit(health_icon_scaled, (WIDTH - 45 * (i + 1), HEIGHT - 45))
                bullets_group.update()
                bullets_group.draw(screen)
                eggs_group.update()
                eggs_group.draw(screen)
                meat_group.update()
                meat_group.draw(screen)
                player.update(level.get_current_wave())
                player.draw(screen)
                level.update()

            clock.tick(60)
            pygame.display.update()
    


if __name__ == "__main__":
    play_fun()
