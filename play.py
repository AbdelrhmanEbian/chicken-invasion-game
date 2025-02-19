import math
import random
import time  # Used for cooldown timers

import pygame

import json
END = False

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
        self.damage = 1
        self.mask = pygame.mask.from_surface(self.image)  # creates a mask for precise collisions
        self.health = 3
        self.invincible = False
        self.invincible_timer = 0
        self.invincibility_duration = 1000
    def player_move(self):
        mouse_pos = pygame.mouse.get_pos()
        pos_diff = [self.rect.centerx - mouse_pos[0], self.rect.centery - mouse_pos[1]]
        self.rect.x -= pos_diff[0] * 0.16
        self.rect.y -= pos_diff[1] * 0.16
        self.rect.right = min(self.rect.right, WIDTH)
        self.rect.bottom = min(self.rect.bottom, HEIGHT - 10)

    def take_damage(self):
        self.health -= 1
        self.invincible = True
        self.invincible_timer = pygame.time.get_ticks()
        print(f"Player hit! Health: {self.health}")
        # if self.health <= 0: # todo don't forget to un comment after debugging
        #     self.kill()
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
        try:
            pygame.mixer.Sound("Content/Music/bullet/a.ogg").play()
        except pygame.error as e:
            print(f"Sound file error: {e}")
    def check_collisions(self, *sprite_groups) -> None:  # more efficient way to check for collisions
        for group in sprite_groups:
            rect_collide_list = pygame.sprite.spritecollide(player.sprite, group, False)
            if rect_collide_list:
                for sprite in rect_collide_list:
                    if pygame.sprite.collide_mask(player.sprite, sprite):
                        if group == lvl_token_group:  # check for collision with lvl tokens
                            self.bullet_lvl += 1
                            sprite.kill()
                            try:
                                pygame.mixer.Sound("Content/Music/bullet/levelUp.ogg").play()
                            except pygame.error as e:
                                print(f"Sound file error: {e}")
                        elif group == gifts_group:  # check for collision with gifts
                            sprite.kill()
                            if self.bull_type == self.bull_types[sprite.type]:
                                self.bullet_lvl += 1
                                try:
                                    pygame.mixer.Sound("Content/Music/bullet/levelUp.ogg").play()
                                except pygame.error as e:
                                    print(f"Sound file error: {e}")
                            else:
                                self.bull_type = self.bull_types[sprite.type]
                                self.bullet_lvl = 1
                        elif not self.invincible:
                            if group == eggs_group and not sprite.broken:  # check collision with the egg
                                sprite.kill()
                                self.take_damage()
                            elif group == chicken_parachute_group or isinstance(sprite , Chicken):
                                self.take_damage()
                                sprite.health -= 2

    def update(self):
        if self.bull_type == 'b':
            self.angle = 20
        else:
            self.angle = 0
        self.player_move()
        self.check_input(bullets_group)
        self.check_collisions(lvl_token_group, gifts_group, eggs_group , chicken_parachute_group , *[ chicken.chicken_list for chicken in level.get_current_wave()])
        # Invincibility
        if self.invincible:
            elapsed_time = pygame.time.get_ticks() - self.invincible_timer
            if elapsed_time > self.invincibility_duration:
                self.invincible = False  # End invincibility
            else:
                if (elapsed_time // 200) % 2 == 0:  # Blinking effect
                    self.image.set_alpha(128)  # Half-transparent
                else:
                    self.image.set_alpha(255)  # Fully visible
        else:
            self.image.set_alpha(255)  # Fully visible

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player1: Player, offset=0.0, angle=0.0, push_back=0.0) -> None:
        super().__init__()
        self.image = pygame.image.load(f"Content/bullet/{player1.bull_type}1.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (10, 20))
        self.angle = angle if player1.bull_type == 'b' else 0
        self.image = pygame.transform.rotate(self.image, -self.angle)
        self.rect = self.image.get_rect(midbottom=(player1.rect.centerx + offset, player1.rect.top + push_back))
        self.speed = 8
        self.damage = 1  # Set damage based on level
        
    def update(self):  # moves and dies
        self.rect.x += self.speed * math.sin(math.radians(self.angle))
        self.rect.y -= self.speed * math.cos(math.radians(self.angle))
        if self.rect.bottom < 0:  # Remove if off-screen
            self.kill()


class Drops(pygame.sprite.Sprite):
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
            midbottom=(random.randint(0, WIDTH - self.image.get_width()), 0))
        self.mask = pygame.mask.from_surface(self.image)

    def drops(self) -> None:
        self.rect.y += self.gravity
        if self.rect.y > HEIGHT:
            self.kill()

    def animate(self) -> None:
        self.frame_index += self.frame_speed
        if self.frame_index >= self.frames_count:
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self) -> None:
        self.drops()
        self.animate()


