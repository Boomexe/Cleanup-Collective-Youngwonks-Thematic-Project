import pygame
from pygame.locals import *
from sys import exit
import random
import time
import os

pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Youngwonks Hackathon: Social Good & Charity")

# Variables
CWD = os.getcwd()
ASSETS = os.path.join(CWD, 'assets')
SPRITES = os.path.join(ASSETS, 'sprites')
PROPS = os.path.join(SPRITES, 'props')
BOY_IDLE = os.path.join(SPRITES, 'boy', 'idle', 'idle_1.png')
BOY_WALK = os.path.join(SPRITES, 'boy', 'walk')
BEGGAR = os.path.join(SPRITES, 'beggar', 'beggar.png')
TRASH = os.path.join(SPRITES, 'trash')
TRASH_BIN = os.path.join(PROPS, 'trash_bin.png')
BACKGROUND = os.path.join(PROPS, 'background.png')

SOUNDS = os.path.join(ASSETS, 'sounds')
BUTTON_PRESS = pygame.mixer.Sound(os.path.join(SOUNDS, 'button.wav'))
FAIL = pygame.mixer.Sound(os.path.join(SOUNDS, 'fail.wav'))
PICKUP = pygame.mixer.Sound(os.path.join(SOUNDS, 'pickup.wav'))
SUCCESS = pygame.mixer.Sound(os.path.join(SOUNDS, 'success.wav'))
THROW_AWAY = pygame.mixer.Sound(os.path.join(SOUNDS, 'throw_away.wav'))

BOY_DIMENSIONS = 100, 100
BOY_IDLING = pygame.transform.scale(pygame.image.load(BOY_IDLE).convert_alpha(), BOY_DIMENSIONS)
BOY_IDLING = BOY_IDLING.subsurface((0, 0, 50, 90))
BOY_IDLING_INVERTED = pygame.transform.flip(BOY_IDLING, True, False)
BOY_WALKING = []
BOY_WALKING_INVERTED = []
TRASHLIST = []
BEGGAR_LOADED = pygame.transform.scale(pygame.image.load(BEGGAR).convert_alpha(), (75, 75))
TRASH_BIN_LOADED = pygame.transform.scale(pygame.image.load(TRASH_BIN).convert_alpha(), (75, 75))
BACKGROUND_LOADED = pygame.transform.scale(pygame.image.load(BACKGROUND).convert(), (WIDTH, HEIGHT))

for item in os.listdir(BOY_WALK):
    img = pygame.transform.scale(pygame.image.load(os.path.join(BOY_WALK, item)).convert_alpha(), BOY_DIMENSIONS)
    img = img.subsurface((0, 0, 50, 90))
    BOY_WALKING.append(img)
    BOY_WALKING_INVERTED.append(pygame.transform.flip(img, True, False))

for item in os.listdir(TRASH):
    img = pygame.transform.scale(pygame.image.load(os.path.join(TRASH, item)).convert_alpha(), (50, 50))
    TRASHLIST.append(img)

pygame.display.set_icon(pygame.image.load(os.path.join(SPRITES, 'trash', 'banana_peel.png')).convert_alpha())

running = True
fps = 60
fps_clock = pygame.time.Clock()
total_time = 60
time_remaining = total_time

player_inventory = {
    'Trash': 0,
    'Money': 0,
    'Karma': 0
}

trash = []
beggars = []

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255,0)
BLACK = (0, 0, 0)

class Character():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
    
    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Boy():
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.speed_x = 0
        self.speed_y = 0
        self.max_speed = 5
        self.current = BOY_IDLING
        self.frame = 1
        self.direction = 'e'
    
    def draw(self):
        screen.blit(self.current, (self.x, self.y))

        if self.speed_x == 0 and self.speed_y == 0:
            if self.direction == 'e':
                self.current = BOY_IDLING
            
            elif self.direction == 'w':
                self.current = BOY_IDLING_INVERTED
            self.frame = 1
        
        elif self.direction == 'e':
            self.current = BOY_WALKING[self.frame % len(BOY_WALKING)]
            self.frame += 1
        
        elif self.direction == 'w':
            self.current = BOY_WALKING_INVERTED[self.frame % len(BOY_WALKING_INVERTED)]
            self.frame += 1
    
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.speed_x > 0:
            self.direction = 'e'
        
        elif self.speed_x < 0:
            self.direction = 'w'

class Button():
    def __init__(self, text, color, bgcolor, font_size, action, x, y):
        self.font = pygame.font.Font('freesansbold.ttf', font_size)
        self.text = self.font.render(text, True, color, bgcolor)

        self.text_rect = self.text.get_rect()
        self.text_rect.topleft = (x, y)
        self.action = action
    
    def draw(self):
        screen.blit(self.text, self.text_rect)
    
    def on_click(self):
        self.action()


