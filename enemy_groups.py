import pygame
from init import *
from enemies import Chicken,Boss
import random
import math
from utils import extract_frames
chicken_green_sheet = pygame.image.load("Content/Enemy/chickenGreen.png").convert_alpha()
chicken_red_sheet = pygame.image.load("Content/Enemy/chickenRed.png").convert_alpha()
chicken_green_animation_list = extract_frames(chicken_green_sheet, 1, 10)
chicken_red_animation_list = extract_frames(chicken_red_sheet, 1, 10)
class ChickenGroup:  # check
    def __init__(
            self,
            x,
            y,
            chicken_type,
            number_of_chickens,
            chicken_per_row,
            initial_x,
            initial_y,
            hidden,
            move_randomly,
    ):
        self.can_move_randomly = move_randomly
        self.speed = 2
        self.last_move_time = pygame.time.get_ticks()
        self.arrival_time = 0
        self.move_interval = 3000
        self.chicken_group = pygame.sprite.Group()
        self.ability_to_move = False
        self.x = x
        self.y = y
        self.hidden = hidden
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.number_of_chickens = number_of_chickens
        self.chicken_per_row = chicken_per_row
        self.type = chicken_type
        if chicken_type == "red chicken":
            self.animation_list = chicken_red_animation_list
        elif chicken_type == "green chicken":
            self.animation_list = chicken_green_animation_list
        self.angle = random.uniform(0, 2 * math.pi)
        self.killed_chicken = 0
        self.generate_chicken_group()
    def generate_chicken_group(self):
        if self.type in ['red chicken' , 'green chicken']:
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
                )
                self.chicken_group.add(chicken)
                chicken_order_in_row += 1
        else :
            self.chicken_group.add(Boss(type=self.type, x=self.x, y=self.y , hidden=self.hidden, initial_x=self.initial_x, initial_y=self.initial_y))
    def move_randomly(self):
        move_in_x = self.speed * math.cos(self.angle)
        move_in_y = self.speed * math.sin(self.angle)
        distance_in_x = move_in_x * self.move_interval / 1000
        distance_in_y = move_in_y * self.move_interval / 1000
        left = min(chicken.rect.left for chicken in self.chicken_group)
        right = max(chicken.rect.right for chicken in self.chicken_group)
        top = min(chicken.rect.top for chicken in self.chicken_group)
        bottom = max(chicken.rect.bottom for chicken in self.chicken_group)
        if left + distance_in_x < 0 or right + distance_in_x > WIDTH:
            self.angle = math.pi - self.angle  # Reverse X direction
            move_in_x = self.speed * math.cos(self.angle)
            self.last_move_time = pygame.time.get_ticks()
        if top + distance_in_y < 0 or bottom + distance_in_y > HEIGHT:
            self.angle = -self.angle  # Reverse Y direction
            move_in_y = self.speed * math.sin(self.angle)
            self.last_move_time = pygame.time.get_ticks()
        for chicken in self.chicken_group:
            if isinstance(chicken, Boss):  # Skip Boss chickens
                continue
            chicken.rect.x += int(move_in_x)
            chicken.rect.y += int(move_in_y)

            chicken.rect.x = max(0, min(chicken.rect.x, WIDTH - chicken.rect.width))
            chicken.rect.y = max(0, min(chicken.rect.y, HEIGHT - chicken.rect.height))
    def change_angle(self):
        self.angle = random.uniform(0, 2 * math.pi)
    def update(self , groups):  # (move) for moving randomly or not
        if len(self.chicken_group) == 0:
            groups.remove(self)
            del self
            return
        first_chicken = self.chicken_group.sprites()[0]
        if self.hidden == "right" and first_chicken.rect.center[0] > self.x and not self.ability_to_move:
            for chicken in self.chicken_group:
                chicken.rect.x -= 2
        elif self.hidden == "left" and first_chicken.rect.center[0] < self.x and not self.ability_to_move:
            for chicken in self.chicken_group:
                chicken.rect.x += 2
        elif self.hidden == "down" and first_chicken.rect.center[1] > self.y and not self.ability_to_move:
            for chicken in self.chicken_group:
                chicken.rect.y -= 2
        elif self.hidden == "up" and first_chicken.rect.center[1] < self.y and not self.ability_to_move:
            for chicken in self.chicken_group:
                chicken.rect.y += 2
        else:
            if not self.ability_to_move:
                self.arrival_time = pygame.time.get_ticks()
                self.ability_to_move = True
        if self.ability_to_move and self.can_move_randomly:
            current_time = pygame.time.get_ticks()
            if current_time - self.arrival_time >= 3000:  # 3-second delay
                self.move_randomly()
                if current_time - self.last_move_time >= self.move_interval:
                    self.change_angle()
                    self.last_move_time = current_time
        self.chicken_group.update()
        self.chicken_group.draw(screen)