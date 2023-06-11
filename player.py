import pygame
from stamina_bar import StaminaBar


class Player:
    def __init__(self, pos_x, pos_y) -> None:
        self.stamina = StaminaBar(100)
        self.player_surface = pygame.Surface((40, 40))
        self.player_surface.fill('Blue')

        self.player_rect = self.player_surface.get_rect(center=(pos_x, pos_y))

        self.__player_speed = 1.5
        # Increase the speed when shift is pressed
        self.__player_running_speed = 6
        self.__is_colliding = False

        # Direction and speed
        self.__moving_up = False
        self.__moving_left = False
        self.__moving_right = False
        self.__moving_down = False
        self.__moving_fast = False

    def update(self):
        self.configure_keys()

        self.__moving_up = self.up_keys and self.player_rect.midtop[1] > 0
        self.__moving_left = self.left_keys and self.player_rect.midleft[0] > 0
        self.__moving_down = self.down_keys and self.player_rect.midbottom[1] < 600
        self.__moving_right = self.right_keys and self.player_rect.midright[0] < 800
        self.__moving_fast = self.can_move_fast()

        self.move()

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

    def move(self):
        self.__player_speed = 2.8 if not self.__moving_fast else self.__player_running_speed

        if self.__moving_up and not self.__is_colliding:
            self.player_rect.centery = int(
                self.player_rect.centery - self.__player_speed)

        if self.__moving_down and not self.__is_colliding:
            self.player_rect.centery = int(
                self.player_rect.centery + self.__player_speed)

        if self.__moving_left and not self.__is_colliding:
            self.player_rect.centerx = int(
                self.player_rect.centerx - self.__player_speed)

        if self.__moving_right and not self.__is_colliding:
            self.player_rect.centerx = int(
                self.player_rect.centerx + self.__player_speed)

        if self.__moving_fast and self.stamina.max_stamina_point > 0:
            self.stamina.use_stamina()

        if not self.__moving_fast:
            if self.stamina.max_stamina_point >= self.stamina.regeneration_time_out_factor:
                self.stamina.refill_stamina()
            # elif self.stamina.regeneration_time_out_factor <= self.stamina.max_stamina_point < 0:
            #     self.stamina.use_stamina() # || DOESN'T WORK YET TRY AND MAKE IT WORK ||

    def get_position(self):
        return self.player_rect

    def draw(self, screen):
        screen.blit(self.player_surface, self.player_rect)
        self.stamina.create_stamina_bar(screen, 500, 50, 260, 4)
