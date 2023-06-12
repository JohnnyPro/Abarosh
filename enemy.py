import pygame, math, random
from player import Player
class Enemy:
    def __init__(self, pos_x, pos_y, detection_radius) -> None:
        self.load_images()
        self.image_index = 0
        self.enemy_surface = self.enemy_up_1

        self.enemy_rect = self.enemy_surface.get_rect(center=(pos_x, pos_y))
        self.orignal_enemy_position = self.enemy_rect.center

        self.enemy_speed = 2.2 #gradually increase the enemy speed when it passes different phases (Decrease it if you want it's just fun to use stamina)
        self.direction = "up"

        self.moving_up = True
        self.moving_left = False
        self.moving_right = False
        self.moving_down = False

        self.detection_radius = detection_radius
        self.is_detecting_player = False
        self.player_position = None
        self.timeout = 100
        self.leaving_probability = 0.1 # gradually increase it when the enemy passes different phases

    def load_images(self):
        self.enemy_down_1 = pygame.image.load('./assets/sprites/police_sprite/Police-2.png.png').convert_alpha()
        self.enemy_down_2 = pygame.image.load('./assets/sprites/police_sprite/Police-3.png.png').convert_alpha()
        self.enemy_up_1 = pygame.image.load('./assets/sprites/police_sprite/Police-4.png.png').convert_alpha()
        self.enemy_up_2 = pygame.image.load('./assets/sprites/police_sprite/Police-5.png.png').convert_alpha()
        self.enemy_right_1 = pygame.image.load('./assets/sprites/police_sprite/Police-6.png.png').convert_alpha()
        self.enemy_right_2 = pygame.image.load('./assets/sprites/police_sprite/Police-7.png.png').convert_alpha()
        self.enemy_left_1 = pygame.image.load('./assets/sprites/police_sprite/Police-8.png.png').convert_alpha()
        self.enemy_left_2 = pygame.image.load('./assets/sprites/police_sprite/Police-9.png.png').convert_alpha()

        self.animation_direction  = {
            "up" : [self.enemy_up_1, self.enemy_up_2],
            "down" : [self.enemy_down_1, self.enemy_down_2],
            "left": [self.enemy_left_1, self.enemy_left_2],
            "right": [self.enemy_right_1, self.enemy_right_2]
            }
        self.setup_collision_box()
    
    def setup_collision_box(self):
        self.enemy_down_1 = pygame.transform.scale(self.enemy_down_1, (40,40))
        self.enemy_down_2 = pygame.transform.scale(self.enemy_down_2, (40,40))
        self.enemy_up_1 = pygame.transform.scale(self.enemy_up_1, (40,40))
        self.enemy_up_2 = pygame.transform.scale(self.enemy_up_2, (40,40))
        self.enemy_right_1 = pygame.transform.scale(self.enemy_right_1, (40,40))
        self.enemy_right_2 = pygame.transform.scale(self.enemy_right_2, (40,40))
        self.enemy_left_1 = pygame.transform.scale(self.enemy_left_1, (40,40))
        self.enemy_left_2 = pygame.transform.scale(self.enemy_left_2, (40,40))


    def update(self, player_position):
        
        distance_to_player = math.dist(self.enemy_rect.center, player_position)
        self.is_detecting_player = distance_to_player <= self.detection_radius
        self.image_index = (self.image_index + 0.1) % 2
        self.enemy_animation()

        if self.is_detecting_player:
            enemy_leaves = random.random() < self.leaving_probability 


            if enemy_leaves:
                self.is_detecting_player = False
            else:
                self.move_towards_player(player_position)
        else:
            self.move_up_and_down() #dumb AI here

    def move_towards_player(self, player_position):
        self.go_to_target(player_position)

    def move_up_and_down(self):
        x_distance =  int(abs(self.orignal_enemy_position[0] - self.enemy_rect.centerx))  
        reached_guard_post = x_distance == 0
        if not reached_guard_post:
            if x_distance <= 3:
                self.enemy_rect.centerx = self.orignal_enemy_position[0]
            self.go_to_target(self.orignal_enemy_position)

        else:
            if self.enemy_rect.midtop[1] <= 0:
                self.enemy_rect.centery += self.enemy_speed
                self.direction = "down"
            
            elif self.enemy_rect.midbottom[1] >= 600:
                self.direction = "up"
                self.enemy_rect.centery -= self.enemy_speed

            else:
                if self.direction == "up":
                    self.moving_up = True
                    self.moving_down = False
                    self.enemy_rect.centery -= self.enemy_speed
                
                elif self.direction == "down":
                    self.moving_down = True
                    self.moving_up = False
                    self.enemy_rect.centery += self.enemy_speed



    def go_to_target(self, target_position):
        dx = target_position[0] - self.enemy_rect.centerx
        dy = target_position[1] - self.enemy_rect.centery

        distance = math.hypot(dx, dy)

        if distance > 0:
            direction_x = dx / distance
            direction_y = dy / distance

            self.enemy_rect.centerx += int(direction_x * self.enemy_speed)
            self.enemy_rect.centery += int(direction_y * self.enemy_speed)

   


    def draw(self, screen):
        screen.blit(self.enemy_surface, self.enemy_rect)

    def get_enemy_position(self):
        return self.enemy_rect.center
    

    def increase_difficulty(self):
        self.enemy_speed *= 1.3
        self.leaving_probability /= 2
        self.detection_radius += 25

    def enemy_animation(self):
        if self.moving_up:
            self.enemy_surface = self.animation_direction["up"][int(self.image_index)]
        elif self.moving_down:
            self.enemy_surface = self.animation_direction["down"][int(self.image_index)]

        elif self.moving_left:
            self.enemy_surface = self.animation_direction["left"][int(self.image_index)]

        elif self.moving_right:
            self.enemy_surface = self.animation_direction["right"][int(self.image_index)]
