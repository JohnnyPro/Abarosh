import pygame

class RescuedPeeps:
    def __init__(self, pos_x, pos_y, game) -> None:
        self.rescued_person_surface = pygame.Surface((40,40))
        self.rescued_person_surface.fill((0, 123, 0))

        self.rescued_person_rect = self.rescued_person_surface.get_rect(center=(pos_x, pos_y))
        self.game = game

        self.visible = True

    def update(self, player_position):
        posx, posy = self.rescued_person_rect.center

        if self.rescued_person_rect.colliderect(player_position):
            print("I have been saved!!")
            self.visible = False
            self.game.increase_enemy_difficulty()



    def draw(self, screen):
        screen.blit(self.rescued_person_surface, self.rescued_person_rect)


    


