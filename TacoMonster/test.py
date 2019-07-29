from Classes import *
import pygame

pygame.init()

white = (255,255,255)
green = (0, 255, 0)
screen = pygame.display.set_mode((400,400))

def create_text_object(message_to_print, location):
    """
    This function creates a text object to be printed to screen.
    :param message_to_print: A string that will be printed to screen.
    :param location: (x,y) tuple.
    :return: Returns a text object and a text rect. In a list [text_object, text_rect]
    """
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(message_to_print, True, white, green)
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

message = "Score: "
location = (40, 40)
score_object_and_location = create_text_object(message, location)

while True:

    screen.fill(white)
    print_text_to_screen(score_object_and_location[0], score_object_and_location[1])
    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
