import math
import time  # Used for cooldown timer
from random import randint

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Content/ship.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (SHIP_SIZE, SHIP_SIZE))
        self.rect = self.image.get_rect(midbottom=(SHIP_POS[0], SHIP_POS[1]))
        self.last_shot_time = 0  # Store the last time a bullet was fired
        self.bullet_lvl = 1
        self.bull_type = 'a'
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
        spread = min(bull_lv, 5)  # Ensure bullet pattern follows the levels

        offsets = [-bullet_size[0] * i for i in range(spread // 2, 0, -1)] + [0] + [bullet_size[0] * i for i in
                                                                                    range(1, spread // 2 + 1)]
        angles = [-self.angle * (i / (spread // 2)) for i in range(spread // 2, 0, -1)] + [0] + [
            self.angle * (i / (spread // 2)) for i in range(1, spread // 2 + 1)]

        for offset, angle in zip(offsets, angles):
            push_back = bullet_size[1] / 2 if abs(angle) == self.angle else bullet_size[1] / 4 if angle else 0
            bullets_g.add(Bullet(self, offset=offset, push_back=push_back, angle=angle))

    def check_collisions(self, lvl_token_g, ):  # more efficient way to check for mask collisions
        rect_collide_list = pygame.sprite.spritecollide(player.sprite, lvl_token_g, False)
        if rect_collide_list:
            for sprite in rect_collide_list:
                if pygame.sprite.collide_mask(player.sprite, sprite):
                    self.bullet_lvl += 1
                    sprite.kill()

    def update(self):
        if self.bull_type == 'b':
            self.angle = 20
        else:
            self.angle = 0
        self.player_move()
        self.check_input(bullets_group)
        self.check_collisions(lvl_token_group)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player: Player, offset=0.0, angle=0.0, push_back=0.0):
        super().__init__()
        self.image = pygame.image.load(f"Content/bullet/{player.bull_type}1.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (10, 20))
        self.angle = angle
        self.image = pygame.transform.rotate(self.image, -angle)
        self.rect = self.image.get_rect(midbottom=(player.rect.centerx + offset, player.rect.top + push_back))
        self.speed = 8
        try:
            pygame.mixer.Sound("Content/Music/bullet/a.ogg").play()
        except pygame.error as e:
            print(f"Sound file error: {e}")

    def update(self):
        self.rect.x += self.speed * math.sin(math.radians(self.angle))
        self.rect.y -= self.speed * math.cos(math.radians(self.angle))
        if self.rect.bottom < 0:  # Remove if off-screen
            self.kill()


class Drops(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frame_speed = None
        self.frames = None
        self.rect = None
        self.gravity = None
        self.frame_index = None
        self.frames_count = None
        self.image = None

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
        super().__init__()
        self.frames = lvl_up_animation_list
        self.frame_index = 0
        self.frame_rate = 100
        self.image = lvl_up_animation_list[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(WIDTH / 2, 0))
        self.frames_count = len(lvl_up_animation_list)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self) -> None:
        self.drops()
        self.animate()


class BulletChangeGift(Drops):  # todo
    pass


class Enemies(pygame.sprite.Sprite):  # todo
    def __init__(self):
        super().__init__()


class RedChicken(Enemies):  # todo
    def __init__(self):
        super().__init__()


WIDTH, HEIGHT = 910, 558  # Screen dimensions
SHIP_SIZE = 50
SHIP_POS = [WIDTH / 2, HEIGHT - 20]  # Starting position
BULLET_COOLDOWN = 0.3  # Cooldown between shots

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Invasion: Deluxe Edition")
# loading up animations
lvl_up_token_sheet = pygame.image.load("Content/bullet/give.png").convert_alpha()
lvl_up_animation_list = tuple([lvl_up_token_sheet.subsurface(pygame.Rect(i * 44, 0, 44, 37)) for i in range(25)])

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

player = pygame.sprite.GroupSingle(Player())
bullets_group = pygame.sprite.Group()
lvl_token_group = pygame.sprite.Group()

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
        if randint(0, 20) == 19:
            lvl_token_group.add(LvlUpToken())
        # lvl_token
        lvl_token_group.update()
        lvl_token_group.draw(screen)
        # Player
        player.update()
        player.draw(screen)
        # Bullets
        bullets_group.update()
        bullets_group.draw(screen)

    clock.tick(60)
    pygame.display.update()
