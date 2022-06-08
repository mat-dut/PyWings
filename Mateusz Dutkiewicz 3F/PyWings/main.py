import pygame
import os
from Background import Background
from Obstacle import Obstacle
from Cloud import Cloud
from Button import Button
import sys
import random
import json

pygame.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

SCORE_FONT = pygame.font.Font("font/pixel_font.ttf", 32)
ESC_FONT = pygame.font.Font("font/pixel_font.ttf", 24)
GAME_END_FONT = SCORE_FONT
END_SCORE_FONT = pygame.font.Font("font/pixel_font.ttf", 22)

pygame.display.set_caption('PyWings')
BG = Background(WIN)
BG_IMAGE = pygame.transform.scale(
    pygame.image.load('images/bg.jpg'), (900, 500))

LOGO = pygame.transform.scale(
    pygame.image.load('images/logo.png'), (772, 170))

SPEAKER_ON = pygame.transform.scale(
    pygame.image.load('images/speaker_on.png'), (65, 50))

SPEAKER_OFF = pygame.transform.scale(
    pygame.image.load('images/speaker_off.png'), (65, 50))

sound_mode = True

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

# DEV mute
# pygame.mixer.Channel(1).stop()
# pygame.mixer.Channel(0).stop()


def play():

    FPS = 60
    VEL = 8

    BORDER = pygame.Rect(WIDTH//2 - 5, 0, 0, HEIGHT)

    PLANE_WIDTH, PLANE_HEIGHT = 100, 60

    PLANE_IMAGE = pygame.image.load(
        os.path.join('images', 'plane.png'))

    PLANE = pygame.transform.scale(
        PLANE_IMAGE, (PLANE_WIDTH, PLANE_HEIGHT))

    ESC = pygame.image.load(os.path.join('images', 'esc_button.png'))

    PLANE_ROTATE_UP = pygame.transform.rotate(PLANE, 15)
    PLANE_ROTATE_DOWN = pygame.transform.rotate(PLANE, -15)

    global highscore
    highscore = 0

    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            data = json.load(f)
            if data['highscore'] != 0:
                highscore = data['highscore']
            else:
                highscore = 0

    def draw_window(plane, score, keys_pressed, clouds):
        # WIN.blit(BG, (0, 0))

        pygame.draw.rect(WIN, (0, 0, 0), BORDER)

        if keys_pressed[pygame.K_UP] and plane.y - VEL > 0:
            WIN.blit(PLANE_ROTATE_UP, plane)
        elif keys_pressed[pygame.K_DOWN] and plane.y + VEL + plane.height < HEIGHT - 15:
            WIN.blit(PLANE_ROTATE_DOWN, plane)
        else:
            WIN.blit(PLANE, plane)

        WIN.blit(score, (10, 10))
        WIN.blit(SCORE_FONT.render(
            f"Najlepszy wynik: {highscore}", 1, 'black'), (10, 40))
        WIN.blit(ESC, (10, 85))

        WIN.blit(ESC_FONT.render('- wyjdz do menu', 1, (0, 0, 0)), (55, 80))

        pygame.display.update()

    def handle_movement(keys_pressed, plane):
        if keys_pressed[pygame.K_LEFT] and plane.x - VEL > 0:
            plane.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and plane.x + VEL + plane.width < BORDER.x:
            plane.x += VEL
        if keys_pressed[pygame.K_UP] and plane.y - VEL > 0:
            plane.y -= VEL
        if keys_pressed[pygame.K_DOWN] and plane.y + VEL + plane.height < HEIGHT - 15:
            plane.y += VEL

        if keys_pressed[pygame.K_ESCAPE]:
            main_menu()

    def main():
        plane = pygame.Rect(100, 100, PLANE_WIDTH, PLANE_HEIGHT)

        if sound_mode:
            pygame.mixer.Channel(0).play(engine, -1)
        else:
            pass

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
                    if sound_mode:
                        pygame.mixer.Channel(2).play(collision)
                    pygame.mixer.Channel(0).stop()

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

        # End screen
        end_screen(score)
    main()


def end_screen(score):
    run = True

    end_score_text = END_SCORE_FONT.render(
        f"Twój wynik: {score}", 1, 'black')
    end_text = GAME_END_FONT.render("Koniec gry!", 1, 'black')
    SPACE = pygame.image.load(os.path.join('images', 'space_button.png'))

    s = pygame.Surface((375, 150))  # the size of your rect
    s.set_alpha(128)                # alpha level
    s.fill((255, 255, 255))
    WIN.blit(s, (WIDTH//2 - end_text.get_width() //
                 2 - 10, HEIGHT-(HEIGHT//1.1)))

    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            data = json.load(f)
            if score > data['highscore']:
                data['highscore'] = score
                with open('data.json', 'w') as f:
                    json.dump(data, f)
    else:
        data = {'highscore': score}
        with open('data.json', 'w') as f:
            json.dump(data, f)

    while run:

        # pygame.draw.rect(WIN, (0, 0, 0, 0.5), score_rect)
        WIN.blit(end_text, (WIDTH//2 - end_text.get_width() //
                 2, HEIGHT-(HEIGHT//1.1)))
        WIN.blit(end_score_text, (WIDTH//2 - end_text.get_width() //
                 2, HEIGHT-(HEIGHT//1.2)))

        WIN.blit(SPACE, (WIDTH//2 - end_text.get_width() //
                 2, HEIGHT-(HEIGHT//1.4)))

        WIN.blit(ESC_FONT.render('- spróbuj jeszcze raz', 1, 'black'), (WIDTH//2 - end_text.get_width() //
                 2 + 70, HEIGHT-(HEIGHT//1.4)-10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.K_ESCAPE:
                run = False
                main_menu()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                run = False
                play()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
                main_menu()

        pygame.display.update()


def main_menu():

    global sound_mode

    pygame.mouse.set_visible(True)

    pygame.mixer.Channel(0).stop()

    if sound_mode:
        SPEAKER_BUTTON = Button(image=SPEAKER_ON, pos=(WIDTH-50, HEIGHT-50),
                                text_input="", font=pygame.font.Font(
            "font/pixel_font.ttf", 32), base_color="#d7fcd4", hovering_color="White")
    else:
        SPEAKER_BUTTON = Button(image=SPEAKER_OFF, pos=(WIDTH-50, HEIGHT-50),
                                text_input="", font=pygame.font.Font(
            "font/pixel_font.ttf", 32), base_color="#d7fcd4", hovering_color="White")

    while True:
        WIN.blit(BG_IMAGE, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_RECT = LOGO.get_rect(center=(WIDTH//2, HEIGHT//2-150))

        PLAY_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("images/Play Rect.png"), (200, 50)), pos=(WIDTH//2, HEIGHT//2),
                             text_input="GRAJ", font=pygame.font.Font(
            "font/pixel_font.ttf", 32), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("images/Quit Rect.png"), (200, 50)), pos=(WIDTH//2, HEIGHT//2+75),
                             text_input="WYJDZ", font=pygame.font.Font(
            "font/pixel_font.ttf", 32), base_color="#d7fcd4", hovering_color="White")

        WIN.blit(LOGO, MENU_RECT)

        for button in [PLAY_BUTTON, SPEAKER_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if SPEAKER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if SPEAKER_BUTTON.image == SPEAKER_ON:
                        SPEAKER_BUTTON.image = SPEAKER_OFF
                        pygame.mixer.Channel(0).stop()
                        pygame.mixer.Channel(1).stop()
                        sound_mode = False
                    else:
                        SPEAKER_BUTTON.image = SPEAKER_ON
                        pygame.mixer.Channel(1).play(
                            music[random.randint(0, 1)])
                        sound_mode = True

                if event.type == SONG_END:
                    pygame.mixer.Channel(1).play(music[random.randint(0, 1)])

        pygame.display.update()


if __name__ == '__main__':
    main_menu()
