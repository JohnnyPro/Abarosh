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
        keys = pygame.key.get_pressed()

        self.__moving_up = keys[pygame.K_w] and self.player_rect.midtop[1] > 0
        self.__moving_left = keys[pygame.K_a] and self.player_rect.midleft[0] > 0
        self.__moving_down = keys[pygame.K_s] and self.player_rect.midbottom[1] < 600
        self.__moving_right = keys[pygame.K_d] and self.player_rect.midright[0] < 800
        self.__moving_fast = self.can_move_fast(keys)

        self.move()

    def can_move_fast(self, keys):
        return (keys[pygame.K_LSHIFT] and keys[pygame.K_w] and self.stamina.max_stamina_point > 0) or (keys[pygame.K_LSHIFT] and keys[pygame.K_a] and self.stamina.max_stamina_point > 0) or (
            keys[pygame.K_LSHIFT] and keys[pygame.K_s] and self.stamina.max_stamina_point > 0) or (keys[pygame.K_LSHIFT] and keys[pygame.K_d] and self.stamina.max_stamina_point > 0)

    def is_shift_pressed(self):
        key = pygame.key.get_pressed()

        return key[pygame.K_LSHIFT]
    def move(self):
        self.__player_speed = 2.8 if not self.__moving_fast else self.__player_running_speed

        if self.__moving_up and not self.__is_colliding:
            self.player_rect.centery = int(self.player_rect.centery - self.__player_speed)

        if self.__moving_down and not self.__is_colliding:
            self.player_rect.centery = int(self.player_rect.centery + self.__player_speed)

        if self.__moving_left and not self.__is_colliding:
            self.player_rect.centerx = int(self.player_rect.centerx - self.__player_speed)

        if self.__moving_right and not self.__is_colliding:
            self.player_rect.centerx = int(self.player_rect.centerx + self.__player_speed)

        if self.__moving_fast and self.stamina.max_stamina_point > 0:
            self.stamina.use_stamina()

        if not self.__moving_fast:
            if self.stamina.max_stamina_point >= self.stamina.regeneration_time_out_factor:
                self.stamina.refill_stamina()
            # elif self.stamina.regeneration_time_out_factor <= self.stamina.max_stamina_point < 0:
            #     self.stamina.use_stamina() # || DOESN'T WORK YET TRY AND MAKE IT WORK ||

    def get_position(self):
        return self.player_rect.center

    def draw(self, screen):
        screen.blit(self.player_surface, self.player_rect)
        self.stamina.create_stamina_bar(screen, 500, 50, 260, 4)
