import pygame
import os
from Background import Background
from Obstacle import Obstacle
from Cloud import Cloud
from Button import Button
import sys
import random

pygame.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

SCORE_FONT = pygame.font.Font("font/pixel_font.ttf", 32)

pygame.display.set_caption('PyWings')
BG = Background(WIN)
BG_IMAGE = pygame.transform.scale(
    pygame.image.load('images/bg.jpg'), (900, 500))

pygame.mixer.init()

engine = pygame.mixer.Sound(os.path.join('sounds', 'engine.ogg'))
music = [pygame.mixer.Sound(os.path.join('sounds', 'bg_music1.ogg')), pygame.mixer.Sound(
    os.path.join('sounds', 'bg_music2.ogg'))]

collision = pygame.mixer.Sound(os.path.join('sounds', 'collision.ogg'))
collision.set_volume(0.6)

engine.set_volume(0.2)

for i in range(len(music)):
    music[i].set_volume(0.2)

SONG_END = pygame.USEREVENT+1

pygame.mixer.Channel(1).play(music[random.randint(0, 1)])
pygame.mixer.Channel(1).set_endevent(SONG_END)


def play():

    FPS = 60
    VEL = 8

    BORDER = pygame.Rect(WIDTH//2 - 5, 0, 0, HEIGHT)

    PLANE_WIDTH, PLANE_HEIGHT = 100, 60

    PLANE_IMAGE = pygame.image.load(
        os.path.join('images', 'plane.png'))

    PLANE = pygame.transform.scale(
        PLANE_IMAGE, (PLANE_WIDTH, PLANE_HEIGHT))

    PLANE_ROTATE_UP = pygame.transform.rotate(PLANE, 15)
    PLANE_ROTATE_DOWN = pygame.transform.rotate(PLANE, -15)

    def draw_window(plane, score, keys_pressed, clouds):
        # WIN.blit(BG, (0, 0))

        pygame.draw.rect(WIN, (0, 0, 0), BORDER)

        if keys_pressed[pygame.K_w] and plane.y - VEL > 0:
            WIN.blit(PLANE_ROTATE_UP, plane)
        elif keys_pressed[pygame.K_s] and plane.y + VEL + plane.height < HEIGHT - 15:
            WIN.blit(PLANE_ROTATE_DOWN, plane)
        else:
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

        if keys_pressed[pygame.K_ESCAPE]:
            main_menu()

    def main():
        plane = pygame.Rect(100, 100, PLANE_WIDTH, PLANE_HEIGHT)

        pygame.mixer.Channel(0).play(engine, -1)

        # pygame.mouse.set_visible(False)

        pygame.mouse.set_pos((WIDTH//4, HEIGHT//2))

        clock = pygame.time.Clock()
        run = True
        pipe_spawn_timer = 0
        cloud_spawn_timer = 0

        pipes = []
        clouds = []
        gap_between_pipes = 100
        gap_between_upper_and_lower_pipe = 200
        movement_speed = 10

        score = 0

        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
                if event.type == pygame.K_ESCAPE:
                    run = False
                    main_menu()
                if event.type == pygame.MOUSEMOTION:
                    if event.pos[0] > BORDER.x:
                        plane.x = BORDER.x - plane.width//2
                        plane.y = event.pos[1] - plane.height//2
                    else:
                        plane.move_ip(
                            event.pos[0] - plane.centerx, event.pos[1] - plane.centery)

                if event.type == SONG_END:
                    pygame.mixer.Channel(1).play(music[random.randint(0, 1)])

            BG.update()
            BG.render()

            pipe_spawn_timer += 1
            cloud_spawn_timer += 1

            if pipe_spawn_timer >= gap_between_pipes:  # use different values for distance between pipes
                pipes.append(
                    Obstacle(WIN, gap_between_upper_and_lower_pipe, movement_speed))
                pipe_spawn_timer = 0

            if cloud_spawn_timer >= 75:
                clouds.append(Cloud(WIN))
                cloud_spawn_timer = 0

            for cloud in clouds:
                cloud.draw()
                cloud.update()

            for pipe in pipes:
                pipe.draw()
                pipe.update()

                if pipe.collide(plane):
                    run = False  # reset the game
                    pygame.mixer.Channel(2).play(collision)

            for pipe in pipes:
                if pipe.score(plane):
                    score += 1
                    if gap_between_pipes != 20:
                        gap_between_pipes -= 2
                    if gap_between_upper_and_lower_pipe != plane.height + 20:
                        gap_between_upper_and_lower_pipe -= 2

                    movement_speed += .2

                # first pipe will be leftmost pipe.
            if pipes and pipes[0].upper_rect.right < 0:
                pipes.pop(0)

            keys_pressed = pygame.key.get_pressed()
            handle_movement(keys_pressed, plane)

            score_text = SCORE_FONT.render(
                f"Wynik: {score}", 1, (0, 0, 0))

            draw_window(plane, score_text, keys_pressed, clouds)

        main()
    main()


def main_menu():

    pygame.mouse.set_visible(True)

    pygame.mixer.Channel(0).stop()

    while True:
        WIN.blit(BG_IMAGE, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = pygame.font.Font(
            "font/pixel_font.ttf", 32).render("MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH//2, HEIGHT//2-150))

        PLAY_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("images/Play Rect.png"), (200, 50)), pos=(WIDTH//2, HEIGHT//2),
                             text_input="GRAJ", font=pygame.font.Font(
            "font/pixel_font.ttf", 32), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("images/Options Rect.png"), (200, 50)), pos=(WIDTH//2, HEIGHT//2+75),
                                text_input="OPCJE", font=pygame.font.Font(
            "font/pixel_font.ttf", 32), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("images/Quit Rect.png"), (200, 50)), pos=(WIDTH//2, HEIGHT//2+150),
                             text_input="WYJDZ", font=pygame.font.Font(
            "font/pixel_font.ttf", 32), base_color="#d7fcd4", hovering_color="White")

        WIN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # options()
                    pass
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
            if event.type == SONG_END:
                print('tak')

        pygame.display.update()


if __name__ == '__main__':
    main_menu()
