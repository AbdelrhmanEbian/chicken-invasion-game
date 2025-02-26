import math
import random

from drops import Drops, Meat, Egg
from init import *
from sprite_groups import bullets_group, eggs_group, meat_group
from utils import extract_frames

chicken_die_sounds = list(
    [
        pygame.mixer.Sound(f"Content/Music/chicken/Chicken_death{i}.ogg")
        for i in range(1, 5)
    ]
)

laser_sound = pygame.mixer.Sound(
    "Content/Music/bullet/laser-shot-ingame-230500.mp3")
parachute_red = pygame.image.load(
    "Content/Enemy/chickenParachuteRed.png"
).convert_alpha()
parachute_red = pygame.transform.scale_by(parachute_red, 0.5)
parachute_blue = pygame.image.load(
    "Content/Enemy/chickenParachuteBlue.png"
).convert_alpha()
parachute_blue = pygame.transform.scale_by(parachute_blue, 0.5)
chicken_boss_sheet = pygame.image.load("Content/Enemy/boss.png").convert_alpha()
chicken_boss_animation_list = extract_frames(chicken_boss_sheet, 1, 10, (100, 100))
chicken_bossRed_sheet = pygame.image.load("Content/Enemy/bossRed.png").convert_alpha()
chicken_bossRed_animation_list = extract_frames(
    chicken_bossRed_sheet, 1, 10, (100, 100)
)


class Enemy(Drops):
    def check_collision(self):
        """Checks for collisions with bullets."""
        collisions_with_bullets = pygame.sprite.spritecollide(
            self, bullets_group, False
        )
        for bullet in collisions_with_bullets:
            if self.health <= 0:
                self.kill()
                loop_index = 1
                chicken_width = self.rect.width
                distance = chicken_width
                if isinstance(self, Boss):
                    loop_index = 3
                    distance = chicken_width // 2
                for i in range(loop_index):
                    pos_x = self.rect.left + (i * distance)
                    pos_y = self.rect.bottom
                    meat_drop_random_number = random.randint(0, 100)
                    if meat_drop_random_number <= 50:
                        meat_group.add(Meat(0, (pos_x, pos_y)))
                    elif meat_drop_random_number in range(51, 76):
                        meat_group.add(Meat(1, (pos_x, pos_y)))
                if settings.sound_effects:
                    random.choice(chicken_die_sounds).play()
            else:
                self.health -= bullet.damage
                bullet.kill()


class Chicken(Enemy):
    """Base class for chicken enemies."""

    def __init__(self, image, animation_list=None, x=None, y=None):
        super().__init__(image=image, animation_list=animation_list)
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 5 * (1 + 0.5 * (int(settings.difficulty) - 1))

    def animate(self):
        """Animates the chicken."""
        if (
                math.ceil(self.frame_index) >= self.frames_count
                or math.floor(self.frame_index) < 0
        ):
            self.frame_speed *= -1
        self.frame_index += self.frame_speed
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        """Updates the chicken's state (e.g., collisions, animation)."""
        self.check_collision()
        if random.randint(0, 1000) == 5:
            eggs_group.add(Egg(self.rect.midbottom))
        self.animate()


class ChickenParachute(Enemy):
    """Chicken enemy with a parachute."""

    def __init__(self):
        self.type = random.choice(["parachuted_red", "parachuted_blue"])
        image = None
        if self.type == "parachuted_red":
            image = parachute_red
        elif self.type == "parachuted_blue":
            image = parachute_blue
        super().__init__(image=image)
        self.gravity = 1
        self.health = 5 * (1 + 0.5 * (int(settings.difficulty) - 1))

    def update(self):
        """Updates the parachute chicken's state (e.g., collisions, egg drops)."""
        self.drops()
        self.check_collision()
        if random.randint(0, 200) == 155:
            pos = self.rect.midbottom
            eggs_group.add(Egg(pos))


