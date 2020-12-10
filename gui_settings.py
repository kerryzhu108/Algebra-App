import pygame

"""Screen Settings"""
width = 1000
height = 600
fps = 30
clock = pygame.time.Clock()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
font = pygame.font.SysFont('cambria', 20)