class LvlUpToken(Drops):
    def __init__(self):
        super().__init__(lvl_up_animation_list)


class BulletChangeGift(Drops):
    def __init__(self):
        self.type = random.randint(0, 1)
        super().__init__(bullet_change_animation_lists[self.type])
class Egg(Drops):
    def __init__(self, pos=None):
        super().__init__(eqq_break_animation_list, egg_image)
        self.frame_speed = 0.1
        self.broken = False
        if pos:
            self.rect.midbottom = pos

    def update(self) -> None:  # todo
        if self.rect.y > HEIGHT - 24:
            self.animate()
            self.broken = True
            if self.frame_index >= 7.9:
                self.kill()
        else:
            self.drops()


# Chicken class

class ChickenParachute(Drops):
    def __init__(self):
        self.type = random.choice(["parachuted_red", "parachuted_blue"])
        image = None
        if self.type == "parachuted_red":
            image = parachute_red
        elif self.type == "parachuted_blue":
            image = parachute_blue
        super().__init__(image=image)
        self.gravity = 1
        self.health = 5

    def check_collision(self):
        no_of_bullets = len(pygame.sprite.spritecollide(self, bullets_group, True))
        if no_of_bullets:
            self.health -= no_of_bullets

    def update(self) -> None:  # todo
        self.drops()
        self.check_collision()
        if random.randint(0, 200) == 155:
            pos = self.rect.midbottom
            eggs_group.add(Egg(pos))
            egg_lay_sound.play()
        if self.health <= 0:
            self.kill()
            random.choice(chicken_die_sounds).play()


class Chicken(Drops):
    def __init__(self , image , animation_list , x , y ,  group_order):
        super().__init__( image=image , animation_list=animation_list )
        self.rect = self.image.get_rect(center=(x,y))
        self.float_x = float(self.rect.x)
        self.float_y = float(self.rect.y)
        self.health = 5
        self.group_order = group_order
    def check_collision(self):
        no_of_bullets = len(pygame.sprite.spritecollide(self, bullets_group, True))
        if no_of_bullets:
            self.health -= no_of_bullets
    def animate(self) -> None:
        if math.ceil(self.frame_index) >= self.frames_count or math.floor(self.frame_index) < 0:
            self.frame_speed *= -1 
        self.frame_index += self.frame_speed
        self.image = self.frames[int(self.frame_index)]
    def update(self , drop) -> None:  # todo
        self.check_collision()
        if self.health <= 0:
            self.kill()
            random.choice(chicken_die_sounds).play()
        if random.randint(0 , 1000) == 5 and drop :
            eggs_group.add(Egg(self.rect.midbottom))
        self.animate()

