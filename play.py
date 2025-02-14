import math
import time  # Used for cooldown timer
from random import randint

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.angle = None
        self.image = pygame.image.load("Content/ship.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (SHIP_SIZE, SHIP_SIZE))
        self.rect = self.image.get_rect(midbottom=(SHIP_POS[0], SHIP_POS[1]))
        self.last_shot_time = 0  # Store the last time a bullet was fired
        self.bullet_lvl = 1
        self.bull_type = 'a'
        self.bull_types = ['a', 'b']
        self.damage = 0.5 + 0.5 * self.bullet_lvl
        self.mask = pygame.mask.from_surface(self.image)  # creates a mask for precise collisions

    def player_move(self):
        mouse_pos = pygame.mouse.get_pos()
        pos_diff = [self.rect.centerx - mouse_pos[0], self.rect.centery - mouse_pos[1]]
        self.rect.x -= pos_diff[0] * 0.16
        self.rect.y -= pos_diff[1] * 0.16
        self.rect.right = min(self.rect.right, WIDTH)
        self.rect.bottom = min(self.rect.bottom, HEIGHT - 10)

    def check_input(self, bullets_g):
        current_time = time.time()  # Get current time in seconds
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            if current_time - self.last_shot_time >= BULLET_COOLDOWN:  # Check cooldown
                self.fire_bullets(bullets_g)
                self.last_shot_time = current_time  # Update last shot time

    def fire_bullets(self, bullets_g):
        bull_lv = min(self.bullet_lvl, 20)
        bullet_size = (10 + bull_lv, 20 + bull_lv * 2) if bull_lv > 3 else (10, 20)
        if bull_lv == 1:
            bullets_g.add(Bullet(self))
        elif bull_lv == 2:
            bullets_g.add(Bullet(self, offset=-bullet_size[0] / 2))
            bullets_g.add(Bullet(self, offset=bullet_size[0] / 2))
        elif bull_lv == 3:
            bullets_g.add(Bullet(self, offset=-bullet_size[0], push_back=bullet_size[1] / 2, angle=-self.angle))
            bullets_g.add(Bullet(self))
            bullets_g.add(Bullet(self, offset=bullet_size[0], push_back=bullet_size[1] / 2, angle=self.angle))
        elif bull_lv == 4:
            bullets_g.add(Bullet(self, offset=-1.5 * bullet_size[0], push_back=bullet_size[1] / 2, angle=-self.angle))
            bullets_g.add(Bullet(self, offset=- bullet_size[0] / 2))
            bullets_g.add(Bullet(self, offset=bullet_size[0] / 2))
            bullets_g.add(Bullet(self, offset=1.5 * bullet_size[0], push_back=bullet_size[1] / 2, angle=self.angle))
        elif bull_lv >= 5:
            bullets_g.add(Bullet(self, offset=-2 * bullet_size[0], push_back=bullet_size[1] / 2, angle=-self.angle))
            bullets_g.add(Bullet(self, offset=-bullet_size[0], push_back=bullet_size[1] / 4, angle=-self.angle / 2))
            bullets_g.add(Bullet(self, offset=bullet_size[0], push_back=bullet_size[1] / 4, angle=self.angle / 2))
            bullets_g.add(Bullet(self, offset=2 * bullet_size[0], push_back=bullet_size[1] / 2, angle=self.angle))
            bullets_g.add(Bullet(self))

    def check_collisions(self, *sprite_groups) -> None:  # more efficient way to check for collisions
        for group in sprite_groups:
            rect_collide_list = pygame.sprite.spritecollide(player.sprite, group, False)
            if rect_collide_list:
                for sprite in rect_collide_list:
                    if pygame.sprite.collide_mask(player.sprite, sprite):
                        if group == lvl_token_group:
                            self.bullet_lvl += 1
                            sprite.kill()
                        elif group == gifts_group:
                            sprite.kill()
                            if self.bull_type == self.bull_types[sprite.type]:
                                self.bullet_lvl += 1
                            else:
                                self.bull_type = self.bull_types[sprite.type]
                                self.bullet_lvl = 1

    def update(self):
        if self.bull_type == 'b':
            self.angle = 20
        else:
            self.angle = 0
        self.player_move()
        self.check_input(bullets_group)
        self.check_collisions(lvl_token_group, gifts_group)


class Bullet(pygame.sprite.Sprite):  # todo: bullet damage
    def __init__(self, player1: Player, offset=0.0, angle=0.0, push_back=0.0):
        super().__init__()
        self.image = pygame.image.load(f"Content/bullet/{player1.bull_type}1.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (10, 20))
        self.angle = angle if player1.bull_type == 'b' else 0
        self.image = pygame.transform.rotate(self.image, -self.angle)
        self.rect = self.image.get_rect(midbottom=(player1.rect.centerx + offset, player1.rect.top + push_back))
        self.speed = 8
        try:
            pygame.mixer.Sound("Content/Music/bullet/a.ogg").play()
        except pygame.error as e:
            print(f"Sound file error: {e}")

    def update(self):  # moves and dies
        self.rect.x += self.speed * math.sin(math.radians(self.angle))
        self.rect.y -= self.speed * math.cos(math.radians(self.angle))
        if self.rect.bottom < 0:  # Remove if off-screen
            self.kill()


class Drops(pygame.sprite.Sprite):
    def __init__(self, animation_list):
        super().__init__()
        self.gravity = 1.8
        self.frames = animation_list
        self.frames_count = len(self.frames)
        self.frame_index = 0
        self.frame_rate = 100
        self.frame_speed = 0.2
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(
            midbottom=(randint(0, WIDTH - self.image.get_width()), 0))  # todo make it spawns in random x-axis

    def drops(self) -> None:
        self.rect.y += self.gravity
        if self.rect.y > HEIGHT:
            self.kill()

    def animate(self) -> None:
        self.frame_index += self.frame_speed
        if self.frame_index >= self.frames_count:
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]


class LvlUpToken(Drops):
    def __init__(self):
        super().__init__(lvl_up_animation_list)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self) -> None:
        self.drops()
        self.animate()


