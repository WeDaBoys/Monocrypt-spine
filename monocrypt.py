# *********************************************************
# Program: monocrypt.py
# Course: PSP0101 PROBLEM SOLVING AND PROGRAM DESIGN
# Class: TL6L
# Year: 2023/24 Trimester 1
# Names: MUHAMMAD IRFAN SYAZWAN BIN MD. ARIFIN | ERIN KLARISA BINTI MOHAMMAD FAIRUZ | LEE MING FUNG
# IDs: 1221108127 | 1221109372 | 1221109363
# Emails: 1221108127@student.mmu.edu | 1221109372@student.mmu.edu.my | 1221109363@student.mmu.edu.my
# Phones: 0123559141 | 0193517153 | 0182021399
# *********************************************************

import pygame
from pygame.locals import *
import random
import sys
import math

pygame.init()

#sound
pygame.mixer.init()
player_hurt_sound = pygame.mixer.Sound('player hit.wav')
enemy_hurt_sound = pygame.mixer.Sound('enemy hit.wav')
space_start_sound = pygame.mixer.Sound('start space bar.wav')
player_death_sound = pygame.mixer.Sound('death sound.wav')
retry_sound = pygame.mixer.Sound('retry.wav')
player_shot_sound = pygame.mixer.Sound('player_shot.mp3')
enemy_spawn_sound = pygame.mixer.Sound('enemy spawn.mp3')
teleport_sound = pygame.mixer.Sound('teleport.wav')
pause_on_sound = pygame.mixer.Sound('pause on.wav')
pause_off_sound = pygame.mixer.Sound('pause off.wav')
enemy_shoot_sound = pygame.mixer.Sound('enemy shot.wav')
quit_sound = pygame.mixer.Sound('quit.wav')
perk_sound = pygame.mixer.Sound('perk obtained.wav')
deny_sound = pygame.mixer.Sound('deny.wav')
title_music = "title_music.mp3"
game_music = "ingame_music.mp3"
end_music = "end_music.mp3"
perk_sound.set_volume(1.3)
enemy_hurt_sound.set_volume(0.3)
player_hurt_sound.set_volume(0.2)
player_shot_sound.set_volume(0.3)
enemy_spawn_sound.set_volume(0.1)
teleport_sound.set_volume(0.6)
#Variables
FPS = 60
FramePerSec = pygame.time.Clock()
SPEED = 5
p1_health = 60
player_bullet_speed = 5
vec = pygame.math.Vector2
HEIGHT = 350
WIDTH = 700
ACC = 0.3
FRIC = -0.10
COUNT = 0
x = 50
y = 50
HEART_WIDTH = 70
HEART_HEIGHT = 70
TELEPORT_DISTANCE = 100
TELEPORT_COOLDOWN = 60 * 5
points = 0 # For purchasing upgrades
score = 0 # For high scores
paused = False
enablekeypress_events = True

#screen information
screen_width = 1056
screen_height = 840
screen = pygame.display.set_mode((screen_width, screen_height),)
pygame.display.set_caption("MonoCrypt")

#background
background = pygame.image.load("background.jpg")
background = pygame.transform.scale (background, (screen_width, screen_height))
screen_width, screen_height = background.get_size()

#colours
white = (255, 255, 255)
black = (0,0,0)
yellow = (255, 255, 200)
red = (215, 50, 80)
green = (0, 255, 0)
blue = (50, 150, 215)

#font
font = pygame.font.Font('OCRAEXT.TTF', 50)
text_color = (255, 255, 255)
def display_text(text, x, y):
    text_surface = font.render(text, True, text_color)
    screen.blit(text_surface, (x, y))

# Load high scores from a file
try:
    with open('high_scores.txt', 'r') as f:
        high_scores = [int(line.strip()) for line in f if line.strip().isdigit()]
except FileNotFoundError:
    high_scores = []

