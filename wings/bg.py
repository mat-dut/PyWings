import pygame


class Background():
    def __init__(self, WIN):
        self.bgimage = pygame.transform.scale(
            pygame.image.load('images/bg.jpg'), (900, 500))
        self.bgimage_flipped = pygame.transform.scale(
            pygame.image.load('images/bg_flipped.jpg'), (900, 500))

        self.rectBGimg = self.bgimage.get_rect()
        self.rectBGimg_flipped = self.bgimage_flipped.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = 0
        self.bgX2 = self.rectBGimg.width

        self.moving_speed = 0.5
        self.WIN = WIN

    def update(self):
        self.bgX1 -= self.moving_speed
        self.bgX2 -= self.moving_speed
        if self.bgX1 <= -self.rectBGimg.width:
            self.bgX1 = self.rectBGimg.width
        if self.bgX2 <= -self.rectBGimg.width:
            self.bgX2 = self.rectBGimg.width

    def render(self):
        self.WIN.blit(self.bgimage, (self.bgX1, self.bgY1))
        self.WIN.blit(self.bgimage_flipped, (self.bgX2, self.bgY2))