class chickenGroup():
    def __init__(self , x , y , type , number_of_chickens , chicken_per_row , transform_x  , transform_y , group_order):
        self.chicken_list = pygame.sprite.Group()
        self.drop = False
        self.x = x
        self.y = y
        self.group_order = group_order
        self.hidden = 'right' if transform_x > 0 else 'left' if not transform_x ==  0 else 'down' if transform_y > 0 else 'up'  
        self.transform_x = transform_x
        self.transform_y = transform_y
        self.number_of_chickens = number_of_chickens
        self.checken_per_row = chicken_per_row
        if type == "red chicken":
            self.animation_list = chicken_red_animation_list
        elif type == "green chicken":
            self.animation_list = chicken_green_animation_list
        self.angle = random.uniform(0 , 2 * math.pi)
        self.killed_chicken = 0
        self.generate_chicken_group()
    def generate_chicken_group(self):
        relative_height = self.transform_y + self.y if not self.hidden == 'down' else self.transform_y
        chicken_order_in_row = 1
        for _ in range(self.number_of_chickens):
            if  chicken_order_in_row == self.checken_per_row + 1:
                chicken_order_in_row = 1
                relative_height += (chicken.image.get_height()) + 10
            relative_distance = (self.transform_x + self.x +  ((chicken_order_in_row) * 60)) if not self.hidden == 'right' else (self.transform_x - ((chicken_order_in_row) * 60) )
            chicken = Chicken(image=None,  animation_list=self.animation_list , x = relative_distance  ,y=relative_height , group_order = self.group_order)
            self.chicken_list.add(chicken)
            chicken_order_in_row += 1
    def move_randomly(self): # move all chickens randomly (inaccurate till now)
        speed  = 3
        move_in_x = speed * math.cos(self.angle)
        move_in_y = speed * math.sin(self.angle)
        # if self.rect.left + move_in_x <= 90 or self.rect.right + move_in_x >= WIDTH - 90:
        #     self.angle = (math.pi / 2)- self.angle  # Reverse X direction
        #     move_in_x = speed * math.cos(self.angle)
        # elif self.rect.top + move_in_y <= 30 or self.rect.bottom + move_in_y >= HEIGHT - 30:
        #     self.angle = -self.angle  # Reverse Y direction
        #     move_in_y = speed * math.sin(self.angle)
        for chicken in self.chicken_list:
            chicken.rect.x += int(move_in_x)
            chicken.rect.y += int(move_in_y)
        self.rect.x += int(move_in_x)
        self.rect.y += int(move_in_y)
    def change_angle(self):
        self.angle = random.uniform(0 , 2 * math.pi)
    def update(self , move):
        # self.move_randomly()
        if len(self.chicken_list) == 0:
            level.current_wave.groups.remove(self)
            del self
            return
        first_chicken = self.chicken_list.sprites()[0 if not self.hidden == 'right' else -1]
        if self.hidden == 'right' and first_chicken.rect.x > self.x and self.drop == False:
            for chicken in self.chicken_list:
                chicken.rect.x -= 2
        elif self.hidden == 'left' and first_chicken.rect.x < self.x and self.drop == False:
            for chicken in self.chicken_list:
                chicken.rect.x += 2
        elif self.hidden == 'down' and first_chicken.rect.y > self.y and self.drop == False:
            for chicken in self.chicken_list:
                chicken.rect.y -= 2 

        elif self.hidden == 'up' and first_chicken.rect.y < self.y and self.drop == False:
            for chicken in self.chicken_list:
                chicken.rect.y += 2
        else : 
            self.drop = True
        # if move:
            # self.move_randomly()
        self.chicken_list.update(self.drop)
        self.chicken_list.draw(screen)
# Boss class
class Boss(Drops):
    def __init__(self, type):
        super().__init__()
        self.type = type
        if self.type == "boss":
            self.image = chicken_boss_sheet
            self.health = 10
        elif self.type == "boss_red":
            self.image = chicken_bossRed_sheet
            self.health = 15
        self.rect = self.image.get_rect(midbottom=(WIDTH / 2, 0))
        self.speed = 2

    def update(self):
        # Move the boss down
        if self.rect.y < 50:  # Stop at a certain position
            self.rect.y += self.speed

    def attack(self):
        # Spawn multiple eggs or other attacks
        for _ in range(3):  # Spawn 3 eggs
            egg = Egg(self.rect.midbottom)
            Egg.add(egg)


def extract_frames(spritesheet, sheet_width: float, sheet_height: float, rows: int, cols: int) -> tuple:
    sprite_width, sprite_height = sheet_width / cols, sheet_height / rows
    return tuple(
        spritesheet.subsurface(pygame.Rect(col * sprite_width, row * sprite_height, sprite_width, sprite_height))
        for col in range(cols) for row in range(rows)
    )


# -------------------------------------------------------------------------------
WIDTH, HEIGHT = 910, 558  # Screen dimensions
SHIP_SIZE = 50
SHIP_POS = [WIDTH / 2, HEIGHT - 20]  # Starting position
BULLET_COOLDOWN = 0.3  # Cooldown between shots

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Invasion: Deluxe Edition")