#start
def start_screen():
    pygame.mixer.music.load(title_music)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    title = pygame.image.load("title screen.png")
    title = pygame.transform.scale(title,(screen_width,screen_height))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_start_sound.play()

                    
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(game_music)
                    pygame.mixer.music.set_volume(0.05)
                    pygame.mixer.music.play(-1)

                    # Animation
                    for i in range(3):  
                        screen.fill((0, 0, 0))  
                        pygame.display.flip()
                        pygame.time.delay(150)  

                        screen.blit(title, (0, 0))
                        pygame.display.flip()
                        pygame.time.delay(150)  

                    return  

        screen.blit(title, (0,0))
        pygame.display.flip()


#game over
def game_over_screen(score):
    end_screen = pygame.image.load("end screen.png")
    end_screen = pygame.transform.scale(end_screen, (screen_width,screen_height))

    score_text = font.render(f'Your score is: {score}', True, (255, 255, 255))
    score_text_rect = score_text.get_rect(center=(screen_width/2, screen_height/2 + 80)) 

    while True:
        screen.fill(black)
        screen.blit(end_screen, (0,50))
        screen.blit(score_text, score_text_rect) 

        for i, high_score in enumerate(high_scores[:3]):  
            high_score_text_str = f'{i+1}. High Score : {str(high_score).rjust(3, " ")}'  
            high_score_text = font.render(high_score_text_str, True, (255, 255, 255))  
            high_score_text_rect = high_score_text.get_rect(center=(screen_width/2, screen_height/2 + 150 + i*50))  
            screen.blit(high_score_text, high_score_text_rect)  

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  
                    retry_sound.play()
                    global points
                    points = 0

                    # Animation
                    for i in range(3):  
                        screen.fill((0, 0, 0)) 
                        pygame.display.flip()
                        pygame.time.delay(150) 

                        screen.blit(end_screen, (0, 50)) 
                        screen.blit(score_text, score_text_rect) 

                        for i, high_score in enumerate(high_scores[:3]):  
                            high_score_text_str = f'{i+1}. High Score : {str(high_score).rjust(3, " ")}' 
                            high_score_text = font.render(high_score_text_str, True, (255, 255, 255))  
                            high_score_text_rect = high_score_text.get_rect(center=(screen_width/2, screen_height/2 + 150 + i*50))
                            screen.blit(high_score_text, high_score_text_rect) 

                        pygame.display.flip()
                        pygame.time.delay(150)
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(game_music)
                    pygame.mixer.music.set_volume(0.05)
                    pygame.mixer.music.play(-1)  

                    return True  
                elif event.key == pygame.K_q:
                    quit_sound.play()
                    pygame.time.delay(850)  
                    return False  

# Button
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path, action, name, tooltip, cost):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.action = action
        self.name = name
        self.tooltip = tooltip
        self.cost = cost

    def is_clicked(self, mouse_pos):
        clicked = self.rect.collidepoint(mouse_pos)
        if clicked and self.action:
            self.action()
    
def show_tooltip(button):
    name_text = font.render(button.name, True, (255, 255, 255))
    tooltip_text = font.render(button.tooltip, True, (255, 255, 255))
    cost_text = font.render(f'COST: {button.cost}', True, (255, 255, 255))
    screen.blit(name_text, (screen_width * 0.06, screen_height * 0.63))
    screen.blit(tooltip_text, (screen_width * 0.06, screen_height * 0.7))
    screen.blit(cost_text, (screen_width * 0.06, screen_height * 0.77))

cost_speed = 10
cost_health = 20
cost_shoot = 5
#perks
def player_bullet_speed_increase():
    global player_bullet_speed, points, cost_shoot
    if points >= cost_shoot:
        perk_sound.play()
        player_bullet_speed += 0.7
        points -= cost_shoot
    else:
        deny_sound.play()

def player_movement_speed_increase():
    global SPEED, points, cost_speed
    if points >= cost_speed:
        perk_sound.play()
        SPEED += 0.4
        points -= cost_speed
    else:
        deny_sound.play()

def more_health():
    global points, cost_health
    if points >= cost_health:
        perk_sound.play()
        P1.health += 20
        points -= cost_health
    else:
        deny_sound.play()

