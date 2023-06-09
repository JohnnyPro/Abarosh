import pygame
from stamina_bar import StaminaBar
from common import *


class Player:
    def __init__(self, pos_x, pos_y) -> None:
        self.animation_direction = load_images('kuncho')
        self.image_index = 0
        self.stamina = StaminaBar(100)
        self.player_surface = self.animation_direction["left"][self.image_index]


        self.player_rect = self.player_surface.get_rect(center=(pos_x, pos_y))
        self.player_collision_rect = setup_collision_box(
            self.player_surface, self.player_rect)

        self.__player_speed = 1.5
        # Increase the speed when shift is pressed
        self.__player_running_speed = 6
        self.__is_colliding = False

        # Direction boolean
        self.__moving_up = False
        self.__moving_left = True
        self.__moving_right = False
        self.__moving_down = False

        # Speed boolean
        self.__moving_fast = False

        self.is_moving = True

    def update(self, rock_position):
        self.configure_keys()
        self.image_index = (self.image_index + 0.1) % 2
        self.player_animation()

        self.__moving_up = self.up_keys and self.player_rect.midtop[1] > 70
        self.__moving_left = self.left_keys and self.player_collision_rect.midleft[0] > 10
        self.__moving_down = self.down_keys and self.player_rect.midbottom[1] < 580 
        self.__moving_right = self.right_keys and self.player_collision_rect.midright[
            0] < 780 
        self.__moving_fast = self.can_move_fast()


        if self.colliding_with_rock(rock_position):
            self.is_moving = False 
             # Set the is_moving flag to False when colliding with a rock
        else:
            self.is_moving = True 
        self.move(rock_position)

    def configure_keys(self):
        self.keys = pygame.key.get_pressed()

        self.up_keys = self.keys[pygame.K_UP] or self.keys[pygame.K_w]
        self.left_keys = self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]
        self.down_keys = self.keys[pygame.K_DOWN] or self.keys[pygame.K_s]
        self.right_keys = self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]

    def can_move_fast(self):
        self.configure_keys()
        running_up = self.is_running_in_direction(self.up_keys)
        running_left = self.is_running_in_direction(self.left_keys)
        running_down = self.is_running_in_direction(self.down_keys)
        running_right = self.is_running_in_direction(self.right_keys)
        return running_up or running_left or running_down or running_right

    def is_running_in_direction(self, direction):
        has_sufficient_stamina = self.stamina.max_stamina_point > 0

        return self.is_shift_pressed() and direction and has_sufficient_stamina

    def is_shift_pressed(self):
        key = pygame.key.get_pressed()

        return key[pygame.K_LSHIFT]

    def move(self, rock_position):
        if not self.is_moving:
            if self.__moving_up:
                self.player_rect.centery = int(self.player_rect.centery + 5)
                self.player_collision_rect.centery = int(self.player_collision_rect.centery + 5)

            if self.__moving_down:
                self.player_rect.centery = int(self.player_rect.centery - 5)
                self.player_collision_rect.centery = int(self.player_collision_rect.centery - 5)

            if self.__moving_left:
                self.player_rect.centerx = int(self.player_rect.centerx + 5)
                self.player_collision_rect.centerx = int(self.player_collision_rect.centerx + 5)

            if self.__moving_right:
                self.player_rect.centerx = int(self.player_rect.centerx - 5)
                self.player_collision_rect.centerx = int(self.player_collision_rect.centerx - 5)
            return
        
        self.__player_speed = 2.8 if not self.__moving_fast else self.__player_running_speed

        # Store the player's previous position
        prev_player_rect = self.player_rect.copy()
        prev_collision_rect = self.player_collision_rect.copy()

        if self.__moving_up and not self.__is_colliding:
            self.player_rect.centery = int(self.player_rect.centery - self.__player_speed)
            self.player_collision_rect.centery = int(self.player_collision_rect.centery - self.__player_speed)

        if self.__moving_down and not self.__is_colliding:
            self.player_rect.centery = int(self.player_rect.centery + self.__player_speed)
            self.player_collision_rect.centery = int(self.player_collision_rect.centery + self.__player_speed)

        if self.__moving_left and not self.__is_colliding:
            self.player_rect.centerx = int(self.player_rect.centerx - self.__player_speed)
            self.player_collision_rect.centerx = int(self.player_collision_rect.centerx - self.__player_speed)

        if self.__moving_right and not self.__is_colliding:
            self.player_rect.centerx = int(self.player_rect.centerx + self.__player_speed)
            self.player_collision_rect.centerx = int(self.player_collision_rect.centerx + self.__player_speed)

        if self.colliding_with_rock(rock_position):
            # Reset the player's position to the previous position
            self.deplete_stamina()
            self.player_rect = prev_player_rect
            self.player_collision_rect = prev_collision_rect

        if self.__moving_fast and self.stamina.max_stamina_point > 0:
            self.stamina.use_stamina()

        if not self.__moving_fast:
            if self.stamina.max_stamina_point >= self.stamina.regeneration_time_out_factor:
                self.stamina.refill_stamina()

            # elif self.stamina.regeneration_time_out_factor <= self.stamina.max_stamina_point < 0:
            #     self.stamina.use_stamina() # || DOESN'T WORK YET TRY AND MAKE IT WORK ||

    def get_position(self):
        return self.player_collision_rect

    def deplete_stamina(self):
        self.stamina.deplete_stamina()

    def draw(self, screen):

        screen.blit(self.player_surface, self.player_rect)
        self.stamina.create_stamina_bar(screen, 500, 50, 260, 4)

    def draw_collision_box(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.player_collision_rect, 2)

    def player_animation(self):
        if self.__moving_up:
            self.player_surface = self.animation_direction["up"][int(
                self.image_index)]
        elif self.__moving_down:
            self.player_surface = self.animation_direction["down"][int(
                self.image_index)]
        elif self.__moving_left:
            self.player_surface = self.animation_direction["left"][int(
                self.image_index)]
        elif self.__moving_right:
            self.player_surface = self.animation_direction["right"][int(
                self.image_index)]
    def colliding_with_rock(self, rock_position):
        return self.player_collision_rect.colliderect(rock_position)