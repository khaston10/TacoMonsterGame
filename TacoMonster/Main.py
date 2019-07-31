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
        self.health_text_object_and_location = []
        self.shooter = False
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False
        self.image_index = 0
        self.score = 0
        self.score_text_object_and_location = []
        self.lives_left = 3

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

        # Update the taco_monster's score as a text object so that it can be printed to screen.
        self.score_text_object_and_location = create_text_object("Tacos: " + str(self.score), (40, 40))

        # Update the taco_monster's health as a text object so that it can be printed to screen.
        self.health_text_object_and_location = create_text_object("Health " + str(self.health), (40, 80))

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
        if self.shooter == True:
            print("Shoot Bullet.")
            create_bullet(self.rect.right, self.rect.centery)

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
        self.rect.x = random.randint(screen_width, screen_width + 3000)
        self.rect.y = random.randint(0, screen_height - 90)

    def update_hot_sauce(self):
        # Move hot sauce bottle.
        self.rect.x -= self.speed

        # Kill hot sauce if it leaves the screen.
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

class Sushi(pygame.sprite.Sprite):
    """
    This is the class for the sushi sprite. The objects the Taco Monster hates.
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed = random.randint(sushi_speed_min, sushi_speed_max)
        self.image = pygame.image.load("sprite_images/sushi/sushi.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(screen_width, screen_width + 300)
        self.rect.y = random.randint(0 , screen_height -90)

    def update_sushi(self):
        self.rect.x -= self.speed

        # Delete sushi if it leaves screen.
        if self.rect.x < 0:
            all_sprites.remove(self)
            sushi_list.remove(self)
            self.kill()

# Useful functions to make game easier to read.
def get_player_input():
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: taco_monster.movingUp = True
    if pressed[pygame.K_DOWN]: taco_monster.movingDown = True
    if pressed[pygame.K_LEFT]: taco_monster.movingLeft = True
    if pressed[pygame.K_RIGHT]: taco_monster.movingRight = True
    if pressed[pygame.K_SPACE]: taco_monster.shoot()

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
    :return: none
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

def create_sushi():
    """
    Creates sushi at random location.
    """
    sushi = Sushi()
    all_sprites.add(sushi)
    sushi_list.add(sushi)

def create_text_object(message_to_print, location):
    """
    This function creates a text object to be printed to screen.
    :param message_to_print: A string that will be printed to screen.
    :param location: (x,y) tuple.
    :return: Returns a text object and a text rect. In a list [text_object, text_rect]
    """
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(message_to_print, True, White)
    text_rect = text.get_rect()
    text_rect = location

    return [text, text_rect]

def print_text_to_screen(text, text_rect):
    """
    Prints text to screen at the location text_rect.
    :param text: A text object created from the function "create_text_object"
    :param text_rect:  A text object location created from the function "create_text_object"
    :return: none
    """
    screen.blit(text, text_rect)

def play_splash_screen():
    """
    This function plays the splash screen at the beginning of game.
    :return: none
    """
    splash_screen_timer_start = 0
    splash_screen_timer_passed = 0
    splash_screen_animation = []
    for i in range(1, 70):
        splash_screen_animation.append("sprite_images/splash_screen/sp_" + str(i) + ".png")

    screen_animation = Animation(splash_screen_animation, screen_width//2 - 200, screen_height//2 - 200)
    animation_list.add(screen_animation)

    while splash_screen_timer_passed - splash_screen_timer_start < length_of_splash_screen:
        # Get user inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Update Splash Screen.
        splash_screen_timer_passed = pygame.time.get_ticks()
        for animation in animation_list:
            animation.update_animation()
        # Draw to screen.
        screen.fill(Black)
        animation_list.draw(screen)
        pygame.display.flip()
        clock.tick(50)

def play_intro_screen():
    """
    This function plays the intro screen at the beginning of game.
    :return: none
    """
    intro_screen_timer_start = 0
    intro_screen_timer_passed = 0
    intro_image = pygame.image.load("intro_images/IntroScreen.png")

    while intro_screen_timer_passed - intro_screen_timer_start < length_of_intro_screen:
        # Get user inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Update intro screen timer Screen.
        intro_screen_timer_passed = pygame.time.get_ticks()

        # Draw to screen.
        screen.blit(intro_image, [0, 0])
        pygame.display.flip()
        clock.tick(FPS)

def update_level_settings(level):
    """
    Call this function in the update section of the game loop to increase level difficulty.
    :param level: level is an integer
    :return:
    """
    global taco_limit
    global max_number_of_sushi
    global hot_sauce_limit
    global background_image
    global background_images
    global level_number

    taco_limit = level * 2
    max_number_of_sushi = level * 2
    hot_sauce_limit = level * 2
    level_number = level
    background_image = pygame.image.load(background_images[level_number])

def initialize_sprite_settings():
    """
    This function is only used to make the code more streamlined.
    :return: None
    """
    global taco_monster
    global screen_height
    global shooter_timer_start
    global shooter_timer_passed
    global player_list
    global taco_list
    global hot_sauce_hit_list
    global sushi_hit_list
    global animation_list
    global all_sprites
    global list_of_taco_sprites
    global bullet_list
    global hot_sauce_list
    global sushi_list

    taco_monster = TacoMonster()
    taco_monster.rect.x = 50
    taco_monster.rect.y = screen_height // 2
    shooter_timer_start = 0
    shooter_timer_passed = 0

    player_list = pygame.sprite.Group()
    player_list.add(taco_monster)

    taco_list = pygame.sprite.Group()
    hot_sauce_list = pygame.sprite.Group()
    sushi_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()
    animation_list = pygame.sprite.Group()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(taco_monster)

    list_of_taco_sprites = initialize_taco_sprites(taco_limit)

    for taco in list_of_taco_sprites:
        all_sprites.add(taco)
        taco_list.add(taco)

# Initialize sprite settings.
initialize_sprite_settings()

# ----------------Display Splash Screen--------------------------
play_splash_screen()

# ----------------Display Intro Screen--------------------------
play_intro_screen()

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

    # Create new hot sauce if the number of hot sauces on screen is less than the hot_sauce_limit.
    for sauce in hot_sauce_list:
        sauce.update_hot_sauce()
    if len(hot_sauce_list) < hot_sauce_limit:
        create_new_hot_sauce()

    # Spawn sushi if the max number of sushi is not on screen.
    if len(sushi_list) < max_number_of_sushi:
        create_sushi()
    for sushi in sushi_list:
        sushi.update_sushi()



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

    # Detect collisions between bullets and sushi. If collision is detected delete the sushi and bullet
    # then play splat animation.
    for bullet in bullet_list:
        bullet_hit_list = pygame.sprite.spritecollide(bullet, sushi_list, True)
        for hit in bullet_hit_list:
            animation = Animation(splat_animation, bullet.rect.x, bullet.rect.y)
            animation_list.add(animation)
            all_sprites.add(animation)

    # Detect collisions between taco_monster and sushi. Delete sushi when collision
    #  detected and decrease taco_monster health. Also, we want to play an animation at the location of collision.
    sushi_hit_list = pygame.sprite.spritecollide(taco_monster, sushi_list, True)
    for hit in sushi_hit_list:
        animation = Animation(yuck_animation, taco_monster.rect.right, taco_monster.rect.top)
        animation_list.add(animation)
        all_sprites.add(animation)
        taco_monster.health -= 10


    # Check to see if taco_monster has shooting enabled. If it is enabled
    # this checks the time passes and disables shooter after time limit reached.
    if taco_monster.shooter and shooter_timer_passed - shooter_timer_start > shooter_time:
        taco_monster.shooter = False

    # Update animations in progress.
    for animation in animation_list:
        animation.update_animation()

    # Check to see if background image needs to be updated, this is based off of tacos_until_new_background.
    if taco_monster.score == tacos_until_new_background and level_number != 1:
        update_level_settings(1)

    elif taco_monster.score == 2 * tacos_until_new_background and level_number != 2:
        update_level_settings(2)

    elif taco_monster.score == 3 * tacos_until_new_background and level_number != 3:
        update_level_settings(3)

    elif taco_monster.score == 4 * tacos_until_new_background and level_number != 4:
        update_level_settings(4)

    elif taco_monster.score == 5 * tacos_until_new_background and level_number != 5:
        update_level_settings(5)

    elif taco_monster.score == 6 * tacos_until_new_background and level_number != 6:
        print("Need to show end of game congratulations screen.")


# Draw the game.
    screen.blit(background_image, [0, 0])
    print_text_to_screen(taco_monster.score_text_object_and_location[0], taco_monster.score_text_object_and_location[1])
    print_text_to_screen(taco_monster.health_text_object_and_location[0], taco_monster.health_text_object_and_location[1])
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
# Exit pygame and system.
pygame.quit()
sys.exit()

