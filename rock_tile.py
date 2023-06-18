import pygame
from common import *

class Rock:
    def __init__(self, pos_x, pos_y) -> None:
        loaded_image = pygame.image.load('assets/rock.png')
        scaled_image = pygame.transform.scale(loaded_image, (152, 152))

        self.rock_surface = scaled_image
        self.rock_rect = self.rock_surface.get_rect(center=(pos_x, pos_y))
        self.rock_collision_rect = setup_collision_box(self.rock_surface, self.rock_rect, 72, 72)

    
    def draw(self, screen):
        screen.blit(self.rock_surface, self.rock_rect)
    
    def draw_collision_box(self, screen):
        pygame.draw.rect(screen, (0,0,0), self.rock_collision_rect, 2)

    def get_position(self):
        return self.rock_collision_rect