def show_text(msg, x, y, color, font_size):
    font = pygame.font.SysFont('', font_size)
    msg = font.render(msg, True, color)
    screen.blit(msg, (x, y))

def randomizer(numa, numb):
    return random.randint(numa, numb) == numa

def draw_sprites():
    screen.blit(BACKGROUND_LOADED, (0, 0))

    for thing in beggars:
        thing.draw()

    for thing in trash:
        thing.draw()
    
    trash_bin.draw()
    player.draw()

    show_text(f'Money: {player_inventory["Money"]}', 10, 10, WHITE, 32)
    show_text(f'Trash: {player_inventory["Trash"]}', 10, 40, WHITE, 32)
    show_text(f'Karma: {player_inventory["Karma"]}', 10, 70, WHITE, 32)
    show_text(f'Time Remaining: {time_remaining}', 10, 100, WHITE, 32)
    donate_button.draw()

    pygame.display.update()

def donate():
    if player_inventory['Money'] > 10:
        player_inventory['Money'] == 0
        player_inventory['Karma'] += 10

def quit():
    pygame.quit()
    exit()

player = Boy(625, 350)
trash_bin = Character(25, 625, TRASH_BIN_LOADED)
donate_button = Button('Donate All to Charity', WHITE, RED, 16, donate, 10, 130)

start_time = time.perf_counter()

while running == True:
    fps_clock.tick(fps)
    draw_sprites()
    player.move()

    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        
        elif event.type == KEYDOWN:
            if event.key == K_w:
                player.speed_y = -player.max_speed
            
            elif event.key == K_s:
                player.speed_y = player.max_speed
            
            elif event.key == K_a:
                player.speed_x = -player.max_speed
            
            elif event.key == K_d:
                player.speed_x = player.max_speed
            
            elif event.key == K_SPACE:
                for thing in beggars:
                    if player.x in range(thing.x - BOY_DIMENSIONS[0], thing.x + 75) and player.y in range(thing.y - BOY_DIMENSIONS[1], thing.y + 75):
                        if player_inventory['Money'] > 4:
                            time_remaining += player_inventory['Money']//2 * 4
                            player_inventory['Money'] //= 2
                            player_inventory['Karma'] += 5
                            beggars.remove(thing)
                            pygame.mixer.Sound.play(SUCCESS)
                        
                        else:
                            pygame.mixer.Sound.play(FAIL)
                
                for thing in trash:
                    if player.x in range(thing.x - BOY_DIMENSIONS[0], thing.x + 75) and player.y in range(thing.y - BOY_DIMENSIONS[1], thing.y + 75):
                        if player_inventory['Trash'] < 5:
                            trash.remove(thing)
                            player_inventory['Trash'] += 1
                            player_inventory['Karma'] += 1
                            pygame.mixer.Sound.play(PICKUP)
                        else:
                            pygame.mixer.Sound.play(FAIL)
                
                if player.x in range(trash_bin.x - BOY_DIMENSIONS[0], trash_bin.x + 75) and player.y in range(trash_bin.y - BOY_DIMENSIONS[1], trash_bin.y + 75):
                    if player_inventory['Trash'] > 0:
                        player_inventory['Money'] += player_inventory['Trash']
                        player_inventory['Trash'] = 0
                        pygame.mixer.Sound.play(THROW_AWAY)
        
        elif event.type == KEYUP:
            if event.key == K_w or event.key == K_s:
                player.speed_y = 0
            
            elif event.key == K_a or event.key == K_d:
                player.speed_x = 0
        
        elif event.type == MOUSEBUTTONDOWN:
            if donate_button.text_rect.collidepoint(event.pos):
                player_inventory['Karma'] += player_inventory['Money']
                time_remaining += player_inventory['Money'] * 3
                player_inventory['Money'] = 0
                pygame.mixer.Sound.play(BUTTON_PRESS)

    
    if randomizer(0, 2000):
        beggars.append(Character(random.randint(0, WIDTH - 75), random.randint(0, HEIGHT - 75), BEGGAR_LOADED))
    
    if randomizer(0, 250):
        trash.append(Character(random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 50), random.choice(TRASHLIST)))
    
    if time.perf_counter() - start_time > 1:
        time_remaining -= 1
        start_time = time.perf_counter()
    
    if time_remaining < 0 or len(beggars) > 4 or len(trash) > 9:
        running = False

screen.blit(BACKGROUND_LOADED, (0, 0))
show_text(f'Final karma after {total_time} seconds: {player_inventory["Karma"]}', 300, 350, BLUE, 62)

while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
