import pygame, sys
import random
from pygame.locals import *
from Variables import *

"""
Artwork credits:
TacoMonster art by: (http://bevouliin.com)
Backgrounds bg_1 by: Sauer2
Taco art by: Kevin Haston
Yumm animation by: Kevin Haston
"""

# Initialize pygame settings.
pygame.init()
screen = pygame.display.set_mode((screen_size))
background_image = pygame.image.load("background_images/bg_1.png")
clock = pygame.time.Clock()
done = False

# Classes
class Taco(pygame.sprite.Sprite):
    """
    This is the class for the taco sprite. The objects the Taco Monster eats.
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1, 7):
            img = pygame.image.load("sprite_images/taco/taco_img_" + str(i) + ".png")
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

        # Attributes
        self.speed = random.randint(taco_speed_min, taco_speed_max)
        self.image_index = 0

    def update_taco(self):
        # Moves taco to the left.
        self.rect.x -= self.speed

        # Deal with sprite image.
        self.image_index += 1

        if self.image_index >= len(self.images):
            self.image_index = 0

        self.image = self.images[self.image_index]

        # Check to see if sprite is off screen. If it is, delete it.
        if self.rect.right <= 0:
            taco_list.remove(self)
            all_sprites.remove(self)
            self.kill()

class TacoMonster(pygame.sprite.Sprite):
    """
    This is the class for the player.
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1, 16):
            img = pygame.image.load("sprite_images/taco_monster/taco-" + str(i) + ".png")
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

        # Attributes
        self.health = 100
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False
        self.image_index = 0
        self.score = 0

    def getHealth(self):
        return self.health

    def getScore(self):
        return self.score

    def update_taco(self):
        # Deal with movement.
        if self.movingUp:
            self.moveUp()
        elif self.movingDown:
            self.moveDown()
        elif self.movingLeft:
            self.moveLeft()
        elif self.movingRight:
            self.moveRight()
        # Deal with sprite image. Update using variable time_between_images.
        self.image_index += 1

        if self.image_index >= len(self.images):
            self.image_index = 1

        self.image = self.images[self.image_index]
    def moveLeft(self):
        if self.rect.left >= 0:
            taco_monster.rect.x -= taco_monster_speed
        self.movingLeft = False
    def moveRight(self):
        if self.rect.right < 300:
            taco_monster.rect.x += taco_monster_speed
        self.movingRight = False
    def moveUp(self):
        if self.rect.top >= 0:
            taco_monster.rect.y -= taco_monster_speed
        self.movingUp = False
    def moveDown(self):
        if self.rect.bottom <= screen_height:
            taco_monster.rect.y += taco_monster_speed
        self.movingDown = False

class Animation(pygame.sprite.Sprite):
    """
    This is the class for an animation to play to the screen once.
    """

    def __init__(self, list_of_files, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.list_of_files = list_of_files
        self.x = x
        self.y = y
        self.images = []
        self.image_index = 0
        for file_name in self.list_of_files:
            img = pygame.image.load(file_name)
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def update_animation(self):
        if self.image_index >= len(self.images):
            all_sprites.remove(self)
            animation_list.remove(self)
            self.kill()
        else:
            self.image = self.images[self.image_index]
        self.image_index += 1


# Useful functions to make game easier to read.
def get_player_input():
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: taco_monster.movingUp = True
    if pressed[pygame.K_DOWN]: taco_monster.movingDown = True
    if pressed[pygame.K_LEFT]: taco_monster.movingLeft = True
    if pressed[pygame.K_RIGHT]: taco_monster.movingRight = True

def initialize_taco_sprites(taco_limit):
    """
    This function initializes taco sprites, an instance of the Taco class.
    :param taco_limit: integer that tells the function how many tacos to create.
    :return: a list of sprites that should be added to all_sprites list.
    """
    list_of_tacos = []

    for i in range(taco_limit):
        random_x = random.randint(screen_width, screen_width + 300)
        random_y = random.randint(0, screen_height - 60)
        taco_i = Taco()
        list_of_tacos.append(taco_i)
        taco_i.rect.x = random_x
        taco_i.rect.y = random_y

    return list_of_tacos

def create_new_tacos():
    """
    This function will create new taco at random location to the right of screen.
    :return:  taco sprite
    """
    random_x = random.randint(screen_width, screen_width + 300)
    random_y = random.randint(0, screen_height - 60)
    new_taco = Taco()
    new_taco.rect.x = random_x
    new_taco.rect.y = random_y
    return new_taco


# Initialize sprite settings.
taco_monster = TacoMonster()
taco_monster.rect.x = 50
taco_monster.rect.y = 50

list_of_taco_sprites = initialize_taco_sprites(taco_limit)

player_list = pygame.sprite.Group()
player_list.add(taco_monster)

taco_list = pygame.sprite.Group()
animation_list = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(taco_monster)

for taco in list_of_taco_sprites:
    all_sprites.add(taco)
    taco_list.add(taco)


# -------------------Main game loop.-----------------------------
while not done:
# Get user inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    get_player_input()


# Update game state.
    taco_monster.update_taco()
    for taco in taco_list:
        taco.update_taco()

    # Create new tacos if the number of tacos on screen is less than the taco limit.
    if len(taco_list) < taco_limit:
        temp_taco = create_new_tacos()
        all_sprites.add(temp_taco)
        taco_list.add(temp_taco)
    # Detect collisions between taco_monster and tacos. Delete tacos when collision
    #  detected and increase taco_monster score. Also, we want to play an animation at the location of collision.
    hit_list = pygame.sprite.spritecollide(taco_monster, taco_list, True)
    for hit in hit_list:
        animation = Animation(yumm_animation, taco_monster.rect.right, taco_monster.rect.top)
        animation_list.add(animation)
        all_sprites.add(animation)
        taco_monster.score +=1

    # Update animations in progress.
    for animation in animation_list:
        animation.update_animation()
    print("Score: " + str(taco_monster.score))

# Draw the game.
    screen.blit(background_image, [0, 0])
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
# Exit pygame and system.
pygame.quit()
sys.exit()

