import pygame, sys
import random
from pygame.locals import *
from Variables import *

"""
Artwork credits:
TacoMonster art by: (http://bevouliin.com)
Backgrounds: Sauer2, Satur9, leyren, Daniel Gregory Benoy from http://opengameart.org
All other art by: Kevin Haston
Music: Zefz from http://opengameart.org
Sound effects: from http://opengameart.org
"""

# Initialize pygame settings.
pygame.init()
screen = pygame.display.set_mode((screen_size))
background_image = pygame.image.load("background_images/bg_1.png")
game_over_image = pygame.image.load(game_over_image_name[0])
game_won_image = pygame.image.load("game_over_screen/game_won.png")
high_score_image = pygame.image.load("Intro_images/IntroScreen.png")
game_over_and_high_score_image = pygame.image.load("game_over_screen/Congratulations.png")
new_high_score_congratulations_image = pygame.image.load("Intro_images/NewHighScoreCongratulations.png")
outline_image = pygame.image.load("intro_images/OutLine.png")
clock = pygame.time.Clock()
done = False

# Initialize sound and music..
splash_screen_sound = pygame.mixer.Sound('sounds/Wav/Hit_00.wav')
hit_taco_sound = pygame.mixer.Sound('sounds/Wav/Hit_00.wav')
hit_hot_sauce_sound = pygame.mixer.Sound('sounds/Wav/Pickup_00.wav')
hit_sushi_sound = pygame.mixer.Sound('sounds/Wav/Hit_03.wav')
shoot_sound = pygame.mixer.Sound('sounds/Wav/Shoot_01.wav')
pygame.mixer.music.load("sounds/music/Epic Intro.mp3")

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
        self.sushi_killed = 0
        self.score_text_object_and_location = []
        self.lives_left = 3

    def getHealth(self):
        return self.health

    def getScore(self):
        return self.score

    def getSushiKilled(self):
        return self.sushi_killed

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
        if self.rect.right < screen_width:
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
            shoot_sound.play()
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

def create_player():
    """
    Creates a player sprite.
    :return: None
    """
    global taco_monster
    taco_monster = TacoMonster()
    taco_monster.rect.x = 60
    taco_monster.rect.y = screen_height // 2 - 10

    all_sprites.add(taco_monster)
    player_list.add(taco_monster)

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

def create_text_object(message_to_print, location, color=White, font_size=32):
    """
    This function creates a text object to be printed to screen.
    :param message_to_print: A string that will be printed to screen.
    :param location: (x,y) tuple.
    :return: Returns a text object and a text rect. In a list [text_object, text_rect]
    """
    font = pygame.font.Font('freesansbold.ttf', font_size)
    text = font.render(message_to_print, True, color)
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
    splash_screen_sound.play()
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

def play_game_over_screen():
    """
    This function kills all sprites on screen, plays the game over screen, and displays player score. Then ends game.
    :return:None
    """
    global all_sprites

    for sprite in all_sprites:
        sprite.kill()

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

    # Delete sprites from game.
    destroy_sprites(taco=True, hot_sauce=True, sushi=True, bullet=False)
    if level == 1:
        level_number = level
        taco_limit = 3
        max_number_of_sushi = 2
        hot_sauce_limit = 1
        background_image = pygame.image.load(background_images[level_number])

    elif level == 2:
        level_number = level
        taco_limit = 4
        max_number_of_sushi = 4
        hot_sauce_limit = 1
        background_image = pygame.image.load(background_images[level_number])

    elif level == 3:
        level_number = level
        taco_limit = 4
        max_number_of_sushi = 6
        hot_sauce_limit = 1
        background_image = pygame.image.load(background_images[level_number])

    elif level == 4:
        level_number = level
        taco_limit = 5
        max_number_of_sushi = 8
        hot_sauce_limit = 2
        background_image = pygame.image.load(background_images[level_number])

    elif level == 5:
        level_number = level
        taco_limit = 5
        max_number_of_sushi = 10
        hot_sauce_limit = 2
        background_image = pygame.image.load(background_images[level_number])

    elif level == 6:
        level_number = level
        taco_limit = 5
        max_number_of_sushi = 12
        hot_sauce_limit = 3
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
    taco_monster.rect.x = 60
    taco_monster.rect.y = screen_height // 2 -10
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

