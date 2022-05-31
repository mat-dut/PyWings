import pygame
import os
from bg import Background

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Wings')

# Sounds
###

FPS = 60
VEL = 3

PLANE_WIDTH, PLANE_HEIGHT = 100, 60

PLANE_IMAGE = pygame.image.load(
    os.path.join('images', 'plane.png'))

PLANE = pygame.transform.scale(
    PLANE_IMAGE, (PLANE_WIDTH, PLANE_HEIGHT))

BG = Background(WIN)


def draw_window(plane):
    # WIN.blit(BG, (0, 0))

    WIN.blit(PLANE, plane)

    pygame.display.update()


def handle_movement(keys_pressed, plane):
    if keys_pressed[pygame.K_a] and plane.x - VEL > 0:
        plane.x -= VEL
    if keys_pressed[pygame.K_d] and plane.x + VEL + plane.width < WIDTH:
        plane.x += VEL
    if keys_pressed[pygame.K_w] and plane.y - VEL > 0:
        plane.y -= VEL
    if keys_pressed[pygame.K_s] and plane.y + VEL + plane.height < HEIGHT - 15:
        plane.y += VEL


def main():
    plane = pygame.Rect(100, 100, PLANE_WIDTH, PLANE_HEIGHT)

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        BG.update()
        BG.render()

        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, plane)

        draw_window(plane)

    main()


if __name__ == '__main__':
    main()
