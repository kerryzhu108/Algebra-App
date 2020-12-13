import pygame
pygame.init()

"""Screen Settings"""
width = 1000
height = 600
fps = 30
clock = pygame.time.Clock()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
font = pygame.font.SysFont('cambria', 20)
number_font = pygame.font.SysFont('freesansbold.ttf', 42)

"""Colors"""
black = (0, 0, 0)
grey = (48, 48, 48)
light_grey = (90, 90, 90)
white = (255, 255, 255)
green = (0, 255, 0)