class BulletChangeGift(Drops):  # todo
    def __init__(self):
        self.type = randint(0, 1)
        super().__init__(bullet_change_animation_lists[self.type])
        self.frames = bullet_change_animation_lists[self.type]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self) -> None:
        self.drops()
        self.animate()
        screen.blit(self.mask.to_surface(), (self.rect.x, self.rect.y))


class Enemies(pygame.sprite.Sprite):  # todo
    def __init__(self):
        super().__init__()


class RedChicken(Enemies):  # todo
    def __init__(self):
        super().__init__()


def extract_frames(spritesheet, sheet_width, sheet_height, rows: int, cols: int) -> tuple:
    sprite_width, sprite_height = sheet_width / cols, sheet_height / rows
    return tuple(
        spritesheet.subsurface(pygame.Rect(col * sprite_width, row * sprite_height, sprite_width, sprite_height))
        for col in range(cols) for row in range(rows)
    )


WIDTH, HEIGHT = 910, 558  # Screen dimensions
SHIP_SIZE = 50
SHIP_POS = [WIDTH / 2, HEIGHT - 20]  # Starting position
BULLET_COOLDOWN = 0.3  # Cooldown between shots

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Invasion: Deluxe Edition")

# loading up animations
lvl_up_token_sheet = pygame.image.load("Content/bullet/give.png").convert_alpha()
lvl_up_animation_list = extract_frames(lvl_up_token_sheet, 1100, 37, 1, 25)
bullet_change_animation_sheet_list = []
bullet_change_animation_lists = []
for index in range(2):
    bullet_change_animation_sheet_list.append(
        pygame.transform.smoothscale(pygame.image.load(f"Content/bullet/gift{index}_spritesheet.png").convert_alpha(),
                                     (512, 306)))
    bullet_change_animation_lists.append(extract_frames(bullet_change_animation_sheet_list[index], 512, 306, 5, 10))

# overlay
overlay = pygame.Surface((WIDTH, HEIGHT))
overlay.fill((0, 0, 0))

# Set up font
pygame.font.init()
font = pygame.font.Font(None, 50)

# Create text surface
text_surface = font.render("Press 'P' to continue", True, (255, 255, 255))
text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

clock = pygame.time.Clock()
bk_ground = pygame.image.load("Content/background/background.png").convert()
bk_ground_scaled = pygame.transform.smoothscale(bk_ground, (WIDTH, HEIGHT))

# Groups
player = pygame.sprite.GroupSingle(Player())
bullets_group = pygame.sprite.Group()
lvl_token_group = pygame.sprite.Group()
gifts_group = pygame.sprite.Group()

pause = False
overlay_alpha = 0
fade_speed = 10  # Speed of fade-in effect

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:  # to pause the game by pressing p
            if event.key == pygame.K_p:
                if not pause:
                    overlay_alpha = 0  # Reset alpha for smooth fade-in
                pause = not pause

    # Screen
    screen.blit(bk_ground_scaled, (0, 0))
    if pause:
        # Gradually increase overlay opacity for fade-in effect

        if overlay_alpha < 180:
            overlay_alpha += fade_speed
            overlay_alpha = min(overlay_alpha, 180)  # set to 180 at max
        pygame.mouse.set_visible(True)
        overlay.set_alpha(overlay_alpha)
        screen.blit(overlay, (0, 0))
        screen.blit(text_surface, text_rect)
    else:  # continue playing + anything we want to disappear upon pausing
        pygame.mouse.set_visible(False)
        # spawns tokens and gifts randomly todo: make it depends on smth
        if not randint(0, 180):
            lvl_token_group.add(LvlUpToken())
            gifts_group.add(BulletChangeGift())
        # Gifts update
        gifts_group.update()
        gifts_group.draw(screen)
        # lvl_token update
        lvl_token_group.update()
        lvl_token_group.draw(screen)
        # Player update
        player.update()
        player.draw(screen)
        # Bullets update
        bullets_group.update()
        bullets_group.draw(screen)

    clock.tick(60)
    pygame.display.update()
