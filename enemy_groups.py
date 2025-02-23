import pygame
from init import *
from enemies import Chicken,ChickenParachute,Boss
import random
import math
from utils import extract_frames
chicken_green_sheet = pygame.image.load("Content/Enemy/chickenGreen.png").convert_alpha()
chicken_red_sheet = pygame.image.load("Content/Enemy/chickenRed.png").convert_alpha()
chicken_green_animation_list = extract_frames(chicken_green_sheet, 1, 10)
chicken_red_animation_list = extract_frames(chicken_red_sheet, 1, 10)
class BossGroup:
    def __init__(self, boss_wave):
        self.wave = boss_wave
        self.chicken_group = pygame.sprite.Group()
        self.genarate_boss()
    def genarate_boss(self):
        for boss in self.wave:
            boss_obj = Boss(type=boss['type'], x=boss['position_x'], y=boss['position_y'])
            self.chicken_group.add(boss_obj)
    def update(self , groups):
        if len(self.chicken_group) == 0:
            groups.remove(self)
            del self
            return
        self.chicken_group.update()
        self.chicken_group.draw(screen)
class ChickenGroup:  # check
    def __init__(
            self,
            x,
            y,
            chicken_type,
            number_of_chickens,
            number_of_parachute_chickens,
            chicken_per_row,
            initial_x,
            initial_y,
            group_order,
            hidden,
    ):
        self.chicken_group = pygame.sprite.Group()
        self.drop = False  # if true make chickens of group have chance drop the eggs
        self.x = x
        self.y = y
        self.group_order = group_order
        self.hidden = hidden
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.number_of_chickens = number_of_chickens
        self.chicken_per_row = chicken_per_row
        self.number_of_parachute_chickens = number_of_parachute_chickens
        self.number_of_parachute_chickens_generated = 0
        if chicken_type == "red chicken":
            self.animation_list = chicken_red_animation_list
        elif chicken_type == "green chicken":
            self.animation_list = chicken_green_animation_list
        self.angle = random.uniform(0, 2 * math.pi)
        self.killed_chicken = 0
        self.generate_chicken_group()

    def generate_chicken_group(self):
        relative_height = self.initial_y
        chicken_order_in_row = 0
        for _ in range(self.number_of_chickens):
            if chicken_order_in_row == self.chicken_per_row + 1:
                chicken_order_in_row = 1
                relative_height += (chicken.image.get_height() / 2) + 10
            relative_distance = self.initial_x + (chicken_order_in_row * 60)
            chicken = Chicken(
                image=None,
                animation_list=self.animation_list,
                x=relative_distance,
                y=relative_height,
                group_order=self.group_order,
            )
            self.chicken_group.add(chicken)
            chicken_order_in_row += 1

    def generating_parachute_chicken(self):
        if (
                self.number_of_parachute_chickens
                and self.number_of_parachute_chickens
                > self.number_of_parachute_chickens_generated
        ):
            if not random.randint(0, 180):
                parachute_chicken = ChickenParachute()
                self.chicken_group.add(parachute_chicken)
                self.number_of_parachute_chickens_generated += 1

    def move_randomly(self):  # move all chickens randomly (inaccurate till now)
        speed = 3
        move_in_x = speed * math.cos(self.angle)
        move_in_y = speed * math.sin(self.angle)
        # if self.rect.left + move_in_x <= 90 or self.rect.right + move_in_x >= WIDTH - 90:
        #     self.angle = (math.pi / 2)- self.angle  # Reverse X direction
        #     move_in_x = speed * math.cos(self.angle)
        # elif self.rect.top + move_in_y <= 30 or self.rect.bottom + move_in_y >= HEIGHT - 30:
        #     self.angle = -self.angle  # Reverse Y direction
        #     move_in_y = speed * math.sin(self.angle)
        for chicken in self.chicken_group:
            chicken.rect.x += int(move_in_x)
            chicken.rect.y += int(move_in_y)
        self.rect.x += int(move_in_x)
        self.rect.y += int(move_in_y)

    def change_angle(self):
        self.angle = random.uniform(0, 2 * math.pi)

    def update(self, move , groups):  # (move) for moving randomly or not
        if len(self.chicken_group) == 0:
            groups.remove(self)
            del self
            return
        first_chicken = self.chicken_group.sprites()[0]
        if self.hidden == "right" and first_chicken.rect.center[0] > self.x and not self.drop:
            for chicken in self.chicken_group:
                if isinstance(chicken, ChickenParachute):
                    break
                chicken.rect.x -= 2
        elif self.hidden == "left" and first_chicken.rect.center[0] < self.x and not self.drop:
            for chicken in self.chicken_group:
                if isinstance(chicken, ChickenParachute):
                    break
                chicken.rect.x += 2
        elif self.hidden == "down" and first_chicken.rect.center[1] > self.y and not self.drop:
            for chicken in self.chicken_group:
                if isinstance(chicken, ChickenParachute):
                    break
                chicken.rect.y -= 2
        elif self.hidden == "up" and first_chicken.rect.center[1] < self.y and not self.drop:
            for chicken in self.chicken_group:
                if isinstance(chicken, ChickenParachute):
                    break
                chicken.rect.y += 2
        else:
            self.drop = True
        self.generating_parachute_chicken()
        self.chicken_group.update(self.drop)
        self.chicken_group.draw(screen)