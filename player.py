import pygame
import math
import random
import time
from init import *
from sprite_groups import lvl_token_group , bullets_group , eggs_group ,meat_group , chicken_parachute_group , gifts_group
from enemies import Chicken , ChickenParachute , Boss
from drops import LvlUpToken , BulletChangeGift
SHIP_SIZE = 50
SHIP_POS = [WIDTH // 2, HEIGHT - 20]  # Starting position
BULLET_COOLDOWN = 0.3  # Cooldown between shots
bullet_sound = pygame.mixer.Sound("Content/Music/bullet/a.ogg")
lvl_up_sound = pygame.mixer.Sound("Content/Music/bullet/levelUp.ogg")
score_font = pygame.font.Font("Content/7segment.ttf", 40)
class Player(pygame.sprite.Sprite):
    """Player class representing the player's ship."""
    def __init__(self, bullet_level=1, bullet_type='a', score=0 , health = 3):
        super().__init__()
        self.angle = None
        self.score = score
        self.image = pygame.image.load("Content/ship.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (SHIP_SIZE, SHIP_SIZE))
        self.rect = self.image.get_rect(midbottom=(SHIP_POS[0], SHIP_POS[1]))
        self.last_shot_time = 0  # Store the last time a bullet was fired
        self.bullet_lvl = bullet_level
        self.bull_type = bullet_type
        self.bull_types = ["a", "b"]
        self.damage = 1
        self.mask = pygame.mask.from_surface(self.image)  # Creates a mask for precise collisions
        self.health = health
        self.lvl_token_count = 0
        self.gift_count = 0
        # Invincibility arguments
        self.invincible = False
        self.invincible_timer = 0
        self.invincibility_duration = 1000

    def player_move(self):
        """Moves the player based on mouse position."""
        mouse_pos = pygame.mouse.get_pos()
        pos_diff = [self.rect.centerx - mouse_pos[0], self.rect.centery - mouse_pos[1]]
        self.rect.x -= pos_diff[0] * 0.16
        self.rect.y -= pos_diff[1] * 0.16
        self.rect.x = max(20, min(self.rect.x, WIDTH - self.rect.width - 20))
        self.rect.y = max(20, min(self.rect.y, HEIGHT - self.rect.height - 20))
        # self.rect.right = min(self.rect.right, WIDTH - 10)
        # self.rect.bottom = min(self.rect.bottom, HEIGHT - 10)

    def take_damage(self):
        """Reduces player health and makes them invincible for a short time."""
        self.health -= 1
        self.invincible = True
        self.invincible_timer = pygame.time.get_ticks()
        print(f"Player hit! Health: {self.health}")

    def check_input(self, bullets_g):
        """Checks for player input (e.g., firing bullets)."""
        current_time = time.time()
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            if current_time - self.last_shot_time >= BULLET_COOLDOWN:
                self.fire_bullets(bullets_g)
                self.last_shot_time = current_time

    def fire_bullets(self, bullets_g):
        """Fires bullets based on the player's bullet level."""
        bull_lv = min(self.bullet_lvl, 20)
        bullet_size = (10 + bull_lv, 20 + bull_lv * 2) if bull_lv > 3 else (10, 20)
        if bull_lv == 1:
            bullets_g.add(Bullet(self))
        elif bull_lv == 2:
            bullets_g.add(Bullet(self, offset=-bullet_size[0] / 2))
            bullets_g.add(Bullet(self, offset=bullet_size[0] / 2))
        elif bull_lv == 3:
            bullets_g.add(
                Bullet(
                    self,
                    offset=-bullet_size[0],
                    push_back=bullet_size[1] / 2,
                    angle=-self.angle,
                )
            )
            bullets_g.add(Bullet(self))
            bullets_g.add(
                Bullet(
                    self,
                    offset=bullet_size[0],
                    push_back=bullet_size[1] / 2,
                    angle=self.angle,
                )
            )
        elif bull_lv == 4:
            bullets_g.add(
                Bullet(
                    self,
                    offset=-1.5 * bullet_size[0],
                    push_back=bullet_size[1] / 2,
                    angle=-self.angle,
                )
            )
            bullets_g.add(Bullet(self, offset=-bullet_size[0] / 2))
            bullets_g.add(Bullet(self, offset=bullet_size[0] / 2))
            bullets_g.add(
                Bullet(
                    self,
                    offset=1.5 * bullet_size[0],
                    push_back=bullet_size[1] / 2,
                    angle=self.angle,
                )
            )
        elif bull_lv >= 5:
            bullets_g.add(
                Bullet(
                    self,
                    offset=-2 * bullet_size[0],
                    push_back=bullet_size[1] / 2,
                    angle=-self.angle,
                )
            )
            bullets_g.add(
                Bullet(
                    self,
                    offset=-bullet_size[0],
                    push_back=bullet_size[1] / 4,
                    angle=-self.angle / 2,
                )
            )
            bullets_g.add(
                Bullet(
                    self,
                    offset=bullet_size[0],
                    push_back=bullet_size[1] / 4,
                    angle=self.angle / 2,
                )
            )
            bullets_g.add(
                Bullet(
                    self,
                    offset=2 * bullet_size[0],
                    push_back=bullet_size[1] / 2,
                    angle=self.angle,
                )
            )
            bullets_g.add(Bullet(self))
        try:
            if settings.sound_effects:
                bullet_sound.play()
        except pygame.error as e:
            print(f"Sound file error: {e}")

    def check_collisions(self, *sprite_groups):
        """Checks for collisions with various sprite groups."""
        for group in sprite_groups:
            rect_collide_list = pygame.sprite.spritecollide(self , group, False)
            if rect_collide_list:
                for sprite in rect_collide_list:
                    if pygame.sprite.collide_mask(self , sprite):
                        if group == lvl_token_group:
                            self.bullet_lvl += 1
                            sprite.kill()
                            try:
                                if settings.sound_effects:
                                    lvl_up_sound.play()
                            except pygame.error as e:
                                print(f"Sound file error: {e}")
                        elif group == gifts_group:
                            sprite.kill()
                            if self.bull_type == self.bull_types[sprite.type]:
                                self.bullet_lvl += 1
                                try:
                                    if settings.sound_effects:
                                        lvl_up_sound.play()
                                except pygame.error as e:
                                    print(f"Sound file error: {e}")
                            else:
                                self.bull_type = self.bull_types[sprite.type]
                                self.bullet_lvl = 1
                        elif group == meat_group:
                            sprite.kill()
                            if sprite.type == 0:
                                self.score += 10
                            elif sprite.type == 1:
                                self.score += 50
                        elif not self.invincible:
                            if group == eggs_group and not sprite.broken:
                                sprite.kill()
                                self.take_damage()
                            elif isinstance(sprite, ChickenParachute) or isinstance(
                                    sprite, Chicken
                            ) or isinstance(sprite, Boss):
                                self.take_damage()
                                sprite.health -= 2

    def draw_score(self):
        """Draws the player's score on the screen."""
        score_text = score_font.render(f"{self.score}", True, (255, 255, 0))
        score_rect = score_text.get_rect()
        score_rect.topright = (WIDTH, 0)
        screen.blit(score_text, score_rect)

    def drop_lvl_token(self):
        """Drops level-up tokens based on the player's score."""
        self.lvl_token_count += 1
        random_number = random.randint(0, 3)
        if not random_number:
            gifts_group.add(BulletChangeGift())
        elif random_number in range(1, 3):
            lvl_token_group.add(LvlUpToken())

    def update(self , groups):
        """Updates the player's state (e.g., movement, collisions)."""
        if self.bull_type == "b":
            self.angle = 20
        else:
            self.angle = 0
        self.player_move()
        self.check_input(bullets_group)
        self.check_collisions(
            lvl_token_group,
            gifts_group,
            eggs_group,
            chicken_parachute_group, meat_group,
            *[chicken.chicken_group if hasattr(chicken, 'chicken_group') else chicken.boss_group for chicken in
              groups],
        )
        if self.lvl_token_count < self.score // 100:
            self.drop_lvl_token()
        # Invincibility
        if self.invincible:
            elapsed_time = pygame.time.get_ticks() - self.invincible_timer
            if elapsed_time > self.invincibility_duration:
                self.invincible = False
            else:
                if (elapsed_time // 200) % 2 == 0:
                    self.image.set_alpha(128)
                else:
                    self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)
        self.draw_score()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player1: Player, offset=0.0, angle=0.0, push_back=0.0) -> None:
        super().__init__()
        self.image = pygame.image.load(f"Content/bullet/{player1.bull_type}1.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (10, 20))
        self.angle = angle if player1.bull_type == "b" else 0
        self.image = pygame.transform.rotate(self.image, -self.angle)
        self.rect = self.image.get_rect(midbottom=(player1.rect.centerx + offset, player1.rect.top + push_back))
        self.speed = 8
        self.damage = 1 + (player1.bullet_lvl - 1) * 0.1  # Set damage based on level

    def update(self):  # moves and dies
        self.rect.x += self.speed * math.sin(math.radians(self.angle))
        self.rect.y -= self.speed * math.cos(math.radians(self.angle))
        if self.rect.bottom < 0:  # Remove if off-screen
            self.kill()