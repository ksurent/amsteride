import os.path
import pygame
from pygame.locals import *
import random

FPS = 60
WIDTH = 800
HEIGHT = 600


class Loader (dict):
    prefix = 'assets'

    def load_all(self):
        for name in self.names:
            path = os.path.join(self.prefix, name)
            self[name] = self.load(path)


class Images (Loader):
    names = [
        'road.png',
        'shroom-red.png', 'shroom-blue.png',
        'cake-red.png', 'cake-blue.png',
        'biker.01.png', 'biker.02.png',
        'gull.png',
    ]

    def load(self, path):
        return pygame.image.load(path)

image_cache = Images()


class Sounds (Loader):
    names = ['pickup.wav']

    def load(self, path):
        return pygame.mixer.Sound(path)

sound_cache = Sounds()


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def follow(self, target):
        self.x = target.x - int(WIDTH * 0.2)
        self.y = - int(HEIGHT * 0.4)

    def draw(self, obj):
        obj.draw(obj.x - self.x, obj.y - self.y)


class HUD:
    def __init__(self, disp, rider):
        self.disp = disp
        self.rider = rider

    def draw(self):
        if self.rider.is_alive:
            text = "Score: %d" % rider.score
        else:
            text = "YOU SUCK"
        score = FNT_SCORE.render(text, True, (255, 0, 0))
        w, h = score.get_size()
        self.disp.blit(score, (0, HEIGHT - h))


class Rider:
    FRAME_DURATION = 30

    def __init__(self, disp):
        self.disp = disp
        self.x = 0
        self.y = Road.HEIGHT / 2
        self.speed = 5
        self.score = 0
        self.imgs = (image_cache["biker.01.png"], image_cache["biker.02.png"])
        self.frame_idx = 0
        self.frame_dur = 0
        self.img = self.imgs[self.frame_idx]
        self.img_w, self.img_h = self.img.get_size()
        self.is_alive = True

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

    def add_score(self, cost):
        self.score += cost

    def bbox(self):
        return (self.x, self.y - 10 + 5, self.img_w, 10)

    def rect(self):
        return pygame.Rect(self.bbox())

    def update(self):
        self.x += self.speed
        self.frame_dur += 1
        if self.frame_dur == self.FRAME_DURATION:
            self.frame_dur = 0
            self.frame_idx += 1
            self.frame_idx %= len(self.imgs)
            self.img = self.imgs[self.frame_idx]

    def draw(self, screen_x, screen_y):
        self.disp.blit(self.img, (screen_x, screen_y - self.img_h))


class Item (object):
    def __init__(self, disp, x, y):
        self.disp = disp
        self.is_alive = True
        self.x = x
        self.y = y
        self.img = image_cache[self.sprite_name]
        self.img_w, self.img_h = self.img.get_size()

    def bbox(self):
        return (self.x, self.y - 10 + 5, self.img_w, 10)

    def rect(self):
        return pygame.Rect(self.bbox())

    def update(self):
        pass

    def draw(self, screen_x, screen_y):
        if self.is_alive:
            self.disp.blit(self.img, (screen_x, screen_y - self.img_h))

        if screen_x < - self.img_w:
            self.is_alive = False


class Bonus (Item):
    all_sprites = ('cake-red.png', 'cake-blue.png',
                   'shroom-red.png', 'shroom-blue.png')

    def __init__(self, disp, x, y):
        self.sprite_name = random.choice(self.all_sprites)
        super(Bonus, self).__init__(disp, x, y)
        self.cost = 5

    def collide(self, rider):
        if not self.is_alive:
            return
        self.is_alive = False
        rider.add_score(self.cost)
        sound_cache['pickup.wav'].play()


class Obstacle (Item):
    sprite_name = 'gull.png'

    def collide(self, rider):
        rider.is_alive = False


class Road:
    HEIGHT = 300

    def __init__(self, disp):
        self.disp = disp
        self.x = 0
        self.y = 0
        self.img = image_cache["road.png"]
        self.img_w, self.img_h = self.img.get_size()

    def update(self):
        pass

    def draw(self, screen_x, screen_y):
        img = self.img
        w = self.img_w
        self.disp.blit(img, (screen_x % w - w, screen_y))
        self.disp.blit(img, (screen_x % w, screen_y))


class ItemGenerator:
    items = [Bonus, Obstacle]

    def __init__(self, disp):
        self.disp = disp
        self.next_x = 1158

    def gimme_maybe(self, x, from_y, to_y):
        if self.next_x > x:
            return None
        self.next_x = x + 300
        y = random.randint(from_y, to_y)
        return random.choice(self.items)(self.disp, x, y)


pygame.init()

disp = pygame.display.set_mode((WIDTH, HEIGHT))

image_cache.load_all()
sound_cache.load_all()

is_running = True

clock = pygame.time.Clock()

FNT_SCORE = pygame.font.Font(pygame.font.get_default_font(), 12)

camera = Camera()
item_gen = ItemGenerator(disp)
rider = Rider(disp)
road = Road(disp)
items = []
hud = HUD(disp, rider)

while is_running:
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN \
           and event.key == K_ESCAPE:
            is_running = False

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
    if item_maybe is not None:
        items.append(item_maybe)

    road.update()
    rider.update()
    for i in items:
        i.update()
    camera.follow(rider)

    clashed = rider.rect().collidedictall({i.bbox(): i for i in items})
    for _, item in clashed:
        item.collide(rider)

    items = [item for item in items if item.is_alive]

    disp.fill((200, 255, 255))
    camera.draw(road)
    for i in sorted([rider] + items, key=lambda o: o.y):
        camera.draw(i)
    hud.draw()
    pygame.display.update()
    clock.tick(FPS)
