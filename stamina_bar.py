import pygame

class StaminaBar:
    def __init__(self, max_stamina_point) -> None:
        self.total_capable_stamina = max_stamina_point
        self.max_stamina_point = max_stamina_point
        self.total_stamina_point = 1.2
        self.regeneration_time_out_factor = -40

    def create_stamina_bar(self, screen, x, y, width, height):
        stamina_bar_outline = pygame.Surface((width, height))
        screen.blit(stamina_bar_outline, (x, y))
        stamina_remaning_bar = int(self.get_remaining_stamina() * 2.6)

        stamina_remaning_bar = 0 if stamina_remaning_bar <= 0 else stamina_remaning_bar

        stamina_bar = pygame.Surface((stamina_remaning_bar,height))
        stamina_bar.fill('Green')
        screen.blit(stamina_bar,  (x, y))

    def get_remaining_stamina(self):
        return self.max_stamina_point
    
    def use_stamina(self):
        #if the player depletes the stamina bar we will have a time out so that the player won't abuse running
        self.max_stamina_point = max(self.max_stamina_point - self.total_stamina_point, self.regeneration_time_out_factor)

    def refill_stamina(self):
        if self.max_stamina_point < self.total_capable_stamina:
            self.max_stamina_point += 0.3
    