def destroy_sprites(player=False, taco=False, hot_sauce=False, sushi=False, animation=False, bullet = False):
    """
    This function deletes sprites from the appropriate list when the sprite name is set to True.
    :param player: When set to True, player sprite is deleted.
    :param taco: When set to True, taco sprites are deleted.
    :param hot_sauce: When set to True, hot_sauce sprites are deleted.
    :param sushi: When set to True, sushi sprites are deleted.
    :return: None
    """""
    global player_list
    global taco_list
    global hot_sauce_list
    global sushi_list
    global animation_list
    global bullet_list

    if bullet:
        if len(bullet_list) > 0:
            for bullet in bullet_list:
                bullet.kill()

    if hot_sauce:
       if len(hot_sauce_list) > 0:
           for hot_sauce in hot_sauce_list:
               hot_sauce.kill()

    if taco:
       if len(taco_list) > 0:
           for taco in taco_list:
               taco.kill()

    if player:
       if len(player_list) > 0:
           for player in player_list:
               player.kill()

    if sushi:
        if len(sushi_list) > 0:
            for sushi in sushi_list:
                sushi.kill()

    if animation:
        if len(animation_list) > 0:
            for animation in animation_list:
                animation.kill()

def update_FPS_min_and_max():
    """
    This function records the min and max frames per second that actually ran during game play, so the user can see
    them at the end of the game.
    :return: None
    """
    global Min_FPS
    global Max_FPS

    current_fps = int(clock.get_fps())
    if Min_FPS > current_fps:
        Min_FPS = current_fps
    if Max_FPS < current_fps:
        Max_FPS = current_fps

def check_highscore(score_int, player_name):
    """
    This function checks to see if the player has achieved high score.
    If his score was reached it is saved in the txt file.
    :param score: integer, players score.
    :return: True if high score is reached.
    """
    score_string = ""
    if len(str(score_int)) == 1:
        score_string = "00" + str(score_int)
    if len(str(score_int)) == 2:
        score_string = "0" + str(score_int)


    f = open("high_score.txt", "r")
    line_1 = f.readlines(1)
    line_2 = f.readlines(2)
    line_3 = f.readlines(3)
    f.close()

    new_high_score = False
    name_1 = line_1[0][0:3]
    score_1 = line_1[0][4:7]
    name_2 = line_2[0][0:3]
    score_2 = line_2[0][4:7]
    name_3 = line_3[0][0:3]
    score_3 = line_3[0][4:7]

    if score_int >= int(score_1):
        new_high_score = True
        score_3 = score_2
        score_2 = score_1
        score_1 = str(score_string)
        name_3 = name_2
        name_2 = name_1
        name_1 = player_name
    elif score_int >= int(score_2):
        new_high_score = True
        score_3 = score_2
        score_2 = str(score_string)
        name_3 = name_2
        name_2 = player_name
    elif score_int >= int(score_3):
        new_high_score = True
        score_3 = str(score_string)
        name_3 = player_name

    f = open("high_score.txt", "w")
    f.write(name_1 + " " + score_1 + "\n")
    f.write(name_2 + " " + score_2 + "\n")
    f.write(name_3 + " " + score_3 + "\n")
    f.close()

    return new_high_score

