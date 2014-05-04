import pygame
from pygame.locals import *

FPS = 60
WIDTH = 640
HEIGHT = 480


##############################################################################
class Rider:
    def __init__(self, disp):
        self._disp = disp
        self._x = 0
        self._y = 240
        self._speed = 100

    def up(self):
        self._y -= 1
        if self._y < 0:
            self._y = 0

    def down(self):
        self._y += 1
        if self._y > HEIGHT:
            self._y = HEIGHT

    def speed_up(self):
        self._speed = 120

    def slow_down(self):
        self._speed = 80

    def update(self):
        self._x += self._speed

    def draw(self):
        pygame.draw.circle(self._disp, (255, 190, 0), (600, self._y), 40)


##############################################################################
class Road:
    def __init__(self, disp):
        self._disp = disp
        self._img = pygame.image.load("assets/road.png")

    def update(self):
        pass

    def draw(self):
        self._disp.blit(self._img, (100, 100))


##############################################################################
pygame.init()

disp = pygame.display.set_mode((WIDTH, HEIGHT))

is_running = True

clock = pygame.time.Clock()

rider = Rider(disp)
road = Road(disp)

while is_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            is_running = False
        elif 1:
            # no-op
            pass

    keys = pygame.key.get_pressed()

    if keys[K_UP]:
        rider.up()
    if keys[K_DOWN]:
        rider.down()
    if keys[K_RIGHT]:
        rider.speed_up()
    if keys[K_LEFT]:
        rider.slow_down()

    road.update()
    rider.update()

    disp.fill(0)
    road.draw()
    rider.draw()
    pygame.display.update()
    clock.tick(FPS)
