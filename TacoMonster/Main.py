import pygame, sys
from pygame.locals import *
from Variables import *

"""
Artwork credits:
TacoMonster art by: (http://bevouliin.com)
Backgrounds bg_1 by: Sauer2
"""

# Initialize pygame settings.
pygame.init()
screen = pygame.display.set_mode((screen_size))
background_image = pygame.image.load("background_images/bg_1.png")
clock = pygame.time.Clock()
done = False

# Classes
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

    def getHealth(self):
        return self.health

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

# Initialize sprite settings.
taco_monster = TacoMonster()
taco_monster.rect.x = 50
taco_monster.rect.y = 50

player_list = pygame.sprite.Group()
player_list.add(taco_monster)

# Useful functions to make game easier to read.
def get_player_input():

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: taco_monster.movingUp = True
    if pressed[pygame.K_DOWN]: taco_monster.movingDown = True
    if pressed[pygame.K_LEFT]: taco_monster.movingLeft = True
    if pressed[pygame.K_RIGHT]: taco_monster.movingRight = True

# -------------------Main game loop.-----------------------------
while not done:
# Get user inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    get_player_input()


# Update game state.
    taco_monster.update_taco()

# Draw the game.
    screen.blit(background_image, [0,0])
    player_list.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
# Exit pygame and system.
pygame.quit()
sys.exit()