def get_highscore(number):
    """
    This function retrieves one of the top three high scores, based upon the number input.
    :param number: integer, which score to retrieve, i.e. number = 1 retrieves the top score.
    :return: list ["nam", "scr"]
    """
    f = open("high_score.txt", "r")
    line_1 = f.readlines(1)
    line_2 = f.readlines(2)
    line_3 = f.readlines(3)
    f.close()

    name_1 = line_1[0][0:3]
    score_1 = line_1[0][4:7]
    name_2 = line_2[0][0:3]
    score_2 = line_2[0][4:7]
    name_3 = line_3[0][0:3]
    score_3 = line_3[0][4:7]

    if number == 1:
        return [name_1, score_1]
    elif number == 2:
        return [name_2, score_2]
    elif number == 3:
        return [name_3, score_3]

# Initialize sprite settings.
initialize_sprite_settings()

# ----------------Display Splash Screen--------------------------
play_splash_screen()

# ----------------Display Intro Screen--------------------------
while high_score_load:

    # Load high score text objects.
    score_1 = get_highscore(1)
    score_2 = get_highscore(2)
    score_3 = get_highscore(3)

    high_score_directions_text_object_and_location = create_text_object\
        ("ENTER NAME: ", [screen_width // 2 - 140, screen_height - 150])

    player_name_text_object_and_location = create_text_object \
        (player_name, [screen_width // 2 + 100, screen_height - 150])

    high_score_text_object_and_location = create_text_object("HIGH SCORE LIST: ",
                                                             [screen_width // 2 - 130, screen_height - 465])

    high_score_1_text_object_and_location = create_text_object(score_1[0] + " " + score_1[1],
                                                               [screen_width // 2 - 50, screen_height - 330])
    high_score_2_text_object_and_location = create_text_object(score_2[0] + " " + score_2[1],
                                                               [screen_width // 2 - 50, screen_height - 260])
    high_score_3_text_object_and_location = create_text_object(score_3[0] + " " + score_3[1],
                                                               [screen_width // 2 - 50, screen_height - 200])
    # Set timers to deal with blinking final score.
    time_start = 0
    time_passed = 0
    display_player_name = False

    pygame.mixer.music.play(-1)

    # Delete sprites from game.

    destroy_sprites(player=True, taco=True, hot_sauce=True, sushi=True, animation=True, bullet=True)

    high_score_load = False
    high_score = True

    while high_score:

        # Get user inputs.

        event = pygame.event.poll()
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)  # Returns the string id of the pressed key.

            if len(key) == 1 and len(player_name) < 3: # This covers all letters and numbers not on numpad.
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    player_name += key.upper()

                else:
                    player_name += key

            elif key == "backspace":
                player_name = player_name[:len(player_name) - 1]

            elif event.key == pygame.K_RETURN and len(player_name) == 3:  # Finished typing.
                break

        player_name_text_object_and_location = create_text_object \
            (player_name, [screen_width // 2 + 100, screen_height - 150], Red)

        time_passed = pygame.time.get_ticks()
        if time_passed - time_start > 500 and not display_player_name:
            time_start = pygame.time.get_ticks()
            time_passed = pygame.time.get_ticks()
            display_player_name = True

        if time_passed - time_start > 500 and display_player_name:
            time_start = pygame.time.get_ticks()
            time_passed = pygame.time.get_ticks()
            display_player_name = False

        # Draw the game.
        screen.blit(high_score_image, [0, 0])

        if display_player_name:
            print_text_to_screen(high_score_directions_text_object_and_location[0],
                                 high_score_directions_text_object_and_location[1])
            print_text_to_screen(player_name_text_object_and_location[0],
                                 player_name_text_object_and_location[1])
        print_text_to_screen(high_score_text_object_and_location[0],
                             high_score_text_object_and_location[1])
        print_text_to_screen(high_score_1_text_object_and_location[0],
                             high_score_1_text_object_and_location[1])
        print_text_to_screen(high_score_2_text_object_and_location[0],
                             high_score_2_text_object_and_location[1])
        print_text_to_screen(high_score_3_text_object_and_location[0],
                             high_score_3_text_object_and_location[1])

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


# -------------------Main game loop.-----------------------------
pygame.mixer.music.stop()  # Stops the music.
pygame.mixer.music.load("sounds/Music/TheLoomingBattle.OGG")
pygame.mixer.music.play(-1)

create_player()

while not done:

    # Get user inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                taco_monster.shoot()
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

    # Set min and max fps variables.
    update_FPS_min_and_max()

    # Create new tacos if the number of tacos on screen is less than the taco limit.
    if len(taco_list) < taco_limit:
        temp_taco = create_new_tacos()
        all_sprites.add(temp_taco)
        taco_list.add(temp_taco)
    # Detect collisions between taco_monster and tacos. Delete tacos when collision
    #  detected and increase taco_monster score. Also, we want to play an animation at the location of collision.
    hit_list = pygame.sprite.spritecollide(taco_monster, taco_list, True)
    for hit in hit_list:
        animation = Animation(yumm_animation, taco_monster.rect.x, taco_monster.rect.y)
        animation_list.add(animation)
        all_sprites.add(animation)
        taco_monster.score += 1
        hit_taco_sound.play()  # Play sound when taco monster hits taco

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
        hit_hot_sauce_sound.play() # Play sound when taco monster hits hot sauce

    # Detect collisions between bullets and sushi. If collision is detected delete the sushi and bullet
    # then play splat animation.
    for bullet in bullet_list:
        bullet_hit_list = pygame.sprite.spritecollide(bullet, sushi_list, True)

        for hit in bullet_hit_list:
            taco_monster.sushi_killed += 1
            animation = Animation(splat_animation, bullet.rect.x, bullet.rect.y)
            animation_list.add(animation)
            all_sprites.add(animation)
            hit_sushi_sound.play()  # Play sound when taco monster hits sushi


    # Detect collisions between taco_monster and sushi. Delete sushi when collision
    #  detected and decrease taco_monster health. Also, we want to play an animation at the location of collision.
    sushi_hit_list = pygame.sprite.spritecollide(taco_monster, sushi_list, True)
    for hit in sushi_hit_list:
        animation = Animation(yuck_animation, taco_monster.rect.x, taco_monster.rect.y)
        animation_list.add(animation)
        all_sprites.add(animation)
        taco_monster.health -= sushi_damage
        hit_sushi_sound.play()  # Play sound when taco monster hits sushi

    # Check to see if taco_monster has shooting enabled. If it is enabled
    # this checks the time passes and disables shooter after time limit reached.
    if taco_monster.shooter and shooter_timer_passed - shooter_timer_start > shooter_time:
        taco_monster.shooter = False

    # Update animations in progress.
    for animation in animation_list:
        animation.update_animation()

    # Check to see if background image needs to be updated, this is based off of tacos_until_new_background.
    if taco_monster.health <= 0:
        new_high_score = check_highscore(taco_monster.score + taco_monster.sushi_killed, player_name)
        if new_high_score:
            game_over_and_new_high_score_load = True
        else:
            game_over_load = True
        done = True

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
        new_high_score = check_highscore(taco_monster.score + taco_monster.sushi_killed, player_name)
        if new_high_score:
            new_high_score_load = True
        else:
            game_won_load = True

        done = True


    # Draw the game.
    screen.blit(background_image, [0, 0])
    print_text_to_screen(taco_monster.score_text_object_and_location[0], taco_monster.score_text_object_and_location[1])
    print_text_to_screen(taco_monster.health_text_object_and_location[0], taco_monster.health_text_object_and_location[1])
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

while game_over_load:

    # Load end of game texts.
    final_taco_text_object_and_location = create_text_object\
        ("TACO SCORE: " + str(taco_monster.score), [screen_width // 2 - 120, screen_height // 2 - 60])

    final_sushi_text_object_and_location = create_text_object\
        ("SUSHI SCORE: " + str(taco_monster.sushi_killed), [screen_width // 2 - 120, screen_height // 2])

    final_score_text_object_and_location = create_text_object ("FINAL SCORE: " +
    str(taco_monster.sushi_killed + taco_monster.score), [screen_width // 2 - 120, screen_height - 100])

    max_fps_text_object_and_location = create_text_object("MAX FPS: " + str(Max_FPS), [0, 0])

    min_fps_text_object_and_location = create_text_object("MIN FPS: " + str(Min_FPS), [0, 60])

    # Delete sprites from game.

    destroy_sprites(player=True, taco=True, hot_sauce=True, sushi=True, animation = True, bullet = True)

    pygame.mixer.music.stop()  # Stops the music.
    pygame.mixer.music.load("sounds/Music/Icy Game Over.mp3")
    pygame.mixer.music.play(1)

    game_over_load = False
    game_over = True

    while game_over:

        # Get user inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False


        # Draw the game.
        screen.blit(game_over_image, [0, 0])
        print_text_to_screen(final_taco_text_object_and_location[0], final_taco_text_object_and_location[1])
        print_text_to_screen(final_sushi_text_object_and_location[0], final_sushi_text_object_and_location[1])
        print_text_to_screen(final_score_text_object_and_location[0], final_score_text_object_and_location[1])
        print_text_to_screen(max_fps_text_object_and_location[0], max_fps_text_object_and_location[1])
        print_text_to_screen(min_fps_text_object_and_location[0], min_fps_text_object_and_location[1])

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

while game_over_and_new_high_score_load:

    # Load high score text objects.
    score_1 = get_highscore(1)
    score_2 = get_highscore(2)
    score_3 = get_highscore(3)

    high_score_1_text_object_and_location = create_text_object(score_1[0] + " " + score_1[1],
                                                               [screen_width // 2 - 50, screen_height - 400], Red2)
    high_score_2_text_object_and_location = create_text_object(score_2[0] + " " + score_2[1],
                                                               [screen_width // 2 - 50, screen_height - 340], Red2)
    high_score_3_text_object_and_location = create_text_object(score_3[0] + " " + score_3[1],
                                                               [screen_width // 2 - 50, screen_height - 280], Red2)

    # Set timers to deal with blinking red outline.
    outline_timer_start = 0
    outline_timer_time_passed = 0
    display_outline = False

    # Delete sprites from game.

    destroy_sprites(player=True, taco=True, hot_sauce=True, sushi=True, animation=True, bullet=True)

    new_high_score_load = False
    new_high_score = True

    pygame.mixer.music.stop()  # Stops the music.
    pygame.mixer.music.load("sounds/Music/Icy Game Over.mp3")
    pygame.mixer.music.play(1)

    while new_high_score:

        # Update the outline_timer_time_passed.
        outline_timer_time_passed = pygame.time.get_ticks()
        if outline_timer_time_passed - outline_timer_start > 500 and not display_outline:
            outline_timer_start = pygame.time.get_ticks()
            outline_timer_time_passed = pygame.time.get_ticks()
            display_outline = True

        if outline_timer_time_passed - outline_timer_start > 500 and display_outline:
            outline_timer_start = pygame.time.get_ticks()
            outline_timer_time_passed = pygame.time.get_ticks()
            display_outline = False

        # Get user inputs.

        event = pygame.event.poll()
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Draw the game.
        screen.blit(game_over_and_high_score_image, [0, 0])
        if display_outline:
            screen.blit(outline_image, [245, 215])
        print_text_to_screen(high_score_1_text_object_and_location[0],
                             high_score_1_text_object_and_location[1])
        print_text_to_screen(high_score_2_text_object_and_location[0],
                             high_score_2_text_object_and_location[1])
        print_text_to_screen(high_score_3_text_object_and_location[0],
                             high_score_3_text_object_and_location[1])

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

while game_won_load:

    # Load end of game texts.
    final_taco_text_object_and_location = create_text_object\
        ("TACO SCORE: " + str(taco_monster.score), [screen_width // 2 - 120, screen_height // 2 - 60])

    final_sushi_text_object_and_location = create_text_object\
        ("SUSHI SCORE: " + str(taco_monster.sushi_killed), [screen_width // 2 - 120, screen_height // 2])

    final_score_text_object_and_location = create_text_object ("FINAL SCORE: " +
    str(taco_monster.sushi_killed + taco_monster.score), [screen_width // 2 - 120, screen_height - 250], Red2)

    max_fps_text_object_and_location = create_text_object("MAX FPS: " + str(Max_FPS), [0, 0])

    min_fps_text_object_and_location = create_text_object("MIN FPS: " + str(Min_FPS), [0, 60])

    # Delete sprites from game.

    destroy_sprites(player=True, taco=True, hot_sauce=True, sushi=True, animation = True, bullet = True)

    game_won_load = False
    game_won = True

    pygame.mixer.music.stop()  # Stops the music.
    pygame.mixer.music.load("sounds/Music/Icy Game Over.mp3")
    pygame.mixer.music.play(1)

    while game_won:

        # Get user inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_won = False


        # Draw the game.
        screen.blit(game_won_image, [0, 0])
        print_text_to_screen(final_taco_text_object_and_location[0], final_taco_text_object_and_location[1])
        print_text_to_screen(final_sushi_text_object_and_location[0], final_sushi_text_object_and_location[1])
        print_text_to_screen(final_score_text_object_and_location[0], final_score_text_object_and_location[1])
        print_text_to_screen(max_fps_text_object_and_location[0], max_fps_text_object_and_location[1])
        print_text_to_screen(min_fps_text_object_and_location[0], min_fps_text_object_and_location[1])

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

while new_high_score_load:

    # Load high score text objects.
    score_1 = get_highscore(1)
    score_2 = get_highscore(2)
    score_3 = get_highscore(3)

    high_score_1_text_object_and_location = create_text_object(score_1[0] + " " + score_1[1],
                                                               [screen_width // 2 - 50, screen_height - 400], Red2)
    high_score_2_text_object_and_location = create_text_object(score_2[0] + " " + score_2[1],
                                                               [screen_width // 2 - 50, screen_height - 340], Red2)
    high_score_3_text_object_and_location = create_text_object(score_3[0] + " " + score_3[1],
                                                               [screen_width // 2 - 50, screen_height - 280], Red2)

    # Set timers to deal with blinking red outline.
    outline_timer_start = 0
    outline_timer_time_passed = 0
    display_outline = False

    # Delete sprites from game.

    destroy_sprites(player=True, taco=True, hot_sauce=True, sushi=True, animation=True, bullet=True)

    new_high_score_load = False
    new_high_score = True

    pygame.mixer.music.stop()  # Stops the music.
    pygame.mixer.music.load("sounds/Music/high_score.mp3")
    pygame.mixer.music.play(1)

    while new_high_score:

        # Update the outline_timer_time_passed.
        outline_timer_time_passed = pygame.time.get_ticks()
        if outline_timer_time_passed - outline_timer_start > 500 and not display_outline:
            outline_timer_start = pygame.time.get_ticks()
            outline_timer_time_passed = pygame.time.get_ticks()
            display_outline = True

        if outline_timer_time_passed - outline_timer_start > 500 and display_outline:
            outline_timer_start = pygame.time.get_ticks()
            outline_timer_time_passed = pygame.time.get_ticks()
            display_outline = False

        # Get user inputs.

        event = pygame.event.poll()
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Draw the game.
        screen.blit(new_high_score_congratulations_image, [0, 0])
        if display_outline:
            screen.blit(outline_image, [245, 215])
        print_text_to_screen(high_score_1_text_object_and_location[0],
                             high_score_1_text_object_and_location[1])
        print_text_to_screen(high_score_2_text_object_and_location[0],
                             high_score_2_text_object_and_location[1])
        print_text_to_screen(high_score_3_text_object_and_location[0],
                             high_score_3_text_object_and_location[1])

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

# Exit pygame and system.
pygame.quit()
sys.exit()