# music load
pygame.mixer.set_num_channels(20)
egg_lay_sound = pygame.mixer.Sound("Content/Music/chicken/Chicken_lay.ogg")
chicken_die_sounds = list([pygame.mixer.Sound(f"Content/Music/chicken/Chicken_death{i}.ogg") for i in range(1, 5)])
bullet_sound = pygame.mixer.Sound("Content/Music/bullet/a.ogg")
# -------------------------------------------------------------------------------
egg_image = pygame.image.load("Content/Enemy/egg.png").convert_alpha()
parachute_red = pygame.image.load("Content/Enemy/chickenParachuteRed.png").convert_alpha()
parachute_red = pygame.transform.scale_by(parachute_red, 0.65)
parachute_blue = pygame.image.load("Content/Enemy/chickenParachuteBlue.png").convert_alpha()
parachute_blue = pygame.transform.scale_by(parachute_blue, 0.65)
chicken_green_sheet = pygame.image.load("Content/Enemy/chickenGreen.png").convert_alpha()
chicken_red_sheet = pygame.image.load("Content/Enemy/chickenRed.png").convert_alpha()
chicken_boss_sheet = pygame.image.load("Content/Enemy/boss.png").convert_alpha()
chicken_bossRed_sheet = pygame.image.load("Content/Enemy/bossRed.png").convert_alpha()
# -------------------------------------------------------------------------------
# loading up animations
chicken_green_animation_list = extract_frames(chicken_green_sheet, 469, 38, 1, 10)
chicken_red_animation_list = extract_frames(chicken_red_sheet, 400, 35, 1, 10)
lvl_up_token_sheet = pygame.image.load("Content/bullet/give.png").convert_alpha()
lvl_up_animation_list = extract_frames(lvl_up_token_sheet, 1100, 37, 1, 25)
gifts_animation_sheet_list = []
bullet_change_animation_lists = []
egg_break_animation_sheet = pygame.image.load("Content/Enemy/eggBreak.png").convert_alpha()
eqq_break_animation_list = extract_frames(egg_break_animation_sheet, 224, 24, 1, 8)
for index in range(2):
    gifts_animation_sheet_list.append(
        pygame.transform.smoothscale(pygame.image.load(f"Content/bullet/gift{index}_spritesheet.png").convert_alpha(),
                                     (512, 306)))
    bullet_change_animation_lists.append(extract_frames(gifts_animation_sheet_list[index], 512, 306, 5, 10))

# overlay
overlay = pygame.Surface((WIDTH, HEIGHT))
overlay.fill((0, 0, 0))
# Set up font
pygame.font.init()
font = pygame.font.Font(None, 50)
angle_event = pygame.USEREVENT + 1
pygame.time.set_timer(angle_event, 2000)
# Create text surface
text_surface = font.render("Press 'P' to continue", True, (255, 255, 255))
text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
clock = pygame.time.Clock()
bk_ground = pygame.image.load("Content/background/background.png").convert()

health_icon = pygame.image.load("Content/background/heart.png").convert_alpha()
health_icon_scaled = pygame.transform.scale_by(health_icon, 0.1)

