import pygame
from common import *

class RescuedPeeps:
    def __init__(self, pos_x, pos_y, game, image_name) -> None:
        loaded_image = pygame.image.load(image_name)
        scaled_image = pygame.transform.scale(loaded_image, (96, 96))
        self.rescued_person_surface = scaled_image

        self.rescued_person_rect = self.rescued_person_surface.get_rect(center=(pos_x, pos_y))
        self.rescued_person_collision_rect = setup_collision_box(self.rescued_person_surface, self.rescued_person_rect)
        self.game = game

        self.visible = True

    def update(self, player_position):
        if self.rescued_person_rect.colliderect(player_position):
            print("I have been saved!!")
            self.visible = False
            self.game.increase_enemy_difficulty()



    def draw(self, screen):
        screen.blit(self.rescued_person_surface, self.rescued_person_rect)

    def draw_collision(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.rescued_person_collision_rect, 2)


    


