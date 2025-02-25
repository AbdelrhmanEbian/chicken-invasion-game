from button import *
from sprite_groups import (bullets_group, gifts_group, eggs_group, lvl_token_group, meat_group , chicken_parachute_group)
from wave_and_level import Level
# Load assets
health_icon = pygame.image.load("Content/background/heart.png").convert_alpha()
health_icon_scaled = pygame.transform.scale_by(health_icon, 0.1)
winner_music = pygame.mixer.Sound("Content/Music/Gamewin.ogg")
game_over_music = pygame.mixer.Sound("Content/Music/Gameover.ogg")
# Groups for game objects
def play_fun(current_level_parameter=1, current_wave_parameter=1, bullet_level=1, bullet_type="a", score=0, health=3):
    """Main game loop."""
    global level
    level = Level(current_level_parameter, current_wave_parameter)
    level.generate_player(bullet_level, bullet_type, score, health)
    overlay_alpha = 0
    text_surface = text_font.render("Press 'ESC' to continue", True, (255, 255, 255))
    text_rect = text_surface.get_rect(midbottom=(WIDTH // 2, HEIGHT // 2 - 100))
    back_button = Button(WIDTH // 2, HEIGHT - 100, 200, 60, (0, 0, 0, 200), (255, 255, 255), "Back")
    button_group = pygame.sprite.GroupSingle()
    button_group.add(back_button)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:  # Pause the game by pressing ESC
                if event.key == pygame.K_ESCAPE:
                    if not settings.is_game_pause:
                        overlay_alpha = 0  # Reset alpha for smooth fade-in
                    if not settings.game_finished:
                        settings.is_game_pause = not settings.is_game_pause
                if event.key == pygame.K_F6:
                    level.player.sprite.drop_lvl_token()
            if event.type == pygame.MOUSEBUTTONDOWN and settings.is_game_pause:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.rect.collidepoint(mouse_pos):
                    level.stop_music()
                    bullets_group.empty()
                    gifts_group.empty()
                    eggs_group.empty()
                    lvl_token_group.empty()
                    meat_group.empty()
                    pygame.mixer.stop()
                    return settings.continue_game  # Return to main menu
        # Screen
        screen.blit(bk_ground, (0, 0))
        if settings.game_finished:  # Check if the game has ended
            if settings.is_winner:
                if overlay_alpha < 180:
                    overlay_alpha += fade_speed
                    overlay_alpha = min(overlay_alpha, 180)  # Set to 180 at max
                pygame.mouse.set_visible(True)
                overlay.set_alpha(overlay_alpha)
                screen.blit(overlay, (0, 0))
                text = text_font.render("Win", True, (255, 255, 255))
                text_rect = text.get_rect(midbottom=(WIDTH // 2, HEIGHT // 2))
                screen.blit(text, text_rect)
                button_group.update()
                button_group.draw(screen)
                if settings.sound_music:
                    if winner_music.get_num_channels() == 0:
                        winner_music.play()  # Play the music
                pygame.display.update()
            else:
                if overlay_alpha < 180:
                    overlay_alpha += fade_speed
                    overlay_alpha = min(overlay_alpha, 180)  # Set to 180 at max
                pygame.mouse.set_visible(True)
                overlay.set_alpha(overlay_alpha)
                screen.blit(overlay, (0, 0))
                text = text_font.render("Game Over", True, (255, 255, 255))
                text_rect = text.get_rect(midbottom=(WIDTH // 2, HEIGHT // 2))
                screen.blit(text, text_rect)
                screen.blit(text, text_rect)
                button_group.update()
                button_group.draw(screen)
                if settings.sound_music:
                    if game_over_music.get_num_channels() == 0:
                        game_over_music.play()  # Play the music
                pygame.display.update()
        elif not settings.game_finished and not settings.is_game_pause:  # Continue playing
            pygame.mouse.set_visible(False)
            # Update and draw game objects
            gifts_group.update()
            gifts_group.draw(screen)
            lvl_token_group.update()
            lvl_token_group.draw(screen)
            for i in range(level.player.sprite.health):
                screen.blit(health_icon_scaled, (WIDTH - 45 * (i + 1), HEIGHT - 45))
            bullets_group.update()
            bullets_group.draw(screen)
            eggs_group.update()
            eggs_group.draw(screen)
            meat_group.update()
            meat_group.draw(screen)
            level.player.update(level.get_current_wave())
            level.player.draw(screen)
            chicken_parachute_group.update()
            chicken_parachute_group.draw(screen)
            level.update()
        elif settings.is_game_pause:
            # Gradually increase overlay opacity for fade-in effect
            if overlay_alpha < 180:
                overlay_alpha += fade_speed
                overlay_alpha = min(overlay_alpha, 180)  # Set to 180 at max
            pygame.mouse.set_visible(True)
            overlay.set_alpha(overlay_alpha)
            screen.blit(overlay, (0, 0))
            screen.blit(text_surface, text_rect)
            button_group.update()
            button_group.draw(screen)
        clock.tick(fps)
        pygame.display.update()
if __name__ == "__main__":
    play_fun()
