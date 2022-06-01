import pygame
import os
from Background import Background
from Obstacle import Obstacle

pygame.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

SCORE_FONT = pygame.font.Font("font/pixel_font.ttf", 32)

pygame.display.set_caption('Wings')

# Sounds
###

FPS = 60
VEL = 3

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 0, HEIGHT)

PLANE_WIDTH, PLANE_HEIGHT = 100, 60

PLANE_IMAGE = pygame.image.load(
    os.path.join('images', 'plane.png'))

PLANE = pygame.transform.scale(
    PLANE_IMAGE, (PLANE_WIDTH, PLANE_HEIGHT))

BG = Background(WIN)


def draw_window(plane, score):
    # WIN.blit(BG, (0, 0))

    pygame.draw.rect(WIN, (0, 0, 0), BORDER)

    WIN.blit(PLANE, plane)
    WIN.blit(score, (10, 10))

    pygame.display.update()


def handle_movement(keys_pressed, plane):
    if keys_pressed[pygame.K_a] and plane.x - VEL > 0:
        plane.x -= VEL
    if keys_pressed[pygame.K_d] and plane.x + VEL + plane.width < BORDER.x:
        plane.x += VEL
    if keys_pressed[pygame.K_w] and plane.y - VEL > 0:
        plane.y -= VEL
    if keys_pressed[pygame.K_s] and plane.y + VEL + plane.height < HEIGHT - 15:
        plane.y += VEL


def main():
    plane = pygame.Rect(100, 100, PLANE_WIDTH, PLANE_HEIGHT)

    pygame.mouse.set_pos((WIDTH//4, HEIGHT//2))

    clock = pygame.time.Clock()
    run = True
    spawn_timer = 0
    pipes = []
    gap_between_pipes = 150
    gap_between_upper_and_lower_pipe = 200

    score = 0

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEMOTION:
                if event.pos[0] > BORDER.x:
                    plane.x = BORDER.x - plane.width//2
                    plane.y = event.pos[1] - plane.height//2
                else:
                    plane.move_ip(
                        event.pos[0] - plane.centerx, event.pos[1] - plane.centery)

        BG.update()
        BG.render()

        spawn_timer += 1

        if spawn_timer >= gap_between_pipes:  # use different values for distance between pipes
            pipes.append(
                Obstacle(WIN, gap_between_upper_and_lower_pipe))
            spawn_timer = 0
        for pipe in pipes:
            pipe.draw()
            pipe.update()

            if pipe.collide(plane):
                run = False  # reset the game

        for pipe in pipes:
            if pipe.score(plane):
                score += 1
                if gap_between_pipes != 20:
                    gap_between_pipes -= 2
                if gap_between_upper_and_lower_pipe != plane.height + 20:
                    gap_between_upper_and_lower_pipe -= 5

            # first pipe will be leftmost pipe.
        if pipes and pipes[0].upper_rect.right < 0:
            pipes.pop(0)

        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, plane)

        score_text = SCORE_FONT.render(
            f"Wynik: {score}", 1, (0, 0, 0))

        draw_window(plane, score_text)

    main()


if __name__ == '__main__':
    main()