buttons = [
    Button(screen_width * 0.06, screen_height * 0.25, 300, 300, 'speedy_projectiles.png', player_bullet_speed_increase, "Projectile Acceleration -", "Increases speed of projectile.", cost_shoot),
    Button(screen_width * 0.36, screen_height * 0.25, 300, 300, 'ectoplasm_feet.png', player_movement_speed_increase, "Ectoplasm Feet -", "Makes your feet go faster.", cost_speed),
    Button(screen_width * 0.66, screen_height * 0.25, 300, 300, 'more_lifeblood.png', more_health, "Lifeblood -", "Increases your health.", cost_health)
]

# Pause Menu
def pause_menu():
    paused_screen = pygame.image.load("paused.png")
    paused_screen = pygame.transform.scale(paused_screen, (screen_width, screen_height))
    points_text = font.render(f'POINTS: {points}', True, (255, 255, 255))
    screen.fill(black)
    screen.blit(paused_screen, (0,0))
    screen.blit(points_text, (10, 3))

    for button in buttons:
        screen.blit(button.image, button.rect.topleft)
        if button.rect.collidepoint(pygame.mouse.get_pos()):
            show_tooltip(button)

#bullets variables
bullets = []
shooting = False

class Bullet:
    def __init__(self, x, y, speed, direction, image, player_bullet):
        self.x = x
        self.y = y
        self.speed = player_bullet_speed if player_bullet==True else speed
        self.direction = direction
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.remove = False

    def move(self):
        dir_norm = self.direction.normalize()
        self.rect.move_ip(dir_norm.x * self.speed, dir_norm.y * self.speed)
    def draw(self, screen):
        screen.blit(self.image, self.rect)

