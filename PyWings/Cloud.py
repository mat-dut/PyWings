import random
import pygame
import os

spawn_timer = 0
movement_speed = 2
# gap_size = 300

width = 900
height = 500


class Cloud:
    def __init__(self, screen, x_pos=width):
        self.movement_speed = movement_speed
        self.x_pos = x_pos
        self.screen = screen
        self.cloud_image = pygame.image.load(
            os.path.join('images', f'cloud{random.randint(1, 4)}.png'))
        self.cloud_rect = self.cloud_image.get_rect()
        self.cloud_rect.x = self.x_pos

    def draw(self):
        self.cloud = pygame.transform.rotate(
            self.cloud_image, 180)

        # pygame.draw.rect(self.screen, (0, 0, 0), self.upper_rect)
        self.screen.blit(self.cloud, self.cloud_rect)
        # pygame.draw.rect(self.screen, (0, 0, 0), self.lower_rect)

    def update(self):
        self.cloud_rect.move_ip(-movement_speed, 0)
        self.cloud_rect.move_ip(-movement_speed, 0)
