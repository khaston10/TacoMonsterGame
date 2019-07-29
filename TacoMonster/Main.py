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
hot_sauce_timer_start_time = 0
hot_sauce_time_passed_time = 0
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
        self.images_shooter = []
        for i in range(1, 16):
            img = pygame.image.load("sprite_images/taco_monster/taco-" + str(i) + ".png")
            self.images.append(img)
        for i in range(1, 16):
            img = pygame.image.load("sprite_images/taco_monster/shooter_taco/taco-" + str(i) + ".png")
            self.images_shooter.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

        # Attributes
        self.health = 100
        self.shooter = False
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

        if self.shooter:
            self.image = self.images_shooter[self.image_index]

        else:
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

    def shoot(self):
        if self.shoot == True:
            print("Shoot Bullet.")

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

class HotSauce(pygame.sprite.Sprite):
    """
        This is the class for the hot sauce sprite. The objects the Taco Monster eats.
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprite_images/hot_sauce/hotsaucebottle.png")
        self.rect = self.image.get_rect()
        self.speed = random.randint(hot_sauce_speed_min, hot_sauce_speed_max)
        self.rect.x = random.randint(screen_width, screen_width + 300)
        self.rect.y = random.randint(0, screen_height - 90)

    def update_hot_sauce(self):
        # Move hot sauce bottle.
        self.rect.x -= self.speed

        # Kill hot suace if it leaves the screen.
        if self.rect.right < 0:
            all_sprites.remove(self)
            hot_sauce_list.remove(self)
            self.kill()

class Bullet(pygame.sprite.Sprite):
    """
    This is the class for the taco sprite. The objects the Taco Monster eats.
    """

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = pygame.image.load("sprite_images/bullet/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update_bullet(self):
        self.rect.x += self.speed

        # Delete bullet if it leaves the screen.
        if self.rect.left > screen_width:
            bullet_list.remove(self)
            all_sprites.remove(self)
            bullet.kill()


# Useful functions to make game easier to read.
def get_player_input():
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: taco_monster.movingUp = True
    if pressed[pygame.K_DOWN]: taco_monster.movingDown = True
    if pressed[pygame.K_LEFT]: taco_monster.movingLeft = True
    if pressed[pygame.K_RIGHT]: taco_monster.movingRight = True
    if pressed[pygame.K_SPACE]: create_bullet(taco_monster.rect.x, taco_monster.rect.y)

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

def create_new_hot_sauce():
    """
    This function will create new hotsauce at random location to the right of screen.
    :return:  none
    """
    hot_sauce = HotSauce()
    all_sprites.add(hot_sauce)
    hot_sauce_list.add(hot_sauce)

def create_bullet(x, y):
    """
    Creates a bullet if the max number of bullets are not on screen.
    :param x: creates a bullet at this location, x
    :param y: creates a bullet at this location, x
    :return: none
    """
    if len(bullet_list) < bullet_limit and taco_monster.shooter:
        bullet = Bullet(x, y)
        all_sprites.add(bullet)
        bullet_list.add(bullet)


# Initialize sprite settings.
taco_monster = TacoMonster()
taco_monster.rect.x = 50
taco_monster.rect.y = 50
shooter_timer_start = 0
shooter_timer_passed = 0

list_of_taco_sprites = initialize_taco_sprites(taco_limit)

player_list = pygame.sprite.Group()
player_list.add(taco_monster)

taco_list = pygame.sprite.Group()
hot_sauce_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
animation_list = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(taco_monster)

for taco in list_of_taco_sprites:
    all_sprites.add(taco)
    taco_list.add(taco)

# spawn a hot sauce for testing.
create_new_hot_sauce()
hot_sauce_timer_start_time = pygame.time.get_ticks()

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
    for bullet in bullet_list:
        bullet.update_bullet()
    # Spawn a hot sauce using timer and update current hot sauces on screen.
    for sauce in hot_sauce_list:
        sauce.update_hot_sauce()

    hot_sauce_time_passed_time = pygame.time.get_ticks()
    if hot_sauce_time_passed_time - hot_sauce_timer_start_time > hot_sauce_spawn_time:
        create_new_hot_sauce()
        hot_sauce_timer_start_time = pygame.time.get_ticks()

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

    # Detect collisions between taco_monster and hot sauce bottles. If collision is detected delete the bottle
    # and update the taco_monster to have shoot enabled.
    hot_sauce_hit_list = pygame.sprite.spritecollide(taco_monster, hot_sauce_list, True)
    shooter_timer_passed = pygame.time.get_ticks()
    for hit in hot_sauce_hit_list:
        shooter_timer_passed = pygame.time.get_ticks()
        shooter_timer_start = pygame.time.get_ticks()
        taco_monster.shooter = True
        animation = Animation(pepper_animation, taco_monster.rect.right - 100, taco_monster.rect.y)
        animation_list.add(animation)
        all_sprites.add(animation)

    # Check to see if taco_monster has shooting enabled. If it is enabled
    # this checks the time passes and disables shooter after time limit reached.
    if taco_monster.shooter and shooter_timer_passed - shooter_timer_start > shooter_time:
        taco_monster.shooter = False

    # Update animations in progress.
    for animation in animation_list:
        animation.update_animation()

# Draw the game.
    screen.blit(background_image, [0, 0])
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
# Exit pygame and system.
pygame.quit()
sys.exit()

