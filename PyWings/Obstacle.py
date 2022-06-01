import random
import pygame
import os

spawn_timer = 0
movement_speed = 2.5
x_size = 50
# gap_size = 300
pipes = []

width = 900
height = 500

OBSTACLE_IMAGE = pygame.image.load(
    os.path.join('images', 'pxArt.png'))


class Obstacle:
    def __init__(self, screen, gap_size, x_pos=width):
        self.gap_size = gap_size
        random_height = random.randint(20, height - self.gap_size)
        self.upper_rect = pygame.Rect(x_pos, -5, x_size, random_height)
        self.lower_rect = pygame.Rect(x_pos, random_height + gap_size + 5,
                                      x_size, height - self.upper_rect.height - gap_size)
        self.screen = screen
        self.passed = False

    def draw(self):
        obstacle_top = pygame.transform.rotate(pygame.transform.scale(
            OBSTACLE_IMAGE, (50, self.upper_rect.height)), 180)

        obstacle_bottom = pygame.transform.scale(
            OBSTACLE_IMAGE, (50, self.lower_rect.height))

        # pygame.draw.rect(self.screen, (0, 0, 0), self.upper_rect)
        self.screen.blit(obstacle_top, self.upper_rect)
        # pygame.draw.rect(self.screen, (0, 0, 0), self.lower_rect)
        self.screen.blit(obstacle_bottom, self.lower_rect)

    def collide(self, rect):
        return self.lower_rect.colliderect(rect) or self.upper_rect.colliderect(rect)

    def update(self):
        self.upper_rect.move_ip(-movement_speed, 0)
        self.lower_rect.move_ip(-movement_speed, 0)

    def score(self, plane):
        if not self.passed and plane.colliderect(pygame.Rect(self.upper_rect.x, 0, 1, 1024)):
            self.passed = True
            return True
        return False