# Groups
player = pygame.sprite.GroupSingle(Player())
bullets_group = pygame.sprite.Group()
lvl_token_group = pygame.sprite.Group()
gifts_group = pygame.sprite.Group()
eggs_group = pygame.sprite.Group()
chicken_parachute_group = pygame.sprite.Group()
bosses = pygame.sprite.Group()
# ------------------------------------------------------------------------------
pause = False
overlay_alpha = 0
fade_speed = 8  # Speed of fade-in effect  
class Wave(pygame.sprite.Sprite):
    def __init__(self , level , wave ):
        self.current_level = level
        self.current_wave_number = wave
        self.read_wave_data()
        self.wave_ended = False
        self.total_chickens =  sum([ group["number of chicken"] for group in self.data['waves']])
        self.number_of_groups = len(self.data['waves'])
        self.waves = self.data['waves']
        self.groups = []
        self.data = {}
        self.generate_groups()
    def read_wave_data(self):
        with open (f'levels_data/level_{self.current_level}_data/waves/wave_{self.current_wave_number}_data.json' , 'r') as file:
            data = json.load(file)
            self.data = data
    def generate_groups(self):
        chicken_wave = [chickenGroup(x = group["position x"] , y = group['position y'] , number_of_chickens= group["number of chicken"] , type=group["type"] , chicken_per_row= group["number of chicken per row"] , transform_x= group["transform x"] , transform_y = group['transform y'] , group_order = index)  for index, group in enumerate(self.waves)]   
        self.groups = chicken_wave
    def get_groups(self):
        return self.groups
    def draw_level_and_wave(self):
        text = font.render(f"you have finished level {self.current_level } wave {self.current_wave_number}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
    def update(self):
        if len(self.groups) == 0:
            self.wave_ended = True
            return
        move_randomly = [ chicken_group.drop for chicken_group in self.groups]
        for chicken_group in self.groups : 
            chicken_group.update( False if False in move_randomly else True)
        
level_event = pygame.USEREVENT + 2 

class Level():
    def __init__(self , level : int , wave : int):
        self.current_level = level
        self.data = {}
        self.current_wave_number = wave
        current_wave = self.generate_wave()
        self.current_wave = current_wave
        self.level_ended = False
        self.read_level_data()
        self.chicken_per_wave =  self.data['number of chickens in each wave']
        self.number_of_waves = self.data['number of waves']
    def generate_wave(self):
        wave = Wave(self.current_level , self.current_wave_number)
        return wave
    def read_level_data(self):
        with open (f'levels_data/level_{self.current_level}_data/level_data.json' , 'r') as file:
            data = json.load(file)
            self.data = data
        
    def get_current_wave(self):
        return self.current_wave.get_groups()
    def update(self):
        if self.current_wave.wave_ended:
            if not hasattr(self, 'wave_end_time'):  # Check if wave_end_time is not already set
                self.wave_end_time = pygame.time.get_ticks()  # Record the time when the wave ended
                if not hasattr(self, 'music_played'):  # Check if music has already been played
                    self.music = pygame.mixer.Sound('Content/Music/Gamewin.ogg')
                    self.music.play()
                    self.music_played = True  # Mark music as played

            # Calculate the time elapsed since the wave ended
            elapsed_time = pygame.time.get_ticks() - self.wave_end_time

            if elapsed_time >= 3000:  # Wait for 3 seconds (3000 milliseconds)
                self.music.stop()  # Stop the music
                if self.current_wave_number == self.number_of_waves:
                    if self.current_level == 2:
                        global END
                        END = True
                        return
                    self.current_level += 1
                    self.current_wave_number = 1  # Reset wave number for the next level
                    self.read_level_data()
                else:
                    self.current_wave_number += 1

                del self.current_wave
                self.current_wave = self.generate_wave()
                del self.wave_end_time  # Reset the timer for the next wave
                del self.music_played  # Reset the music flag for the next wave  
            else : 
                self.current_wave.draw_level_and_wave()             
        else:
            self.current_wave.update()
start_up_level = 1
start_up_wave = 1
level = Level(start_up_level , start_up_wave)
winner_music = pygame.mixer.Sound('Content/Music/Gamewin.ogg')

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
        if event.type == angle_event:
            for chicken_group in level.get_current_wave():
                chicken_group.change_angle()
    # Screen
    screen.blit(bk_ground, (0, 0))
    if pause:
        # Gradually increase overlay opacity for fade-in effect
        if overlay_alpha < 180:
            overlay_alpha += fade_speed
            overlay_alpha = min(overlay_alpha, 180)  # set to 180 at max
        pygame.mouse.set_visible(True)
        overlay.set_alpha(overlay_alpha)
        screen.blit(overlay, (0, 0))
        screen.blit(text_surface, text_rect)
    elif END == True:
        text = font.render("Winner", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        if winner_music.get_num_channels() == 0:
            winner_music.play() # Play the music
        pygame.display.update()
    elif not END:  # continue playing + anything we want to disappear upon pausing
        pygame.mouse.set_visible(False)
        # spawns tokens and gifts randomly todo: make it depends on something
        if not random.randint(0, 180):
            lvl_token_group.add(LvlUpToken())
            gifts_group.add(BulletChangeGift())
            eggs_group.add(Egg())
            chicken_parachute_group.add(ChickenParachute())
        # Gifts update
        gifts_group.update()
        gifts_group.draw(screen)
        # lvl_token update
        lvl_token_group.update()
        lvl_token_group.draw(screen)
        # health update
        for i in range(player.sprite.health):
            screen.blit(health_icon_scaled, (WIDTH - 45 * (i + 1), HEIGHT - 45))
        # Bullets update
        bullets_group.update()
        bullets_group.draw(screen)
        # eggs update
        eggs_group.update()
        eggs_group.draw(screen)
        # chicken parachute update
        # chicken_parachute_group.update()
        # chicken_parachute_group.draw(screen)
        # Player update
        player.update()
        player.draw(screen)
        # group.update()
        # group.draw(screen)
        level.update()    
    
    clock.tick(60)
    pygame.display.update()