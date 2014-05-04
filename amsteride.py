import pygame
from pygame.locals import *

FPS = 60
WIDTH = 640
HEIGHT = 480


##############################################################################
class Sun:
    def __init__(self, disp):
        self._disp = disp
        self._x = 0
        self._y = 240

    def move(self, step):
        self._y = self._y + step
        if self._y > HEIGHT:
            self._y = HEIGHT
        elif self._y < 0:
            self._y = 0

    def update(self):
        self._x = self._x + 1
        if self._x > WIDTH:
            self._x = 0

    def draw(self):
        pygame.draw.circle(self._disp, (255, 190, 0), (self._x, self._y), 40)


##############################################################################
pygame.init()

disp = pygame.display.set_mode((WIDTH, HEIGHT))

is_running = True

clock = pygame.time.Clock()

sun = Sun(disp)

while is_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            is_running = False
        elif 1:
            # no-op
            pass

    keys = pygame.key.get_pressed()

    if keys[K_UP]:
        sun.move(-1)
    if keys[K_DOWN]:
        sun.move(1)

    sun.update()

    disp.fill(0)
    sun.draw()
    pygame.display.update()
    clock.tick(FPS)