desired_size = (62, 107)

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.x = screen_width / 2
        self.y = screen_height / 2
        self.initial_position = pygame.math.Vector2(self.x, self.y)
        self.image = pygame.image.load("player_front.png")
        self.image_front = pygame.image.load("player_front.png")
        self.image_left = pygame.image.load("player_left.png")
        self.image_right = pygame.image.load("player_right_0000.png")
        self.is_animated = False
        self.sprite = []
        self.sprite.append(pygame.image.load("player_right_0000.png"))
        self.sprite.append(pygame.image.load("player_right_0001.png"))
        self.sprite.append(pygame.image.load("player_right_0002.png"))
        self.sprite.append(pygame.image.load("player_right_0003.png"))
        self.sprite.append(pygame.image.load("player_right_0004.png"))
        self.sprite.append(pygame.image.load("player_right_0005.png"))
        self.sprite.append(pygame.image.load("player_right_0006.png"))
        self.sprite.append(pygame.image.load("player_right_0007.png"))
        self.sprite.append(pygame.image.load("player_right_0008.png"))
        self.sprite.append(pygame.image.load("player_right_0009.png"))
        self.sprite.append(pygame.image.load("player_right_0010.png"))
        self.sprite.append(pygame.image.load("player_right_0012.png"))
        self.sprite.append(pygame.image.load("player_right_0013.png"))
        self.current_sprite = 0
        self.image = self.sprite[self.current_sprite]

        self.teleport_sprites = []
        self.teleport_sprites.append(pygame.image.load("player_dash_0001.png"))
        self.teleport_sprites.append(pygame.image.load("player_dash_0002.png"))
        self.teleport_sprites.append(pygame.image.load("player_dash_0003.png"))
        self.teleport_sprites.append(pygame.image.load("player_dash_0004.png"))
        self.teleport_sprites.append(pygame.image.load("player_dash_0006.png"))
        self.current_teleport_sprite = 0
        self.is_teleporting = False

        self.death_anim = []
        self.death_anim.append(pygame.image.load("player_death anim_0000.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0001.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0002.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0003.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0004.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0005.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0006.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0007.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0008.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0009.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0010.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0011.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0012.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0013.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0014.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0015.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0016.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0017.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0018.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0019.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0020.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0021.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0022.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0023.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0024.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0025.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0026.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0027.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0028.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0030.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0031.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0032.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0033.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0034.png"))
        self.death_anim.append(pygame.image.load("player_death anim_0035.png"))

        self.current_death_sprite = 0
        self.is_dying = False

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.direction = pygame.math.Vector2(0, -1)  

        self.rect.width -= 20  
        self.rect.height -= 20  
        self.rect.center = (self.x, self.y)

        self.health = p1_health
        self.heart_image = pygame.image.load("heart.png")
        self.heart_image = pygame.transform.scale(self.heart_image, (HEART_WIDTH, HEART_HEIGHT))

        self.last_teleport_frame = -TELEPORT_COOLDOWN 
        self.hitbox = pygame.Rect(self.x, self.y, self.rect.width - 0, self.rect.height - 0)
        self.remove = False
        self.invincible = False
        self.death_sound_played = False

    def update(self):
        if enablekeypress_events:
            pressed_keys = pygame.key.get_pressed()
            if self.rect.top > 100:
                if pressed_keys[K_w]:
                    if pressed_keys[K_w]:
                        self.image = self.image_front
                        self.rect.move_ip(0, -SPEED)
                        self.direction = pygame.math.Vector2(0, -1)  # Up
            if self.rect.bottom < (screen_height - 100):    
                if pressed_keys[K_s]:
                    self.image = self.image_front
                    self.rect.move_ip(0, SPEED)
                    self.direction = pygame.math.Vector2(0, 1)  # Down
            if self.rect.left > 100:
                if pressed_keys[K_a]:
                    self.image = self.image_left
                    self.rect.move_ip(-SPEED, 0)
                    self.direction = pygame.math.Vector2(-1, 0)  # Left
            if self.rect.right < (screen_width - 100):        
                if pressed_keys[K_d]:
                    self.image = self.image_right
                    self.rect.move_ip(SPEED, 0)
                    self.direction = pygame.math.Vector2(1, 0)  # Right

            if pressed_keys[K_a] or pressed_keys[K_d] or pressed_keys[K_w] or pressed_keys[K_s]:
                self.current_sprite += 0.2
                if self.current_sprite >= len(self.sprite):
                    self.current_sprite = 0
                self.image = self.sprite[int(self.current_sprite)]

                if pressed_keys[K_a]:
                    self.image = pygame.transform.flip(self.image, True, False)
        
        if self.is_teleporting:
            self.current_teleport_sprite += 0.2
            if self.current_teleport_sprite >= len(self.teleport_sprites):
                self.current_teleport_sprite = 0
                self.is_teleporting = False  
                self.invincible = False  
            else:
                self.image = self.teleport_sprites[int(self.current_teleport_sprite)]
                if self.direction.x < 0:  
                    self.image = pygame.transform.flip(self.image, True, False)
        
        if self.is_dying:
            self.current_death_sprite +=0.2
            if self.current_death_sprite >= len(self.death_anim):
                self.is_dying = False
                return self.is_dying
            else:
                self.image = self.death_anim[int(self.current_death_sprite)]
                if self.direction.x < 0:  
                    self.image = pygame.transform.flip(self.image, True, False)

        self.hitbox.topleft = self.rect.topleft


    def draw(self, surface):
        surface.blit(self.image, self.rect)   
    
    #health bar
    def draw_health_hearts(self, surface):
        for i in range(self.health // 20):  
            surface.blit(self.heart_image, (10 + i * HEART_WIDTH, 10)) 
    
    #teleport
    def can_teleport(self, current_frame):
        
        return current_frame - self.last_teleport_frame >= TELEPORT_COOLDOWN

    def teleport(self, current_frame):
        self.is_teleporting = True
        self.invincible = True
        self.current_teleport_sprite = 0
        new_position = self.rect.move(self.direction * TELEPORT_DISTANCE)

        # Check if the new position would be outside the screen
        if new_position.top < 100:
            new_position.top = 100
        if new_position.bottom > (screen_height - 100):
            new_position.bottom = screen_height - 100
        if new_position.left < 100:
            new_position.left = 100
        if new_position.right > (screen_width - 100):
            new_position.right = screen_width - 100

        self.rect = new_position
        self.last_teleport_frame = current_frame

        #dying
    def player_dead(self):
        self.is_dying = True
        self.current_dying_sprite = 0

def draw_cooldown_bar(screen, x, y, total_width, height, remaining_cooldown, max_cooldown, color):
    
    bar_width = int(remaining_cooldown / max_cooldown * total_width)

    
    pygame.draw.rect(screen, color, pygame.Rect(x, y, bar_width, height))
cooldown_icon = pygame.image.load("cooldown_icon.png") 
cooldown_icon = pygame.transform.scale(cooldown_icon, (50, 50))  

P1 = Player()

# Enemy
class Enemy:
    def __init__(self, x, y, speed, image):
        x = random.randint(0, screen_width - 100 - 50)
        y = random.randint(0, screen_height - 100 - 50)
        self.rect = pygame.Rect(x, y, 50, 50)  
        self.speed = speed
        self.original_image = pygame.image.load(image)  
        self.image = pygame.transform.scale(self.original_image.copy(), (self.rect.width, self.rect.height))  
        self.invulnerability_duration = 180  
        self.spawn_duration = self.invulnerability_duration  
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height)) 
        self.bullets = []
        self.shoot_delay = 100
        self.direction = pygame.math.Vector2(1, 2)
        self.health = 100
        self.spawn_duration = 180 
        self.spawn_images = []
        self.spawn_images.append(pygame.image.load("spawn_0000.png"))
        self.spawn_images.append(pygame.image.load("spawn_0001.png"))
        self.spawn_images.append(pygame.image.load("spawn_0002.png"))
        self.spawn_images.append(pygame.image.load("spawn_0003.png"))
        self.spawn_images.append(pygame.image.load("spawn_0004.png"))
        self.spawn_images.append(pygame.image.load("spawn_0005.png"))
        self.spawn_images.append(pygame.image.load("spawn_0006.png"))
        self.spawn_images.append(pygame.image.load("spawn_0007.png"))
        self.spawn_images.append(pygame.image.load("spawn_0008.png"))
        self.current_spawn_sprite = 0  
        self.spawn_sprite_increment = len(self.spawn_images) / self.spawn_duration  
        self.is_dead = False
        self.death_sprites = []
        self.death_sprites.append(pygame.image.load("enemy_death_0000.png"))
        self.death_sprites.append(pygame.image.load("enemy_death_0001.png"))
        self.death_sprites.append(pygame.image.load("enemy_death_0002.png"))
        self.death_sprites.append(pygame.image.load("enemy_death_0003.png"))
        self.death_sprites.append(pygame.image.load("enemy_death_0004.png"))
        self.death_sprites.append(pygame.image.load("enemy_death_0005.png"))
        self.death_sprites.append(pygame.image.load("enemy_death_0006.png"))
        self.death_sprites.append(pygame.image.load("enemy_death_0007.png"))
        self.death_sprites.append(pygame.image.load("enemy_death_0008.png"))
        self.current_death_sprite = 0
        self.sound_played = False
        self.hit_image = pygame.image.load('enemy_death_0000.png')
        self.is_hit = False
        self.just_shot = False
    
    def hit(self):  
        self.is_hit = True
        self.image = self.hit_image

    def die(self):
        self.is_dead = True
        self.current_death_sprite = 0

    def update(self, player_dead):
        if not player_dead:  
            if self.spawn_duration > 0:
                self.current_spawn_sprite += self.spawn_sprite_increment  
                if self.current_spawn_sprite >= len(self.spawn_images):
                    self.current_spawn_sprite = 0
                self.image = self.spawn_images[int(self.current_spawn_sprite)]
                self.spawn_duration -= 1
                if self.spawn_duration == 0:  
                    self.image = pygame.transform.scale(self.original_image.copy(), (self.rect.width, self.rect.height)) 
                return
            if self.is_dead:
                self.current_death_sprite += 0.2
                if self.current_death_sprite >= len(self.death_sprites):
                    self.current_death_sprite = 0
                    active_enemies.remove(self)  
                return

            if random.randint(0, 50) == 1:  
                new_direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
                new_x = self.rect.x + self.speed * new_direction[0]
                new_y = self.rect.y + self.speed * new_direction[1]
                if 0 <= new_x <= (screen_width-80) - self.rect.width and 0 <= new_y <= (screen_height-80) - self.rect.height:
                    self.direction = new_direction   
                else:
                    self.direction = -new_direction
                    
            new_x = self.rect.x + self.speed * self.direction[0]
            new_y = self.rect.y + self.speed * self.direction[1]
            if 0 <= new_x <= (screen_width-80) - self.rect.width:
                self.rect.x = new_x
            if 0 <= new_y <= (screen_height-80) - self.rect.height:
                self.rect.y = new_y

            if self.shoot_delay > 0:
                self.shoot_delay -= 1
    def draw(self, surface):
        if self.is_dead:
            self.image = self.death_sprites[int(self.current_death_sprite)]
            death_image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
            surface.blit(death_image, self.rect)
        elif self.is_hit:  # If the enemy has been hit
            hit_image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
            surface.blit(hit_image, self.rect)
        elif self.spawn_duration > 0:
            image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))  
            surface.blit(image, self.rect)
        else:
            surface.blit(self.image, self.rect)
            

    def shoot(self, target):
        if self.shoot_delay <= 0:  
            dir_vector = vec(target.rect.centerx - self.rect.centerx, target.rect.centery - self.rect.centery)
            bullet = Bullet(self.rect.centerx, self.rect.centery, 5, dir_vector, 'enemy_bullet.png', player_bullet=False) 
            self.bullets.append(bullet)
            self.shoot_delay = 100
            self.just_shot = True

