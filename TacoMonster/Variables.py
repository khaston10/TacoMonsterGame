# Colors
Black = (0, 0, 0)
Red = (255, 0, 0)
Red2 = (183, 44, 25)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Yellow = (255, 255, 0)
Orange = (255, 165, 0)
Grey = (192, 192, 192)
White = (255, 255, 255)

# Variables for game.
screen_width = 1000
screen_height = 800
FPS = 25 # Frames per second
Min_FPS = FPS
Max_FPS = FPS
screen_size = (screen_width, screen_height)
length_of_splash_screen = 3000 # 3 seconds
length_of_intro_screen = 5000 # 5 seconds
length_of_game_over_screen = 5000 # 5 seconds
level_number = 0  # Used to streamline the background update.
game_over = False
game_over_load = False
game_won_load = False
game_over_and_new_high_score = False
game_over_and_new_high_score_load = False
game_won = False
high_score_load = True
high_score = False
new_high_score_load = False
new_high_score = False
player_name = ""

# Variables for Taco Monster.
taco_monster_speed = 20
shooter_time = 5000 # 5 seconds

# Variables for bullets.
bullet_speed = 30
bullet_limit = 8

# Variables for Tacos.
taco_limit = 10  # Limit for how many taco sprites can populate the screen.
tacos_until_new_background = 50  # Required tacos to eat to update the background.
taco_speed_max = 10
taco_speed_min = 2

# Setting for hot_sauce.
hot_sauce_speed_max = 10
hot_sauce_speed_min = 2
hot_sauce_limit = 1

# Variables for sushi.
max_number_of_sushi = 0
sushi_speed_max = 20
sushi_speed_min = 2
sushi_damage = 10


# List of animations.
yumm_animation = ["sprite_images/yumm/YUMM_1.png", "sprite_images/yumm/YUMM_2.png",
                  "sprite_images/yumm/YUMM_3.png", "sprite_images/yumm/YUMM_4.png",
                  "sprite_images/yumm/YUMM_5.png", "sprite_images/yumm/YUMM_6.png",
                  "sprite_images/yumm/YUMM_7.png", "sprite_images/yumm/YUMM_8.png"]

pepper_animation = ["sprite_images/pepper/pepper_1.png", "sprite_images/pepper/pepper_2.png",
                    "sprite_images/pepper/pepper_3.png", "sprite_images/pepper/pepper_4.png",
                    "sprite_images/pepper/pepper_5.png", "sprite_images/pepper/pepper_6.png",
                    "sprite_images/pepper/pepper_7.png", "sprite_images/pepper/pepper_8.png",
                    "sprite_images/pepper/pepper_9.png", "sprite_images/pepper/pepper_10.png",
                    "sprite_images/pepper/pepper_11.png", "sprite_images/pepper/pepper_12.png",]

yuck_animation = ["sprite_images/yuck/yuck_1.png", "sprite_images/yuck/yuck_2.png", "sprite_images/yuck/yuck_3.png",
                  "sprite_images/yuck/yuck_4.png", "sprite_images/yuck/yuck_5.png", "sprite_images/yuck/yuck_6.png",
                  "sprite_images/yuck/yuck_7.png", "sprite_images/yuck/yuck_8.png", "sprite_images/yuck/yuck_9.png"]

splat_animation = ["sprite_images/splat/splat_1.png", "sprite_images/splat/splat_2.png", "sprite_images/splat/splat_3.png",
                   "sprite_images/splat/splat_4.png", "sprite_images/splat/splat_5.png", "sprite_images/splat/splat_6.png",
                   "sprite_images/splat/splat_7.png", "sprite_images/splat/splat_8.png", "sprite_images/splat/splat_9.png",
                   "sprite_images/splat/splat_10.png", "sprite_images/splat/splat_11.png", "sprite_images/splat/splat_12.png"]

# List of background images.
background_images = ["background_images/bg_1.png", "background_images/bg_2.png",
                     "background_images/bg_3.png", "background_images/bg_4.png",
                     "background_images/bg_5.png", "background_images/bg_6.png", "game_over_screen/Game_Over.png"]

game_over_image_name = ["game_over_screen/Game_Over.png"]
game_won_image_name = ["game_over_screen/Congratulations.png"]