class Boss(Enemy):
    """Boss enemy class."""

    def __init__(self, type, x, y, hidden, initial_x, initial_y):
        self.type = type
        self.is_move_randomly = False
        if self.type == "boss":
            super().__init__(animation_list=chicken_boss_animation_list)
            self.health = 200 * (1 + 0.5 * (int(settings.difficulty) - 1))
        elif self.type == "boss_red":
            super().__init__(animation_list=chicken_bossRed_animation_list)
            self.health = 150 * (1 + 0.5 * (int(settings.difficulty) - 1))
        self.rect = self.image.get_rect(midbottom=(initial_x, initial_y))
        self.last_move_time = pygame.time.get_ticks()
        self.move_interval = 3000
        self.ability_to_move = False
        self.chicken_group = pygame.sprite.GroupSingle(self)
        self.destination_x = 0
        self.destination_y = 0
        self.speed_x = 0
        self.speed_y = 0
        self.frame_speed = 0.2
        self.hidden = hidden
        self.x = x
        self.y = y

    def check_ability_to_move(self):
        current_time = pygame.time.get_ticks()
        if self.last_move_time + self.move_interval <= current_time and not self.is_move_randomly:
            self.is_move_randomly = True
            self.destination_x = random.randint(30, WIDTH - 30)
            self.destination_y = random.randint(30, HEIGHT - 30)

    def update(self):
        """Updates the boss's state (e.g., collisions, movement, attacks)."""
        if self.hidden == "right" and self.rect.centerx > self.x and not self.ability_to_move:
            self.rect.x -= 1
        elif self.hidden == "left" and self.rect.centerx < self.x and not self.ability_to_move:
            self.rect.x += 1
        elif self.hidden == "down" and self.rect.bottom > self.y and not self.ability_to_move:
            self.rect.y -= 1
        elif self.hidden == "up" and self.rect.bottom < self.y and not self.ability_to_move:
            self.rect.y += 1
        else:
            if not self.ability_to_move:
                self.last_move_time = pygame.time.get_ticks()
            self.ability_to_move = True
        self.check_collision()
        if self.ability_to_move:
            self.check_ability_to_move()
        if self.is_move_randomly:
            self.move_randomly()
        if self.type == "boss_red":
            if (
                    math.ceil(self.frame_index) >= self.frames_count
                    or math.floor(self.frame_index) < 0
            ):
                self.frame_speed *= -1
        self.animate()
        self.attack()

    def move_randomly(self):
        """Moves the boss randomly."""
        speed_x = (self.rect.centerx - self.destination_x) * 0.03
        speed_y = (self.rect.centery - self.destination_y) * 0.03
        self.rect.centerx -= speed_x
        self.rect.centery -= speed_y
        if self.speed_x == speed_x and self.speed_y == speed_y:
            self.is_move_randomly = False
            self.last_move_time = pygame.time.get_ticks()
        self.speed_x = speed_x
        self.speed_y = speed_y

    def attack(self):
        """Spawns eggs as an attack."""
        if HEIGHT - 20 > self.rect.bottom > 0:
            if self.type == "boss_red":
                distance = self.rect.width // 2
                if random.randint(0, 100) == 99:
                    for i in range(3):
                        pos_x = self.rect.left + (i * distance) + 5
                        pos_y = self.rect.bottom
                        egg = Egg((pos_x, pos_y))
                        eggs_group.add(egg)
            else:  # Laser attack for the ufo boss
                current_time = pygame.time.get_ticks()

                if not hasattr(self, 'last_attack_time'):
                    self.last_attack_time = current_time  # Initialize attack timer
                    self.attacking = False
                    self.last_shot_time = 0  # Track last laser shot

                if not self.attacking and current_time - self.last_attack_time >= 1000:  # Cooldown for 1 second
                    self.attacking = True
                    self.last_attack_time = current_time  # Reset timer

                if self.attacking and current_time - self.last_attack_time < 1000:  # Attack for 1 second
                    if current_time - self.last_shot_time >= 300:  # Fire every 300ms
                        self.last_shot_time = current_time  # Reset shot timer
                        if settings.sound_effects:
                            laser_sound.play()
                        laser = Laser(self, offset=0, angle=0)  # Shoots straight down
                        eggs_group.add(laser)
                        laser = Laser(self, offset=20, angle=30)  # Shoots straight down
                        eggs_group.add(laser)
                        laser = Laser(self, offset=-20, angle=-30)  # Shoots straight down
                        eggs_group.add(laser)

                if current_time - self.last_attack_time >= 1000:  # Stop attacking after 1 second
                    self.attacking = False
                    self.last_attack_time = current_time  # Reset cooldown timer


class Laser(pygame.sprite.Sprite):
    def __init__(self, boss: Boss, offset=0.0, angle=0.0, push_back=0.0) -> None:
        super().__init__()
        self.image = pygame.image.load(f"Content/bullet/laser_ball.png").convert_alpha()
        self.angle = angle
        self.image = pygame.transform.rotate(self.image, -self.angle)
        self.rect = self.image.get_rect(midbottom=(boss.rect.centerx + offset, boss.rect.bottom + push_back))
        self.speed = 8
        self.broken = False

    def update(self):  # moves and dies
        self.rect.x += self.speed * math.sin(math.radians(self.angle))
        self.rect.y += self.speed * math.cos(math.radians(self.angle))
        if self.rect.top > HEIGHT:  # Remove if off-screen
            self.kill()