active_enemies = []
enemy = Enemy(100, 100, 2, 'enemy.png')

# Spawn New Enemies
enemy_count = 1

def spawn_new_enemies(num_enemies):
    if enemy_spawn_sound.get_num_channels() == 0:
        enemy_spawn_sound.play()

    for _ in range(num_enemies):
        new_enemy = Enemy(random.randint(0, screen_width - 50), random.randint(0, screen_height - 50), 2, 'enemy.png')
        active_enemies.append(new_enemy)

start_screen()
spawn_new_enemies(enemy_count)
current_frame = 0

#arrow code
arrow_image = pygame.image.load('arrow.png')
initial_angle = 0 
arrow_image = pygame.transform.rotate(arrow_image, initial_angle)
arrow_width = 25  
arrow_height = 25 
arrow_image = pygame.transform.scale(arrow_image, (arrow_width, arrow_height))
arrow_offset_x = 0 
arrow_offset_y = 0




#game loop
game = True
while game:
    for event in pygame.event.get(): 
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and not P1.is_dying:
                mouse_pos = pygame.mouse.get_pos()
                dir_vector = vec(mouse_pos[0] - P1.rect.centerx, mouse_pos[1] - P1.rect.centery)
                if not paused:
                    player_shot_sound.play()
                    bullet = Bullet(P1.rect.centerx, P1.rect.centery, 10, dir_vector, 'bullet.png', player_bullet=True) 
                    bullets.append(bullet)
                    shooting = True
                    
                else:
                    for button in buttons:
                        if button.is_clicked(mouse_pos):
                            button.action()
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                shooting = False
        elif event.type == KEYDOWN:
            if event.key == K_LSHIFT:
                if P1.can_teleport(current_frame):
                    teleport_sound.play()
                    P1.teleport(current_frame)
            if event.key == K_ESCAPE:
                if paused:
                    pause_off_sound.play()
                else:
                    pause_on_sound.play()
                paused = not paused  
    current_frame += 1
    if paused == True:
        pause_menu()
        pygame.display.flip()
        continue

    bullet_buffer = []

    for bullet in bullets:
        bullet.move()
    
    for bullet in bullets:
        bullet.draw(screen)
        for enemy in active_enemies:
            if bullet.rect.colliderect(enemy.rect) and enemy.spawn_duration <= 0 and not enemy.is_dead:  
                enemy.health -= 50  
                enemy.hit()
                enemy_hurt_sound.play()  
                bullet_buffer.append(bullet)
                if enemy.health <= 0 and not enemy.is_dead:
                    enemy.die() 
                    points += 1
                    score += 1  
                break
    for bullet in bullet_buffer:
        bullets.remove(bullet)  
    mouse_pos = pygame.mouse.get_pos()
    rel_x, rel_y = mouse_pos[0] - P1.rect.centerx, mouse_pos[1] - P1.rect.centery
    angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
    arrow_image_rotated = pygame.transform.rotate(arrow_image, angle)
    radius = 65 
    arrow_pos = (P1.rect.centerx + radius * math.cos(math.radians(-angle)), P1.rect.centery + radius * math.sin(math.radians(-angle)))
    arrow_rect = arrow_image_rotated.get_rect(center=arrow_pos)

    for enemy in active_enemies:
        for bullet in enemy.bullets:
            bullet.move()

        enemy.update(P1.is_dying)
        enemy.draw(screen)

        if enemy.health > 0 and enemy.shoot_delay == 0 and not enemy.is_dead:
            enemy.shoot(P1)
            

        if not active_enemies:
            enemy_count += 1
            spawn_new_enemies(enemy_count)

        if not active_enemies:
            enemy_count += 1
            spawn_new_enemies(enemy_count) 
        
        for enemy in active_enemies:
            for bullet in enemy.bullets:
                if P1.hitbox.colliderect(bullet.rect) and not P1.invincible:
                    P1.health -= 20 
                    player_hurt_sound.play()
                    bullet.remove = True
                    print(P1.health)
                    break
        
        for enemy in active_enemies:
            enemy.bullets = [bullet for bullet in enemy.bullets if not bullet.remove]
        
        if enemy.just_shot:
            enemy_shoot_sound.play()
            enemy.just_shot = False

    if P1.health <= 0:
        enablekeypress_events = False
        if not P1.player_dead():
            P1.invincible = True
            P1.is_dying = True
            if not P1.death_sound_played:
                pygame.mixer.music.stop()
                player_death_sound.play()
                P1.death_sound_played = True
            if P1.current_death_sprite >= len(P1.death_anim):
                P1.is_dying = False

        if not P1.is_dying:
            high_scores.append(score)
            high_scores.sort(reverse=True)
            with open('high_scores.txt', 'w') as f:
                for high_score in high_scores:
                    f.write(str(high_score) + '\n')

            pygame.mixer.music.load(end_music)
            pygame.mixer.music.set_volume(1.3)
            pygame.mixer.music.play(-1)

            if game_over_screen(score):
                P1 = Player()
                P1.death_sound_played = False
                enablekeypress_events = True
                active_enemies.clear()
                enemy = Enemy(100, 100, 2, 'enemy.png')
                enemy_count = 1
                spawn_new_enemies(enemy_count)
                bullets = []
                player_bullet_speed = 5
                SPEED = 5
                point = 0
                score = 0
            else:
                pygame.quit()
                sys.exit()
        
    P1.update()

    screen.fill(white)
    screen.blit(background, (0, 0))
    for bullet in bullets:
        bullet.draw(screen)
    for enemy in active_enemies:
        for bullet in enemy.bullets:
            bullet.draw(screen)
    P1.draw(screen)
    P1.draw_health_hearts(screen)
    
    if P1.health > 0:
        screen.blit(arrow_image_rotated, arrow_rect.topleft) 
    score_text = font.render(f'SCORE: {score}', True, (255, 255, 255)) 
    text_width = score_text.get_width()  
    screen_width = screen.get_width() 
    screen.blit(score_text, ((screen_width - text_width) - 40, 10)) 


    if not P1.can_teleport(current_frame):
        remaining_cooldown = TELEPORT_COOLDOWN - (current_frame - P1.last_teleport_frame)
        draw_cooldown_bar(screen, 80, 100, 150, 15, remaining_cooldown, TELEPORT_COOLDOWN, (80, 80, 255))
        screen.blit(cooldown_icon, (20, 80))

    for enemy in active_enemies:
        if enemy.health > 0 or enemy.is_dead:  
            enemy.draw(screen)
    pygame.display.update()

    FramePerSec.tick(FPS)
