import pygame
from sys import exit
from player import Player
from enemy import Enemy
from rescued_people import RescuedPeeps
from rock_tile import Rock
from state import State


class Game(State):
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.background_image = pygame.image.load('assets/trail1.png')
        self.background_image = pygame.transform.scale(
            self.background_image, (800, 600))
        self.clock = pygame.time.Clock()
        self.player = Player(400, 300)
        self.enemy = Enemy(150, 300, 150)
        self.rock = Rock(250, 300)
        self.rescuedpeeps = []
        self.setup_prisoners()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def setup_prisoners(self):
        self.rescuedpeeps.append(RescuedPeeps(
            50, 150, self, 'assets/sprites/peeps_sprite/Peeps-2.png.png'))
        self.rescuedpeeps.append(RescuedPeeps(
            50, 240, self, 'assets/sprites/peeps_sprite/Peeps-4.png.png'))
        self.rescuedpeeps.append(RescuedPeeps(
            50, 350, self, 'assets/sprites/peeps_sprite/Peeps-3.png.png'))
        self.rescuedpeeps.append(RescuedPeeps(
            50, 440, self, 'assets/sprites/peeps_sprite/Peeps-5.png.png'))

    def increase_enemy_difficulty(self):
        self.enemy.increase_difficulty()

    def update(self):
        peeps_to_remove = []

        if self.player.player_collision_rect.colliderect(self.enemy.enemy_collision_rect):
            # implement your game over logic here
            State.currentPage = "GAMEOVER"

        elif not self.rescuedpeeps:
            print("You won")
            State.currentPage = "GAMEWON"

        if self.enemy.enemy_collision_rect.colliderect(self.rock.rock_collision_rect):
            print("Enemy down I repeat enemy down")

        if self.player.player_collision_rect.colliderect(self.rock.rock_collision_rect):
            self.player.deplete_stamina()
        self.player.update(self.rock.rock_collision_rect)
        self.enemy.update(self.player.get_position().center)

        for peeps in self.rescuedpeeps:
            if not peeps.visible:
                peeps_to_remove.append(peeps)
            else:
                peeps.update(self.player.get_position())

        for peep in peeps_to_remove:
            self.rescuedpeeps.remove(peep)

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        if self.player.get_position().centery > self.rock.get_position().centery:
            self.rock.draw(self.screen)
            self.rock.draw_collision_box(self.screen)
            self.draw_sprites()

        else:
            print("when am i drawn here?")
            self.draw_sprites()
            self.rock.draw(self.screen)
            self.rock.draw_collision_box(self.screen)

        for peeps in self.rescuedpeeps:
            peeps.draw(self.screen)
            peeps.draw_collision(self.screen)

        pygame.display.update()

    def draw_sprites(self):
        if (self.player.get_position().centery > self.enemy.get_enemy_position()[1]):
            self.enemy.draw(self.screen)
            self.enemy.draw_collision_box(self.screen)

            self.player.draw(self.screen)
            self.player.draw_collision_box(self.screen)

        else:
            self.player.draw(self.screen)
            self.player.draw_collision_box(self.screen)

            self.enemy.draw(self.screen)
            self.enemy.draw_collision_box(self.screen)

    def run(self):
        while State.currentPage == "PLAY":
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
