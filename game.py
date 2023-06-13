import pygame
from sys import exit
from player import Player
from enemy import Enemy
from rescued_people import RescuedPeeps


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.player = Player(400, 300)
        self.enemy = Enemy(150, 300, 150)
        self.rescuedpeeps = []
        self.setup_prisoners()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def setup_prisoners(self):
        self.rescuedpeeps.append(RescuedPeeps(50, 50, self))
        self.rescuedpeeps.append(RescuedPeeps(50, 200, self))
        self.rescuedpeeps.append(RescuedPeeps(50, 350, self))
        self.rescuedpeeps.append(RescuedPeeps(50, 500, self))

    def increase_enemy_difficulty(self):
        self.enemy.increase_difficulty()

    def update(self):
        peeps_to_remove = []

        if self.player.player_collision_rect.colliderect(self.enemy.enemy_collision_rect):
            # implement your game over logic here
            print("Game over bitch hehehe")

        self.player.update()
        self.enemy.update(self.player.get_position().center)

        for peeps in self.rescuedpeeps:
            if not peeps.visible:
                peeps_to_remove.append(peeps)
            else:
                peeps.update(self.player.get_position())

        for peep in peeps_to_remove:
            self.rescuedpeeps.remove(peep)

    def draw(self):
        self.screen.fill('White')
        self.player.draw(self.screen)
        self.player.draw_collision_box(self.screen)

        self.enemy.draw(self.screen)
        self.enemy.draw_collision_box(self.screen)

        for peeps in self.rescuedpeeps:
            peeps.draw(self.screen)

        pygame.display.update()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
