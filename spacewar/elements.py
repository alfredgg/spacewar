#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

SPACESHIP1_FILE = 'pictures/ship1.png'
SPACESHIP2_FILE = 'pictures/ship2.png'
PLANET_FILE = 'pictures/planet.png'
TITLE_FILE = 'pictures/title.png'

FONT_BARS_SIZE = 25
BAR_X_1 = 42
BAR_X_2 = 588
BAR_Y_E = 432
BAR_Y_S = 408
BAR_TEXT_MARGIN_X = 20
BAR_TEXT_MARGIN_Y = 12
BAR_WIDTH = 2
BAR_BLINKING_AT = 15
BAR_BLINKING_TIME = 3

RATIO_STARS = 0.0005
STAR_SIZE = 2
ACCELERATION = 1
SPACESHIP_SIZE = 25
PLANET_SIZE = 100
MISIL_SIZE = 10

SPACESHIP1_SPRITES = None
SPACESHIP2_SPRITES = None
MISSILE_SPRITES = None
SPACESHIP_ENERGY = 100
SPACESHIP_LIFE = 100
SPACESHIP_ENERGY_CHANGE = 3

SOUND_ALARM = 'alarm'
SOUND_EXPLOSION = 'explosion'
SOUND_IMPACT = 'impact'
SOUND_LASER = 'laser'
SOUND_MISSILE = 'missile'
SOUND_TELEPORT = 'teleport'

def background(screensize, add_bars=False):
    from random import randint
    w, h = screensize[0], screensize[1]
    background = pygame.Surface(screensize)
    background.fill((0, 0, 0))
    nstars = int((w * h) * RATIO_STARS)
    for _ in xrange(0, nstars):
        x, y = randint(0, w), randint(0, h)
        pygame.draw.rect(background, (255, 255, 255), pygame.Rect(x, y, STAR_SIZE, STAR_SIZE))
    if add_bars:
        myfont = pygame.font.SysFont("monospace", FONT_BARS_SIZE, bold=True)
        label = myfont.render("S", 1, (255,255,255))
        background.blit(label, (BAR_X_1, BAR_Y_S))
        background.blit(label, (BAR_X_2, BAR_Y_S))
        label = myfont.render("E", 1, (255,255,255))
        background.blit(label, (BAR_X_1, BAR_Y_E))
        background.blit(label, (BAR_X_2, BAR_Y_E))
    return background

class GameObject(object):
    def __init__(self, ini_position=(0,0), angle=0, radio=0, mass=1, image_path=None, image_size=100):
        self.position = ini_position
        self.orientation = angle
        self.radio = radio
        self.acceleration = 0
        self.velocity = 0
        self.images = [pygame.transform.scale(pygame.image.load(image_path), (image_size, image_size))] if image_path else None
        self.visible = self.images is not None
        self.mass = mass
        self.body = None

    def draw(self, screen):
        if not self.visible or self.images is None:
            return
        idx = (self.orientation * len(self.images)) / 360
        image = self.images[idx] if self.orientation else self.images[0]
        screen.blit(image, self.position)

    def update(self):
        pass

class Ship(GameObject):
    def __init__(self, ini_position, angle=0, add_new_element_function=None):
        GameObject.__init__(self, ini_position, angle, 10, mass=5)
        self.accelerating = False
        self.add_new_element = add_new_element_function
        self.visible = True
        self.energy = SPACESHIP_ENERGY
        self.life = SPACESHIP_LIFE

    def load_sprites(self, img_path, size):
        from controllers import ROTATION_VELOCITY
        image  = pygame.image.load(img_path)
        image = pygame.transform.scale(image, (size, size))
        return [pygame.transform.rotate(image, v * ROTATION_VELOCITY) for v in xrange(0, 360 / ROTATION_VELOCITY)]

    def update(self):
        self.acceleration = 1 if self.accelerating else 0

    def fire_missile(self):
        pass

    def fire_laser(self):
        pass

    def teleport(self):
        pass

    def change_energy(self, value):
        value *= SPACESHIP_ENERGY_CHANGE
        if self.life + (value*-1) > 5 and self.energy + (value) > 5:
            self.energy += value
            self.life += (value*-1)

class SpaceShip1(Ship):
    def __init__(self, ini_position, angle=0, add_new_element_function=None):
        Ship.__init__(self, ini_position, angle, add_new_element_function=add_new_element_function)

        global SPACESHIP1_SPRITES
        if SPACESHIP1_SPRITES is None:
            SPACESHIP1_SPRITES = self.load_sprites(SPACESHIP1_FILE, SPACESHIP_SIZE)
        self.images = SPACESHIP1_SPRITES

class SpaceShip2(Ship):
    def __init__(self, ini_position, angle=0, add_new_element_function=None):
        Ship.__init__(self, ini_position, angle, add_new_element_function=add_new_element_function)

        global SPACESHIP2_SPRITES
        if SPACESHIP2_SPRITES is None:
            SPACESHIP2_SPRITES = self.load_sprites(SPACESHIP2_FILE, SPACESHIP_SIZE)
        self.images = SPACESHIP2_SPRITES

class Planet(GameObject):
    def __init__(self, ini_position):
        GameObject.__init__(self, ini_position, 0, 30, mass=300, image_path=PLANET_FILE, image_size=PLANET_SIZE)

class Missile(GameObject):
    def __init__(self, position, rotation):
        GameObject.__init__(self, position, rotation)

class Bar(object):
    def __init__(self, spaceship, left=True):
        self.ship = spaceship
        self.position = (0,0)
        self.left = left
        self.blink_time = 0
        self.blink_visible = True
        if (left):
            self.s_position = (BAR_X_1 + BAR_TEXT_MARGIN_X, BAR_Y_S + BAR_TEXT_MARGIN_Y)
            self.e_position = (BAR_X_1 + BAR_TEXT_MARGIN_X, BAR_Y_E + BAR_TEXT_MARGIN_Y)
        else:
            self.s_position = (BAR_X_2 - BAR_TEXT_MARGIN_X/2, BAR_Y_S + BAR_TEXT_MARGIN_Y)
            self.e_position = (BAR_X_2 - BAR_TEXT_MARGIN_X/2, BAR_Y_E + BAR_TEXT_MARGIN_Y)

    def draw(self, screen):
        if self.ship.life < BAR_BLINKING_AT:
            if not self.blink_visible:
                return
        self.draw_bars(screen)

    def draw_bars(self, screen):
        if self.left:
            end_x_s = self.s_position[0] + self.ship.life
            end_x_e = self.e_position[0] + self.ship.energy
        else:
            end_x_s = self.s_position[0] - self.ship.life
            end_x_e = self.e_position[0] - self.ship.energy
        pygame.draw.line(screen, (255, 255, 255), self.s_position, (end_x_s, self.s_position[1]), BAR_WIDTH)
        pygame.draw.line(screen, (255, 255, 255), self.e_position, (end_x_e, self.e_position[1]), BAR_WIDTH)

    def update(self):
        if BAR_BLINKING_AT > self.ship.life:
            self.blink_time -= 1
            if self.blink_time < 0:
                self.blink_time = BAR_BLINKING_TIME
                self.blink_visible = not self.blink_visible

class Laser(GameObject):
    pass
