import random

from init import *
from utils import extract_frames

lvl_up_token_sheet = pygame.image.load("Content/bullet/give.png").convert_alpha()
lvl_up_animation_list = extract_frames(lvl_up_token_sheet, 1, 25)

egg_break_animation_sheet = pygame.image.load("Content/Enemy/eggBreak.png").convert_alpha()
eqq_break_animation_list = extract_frames(egg_break_animation_sheet, 1, 8)

gifts_animation_sheet_list = []
bullet_change_animation_lists = []
for index in range(2):
    gifts_animation_sheet_list.append(
        pygame.transform.smoothscale(
            pygame.image.load(
                f"Content/bullet/gift{index}_spritesheet.png"
            ).convert_alpha(),
            (512, 306),
        )
    )
    bullet_change_animation_lists.append(
        extract_frames(gifts_animation_sheet_list[index], 5, 10)
    )


roasted_leg_image = pygame.image.load("Content/Enemy/Roasted0.webp").convert_alpha()
roasted_leg_image = pygame.transform.scale_by(roasted_leg_image, 0.45)
roasted_chicken_image = pygame.image.load("Content/Enemy/Roasted1.webp").convert_alpha()
roasted_chicken_image = pygame.transform.scale_by(roasted_chicken_image, 0.35)
roasted_list = [roasted_leg_image, roasted_chicken_image]

egg_image = pygame.image.load("Content/Enemy/egg.png").convert_alpha()
egg_lay_sound = pygame.mixer.Sound("Content/Music/chicken/Chicken_lay.ogg")


class Drops(pygame.sprite.Sprite):
    """Base class for drops and collectibles."""

    def __init__(self, animation_list=None, image=None):
        super().__init__()
        self.gravity = 1.8
        if image:
            self.image = image
        elif animation_list:
            self.image = animation_list[0]
        if animation_list:
            self.frames = animation_list
            self.frames_count = len(self.frames)
            self.frame_index = 0
            self.frame_speed = 0.2
        self.rect = self.image.get_rect(
            midbottom=(random.randint(self.image.get_width() + 5, WIDTH - self.image.get_width() - 5), -100)
        )
        self.mask = pygame.mask.from_surface(self.image)

    def drops(self):
        """Moves the drop downward with gravity."""
        self.rect.y += self.gravity
        if self.rect.y > HEIGHT:
            self.kill()

    def animate(self):
        """Animates the drop."""
        self.frame_index += self.frame_speed
        if self.frame_index >= self.frames_count:
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        """Updates the drop's state (e.g., movement, animation)."""
        self.drops()
        self.animate()


class LvlUpToken(Drops):
    """Level-up token drop."""

    def __init__(self):
        super().__init__(lvl_up_animation_list)


class BulletChangeGift(Drops):
    """Bullet change gift drop."""

    def __init__(self):
        self.type = random.randint(0, 1)
        super().__init__(bullet_change_animation_lists[self.type])


class Egg(Drops):
    """Egg drop."""

    def __init__(self, pos=None):
        super().__init__(eqq_break_animation_list, egg_image)
        self.frame_speed = 0.1
        self.broken = False
        if pos:
            self.rect.midbottom = pos
        if settings.sound_effects:
            egg_lay_sound.play()

    def update(self):
        """Updates the egg's state (e.g., breaking animation)."""
        if self.rect.y > HEIGHT - 24:
            self.animate()
            self.broken = True
            if self.frame_index >= 7.9:
                self.kill()
        else:
            self.drops()


class Meat(Drops):
    """Meat drop."""

    def __init__(self, meat_type: int, pos: tuple):
        super().__init__(image=roasted_list[meat_type])
        self.type = meat_type
        self.rect.midbottom = pos

    def update(self):
        """Updates the meat's state (e.g., movement)."""
        self.drops()
