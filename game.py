import pygame
from pygame.locals import *

screen_width = 800
screen_height = 600


class Player(pygame.sprite.Sprite):
    pass


class Crate(pygame.sprite.Sprite):
    pass


def main():
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        pygame.display.update()
        clock.tick(60)


main()
