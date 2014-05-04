import pygame
from pygame.locals import *
import random

FPS = 60
WIDTH = 800
HEIGHT = 600


##############################################################################
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = WIDTH
        self.h = HEIGHT

    def follow(self, target):
        self.x = target.x - int(self.w * 0.2)
        self.y = - int(self.h * 0.4)

    def draw(self, obj):
        obj.draw(obj.x - self.x, obj.y - self.y)


##############################################################################
class Rider:
    def __init__(self, disp):
        self.disp = disp
        self.x = 0
        self.y = Road.HEIGHT / 2
        self.speed = 5
        self.img = pygame.image.load("assets/biker.png")
        self.img_w, self.img_h = self.img.get_size()

    def up(self):
        self.y -= 5
        if self.y < 0:
            self.y = 0

    def down(self):
        self.y += 5
        if self.y > Road.HEIGHT:
            self.y = Road.HEIGHT

    def speed_up(self):
        self.speed = 30

    def slow_down(self):
        self.speed = 1

    def normal_speed(self):
        self.speed = 5

    def update(self):
        self.x += self.speed

    def draw(self, screen_x, screen_y):
        self.disp.blit(self.img, (screen_x, screen_y - self.img_h))


##############################################################################
class Item:
    def __init__(self, disp, x, y):
        self.disp = disp
        self.x = x
        self.y = y
        self.img = pygame.image.load("assets/cake.png")
        self.img_w, self.img_h = self.img.get_size()

    def update(self):
        pass

    def draw(self, screen_x, screen_y):
        self.disp.blit(self.img, (screen_x, screen_y - self.img_h))


##############################################################################
class Road:
    HEIGHT = 300

    def __init__(self, disp):
        self.disp = disp
        self.x = 0
        self.y = 0
        self.img = pygame.image.load("assets/road.png")
        self.img_w, self.img_h = self.img.get_size()

    def update(self):
        pass

    def draw(self, screen_x, screen_y):
        self.disp.blit(self.img, (screen_x % self.img_w - self.img_w, screen_y))
        self.disp.blit(self.img, (screen_x % self.img_w, screen_y))


##############################################################################
class ItemGenerator:
    def __init__(self, disp):
        self.disp = disp
        self.next_x = 1158

    def gimme_maybe(self, x, from_y, to_y):
        if self.next_x > x:
            return None
        self.next_x = x + 300
        y = random.randint(from_y, to_y)
        return Item(self.disp, x, y)


##############################################################################
pygame.init()

disp = pygame.display.set_mode((WIDTH, HEIGHT))

is_running = True

clock = pygame.time.Clock()

camera = Camera()
item_gen = ItemGenerator(disp)
rider = Rider(disp)
road = Road(disp)
items = []

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

    rider.normal_speed()
    if keys[K_RIGHT]:
        rider.speed_up()
    if keys[K_LEFT]:
        rider.slow_down()

    item_maybe = item_gen.gimme_maybe(camera.x + WIDTH, 0, Road.HEIGHT)
    if item_maybe != None:
        items.append(item_maybe)

    road.update()
    rider.update()
    for i in items:
        i.update()
    camera.follow(rider)

    disp.fill((200, 255, 255))
    camera.draw(road)
    camera.draw(rider)
    for i in items:
        camera.draw(i)
    pygame.display.update()
    clock.tick(FPS)
