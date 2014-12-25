#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import sound
from physics import coord

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
BAR_BLINKING_AT = 25
BAR_BLINKING_TIME = 3

RATIO_STARS = 0.0005
STAR_SIZE = 2
ACCELERATION = 1
SPACESHIP_SIZE = 25
PLANET_SIZE = 100
MISIL_SIZE = 10

LASER_LENGTH = 150
LASER_WIDTH = 2
LASER_OFFSET = 3
LASER_LIFE = 2
LASER_ENERGY = 3

COLOR_DEBUG = (255, 0, 0)

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
    bckgnd = pygame.Surface(screensize)
    bckgnd.fill((0, 0, 0))
    nstars = int((w * h) * RATIO_STARS)
    for _ in xrange(0, nstars):
        x, y = randint(0, w), randint(0, h)
        pygame.draw.rect(bckgnd, (255, 255, 255), pygame.Rect(x, y, STAR_SIZE, STAR_SIZE))
    if add_bars:
        myfont = pygame.font.SysFont("monospace", FONT_BARS_SIZE, bold=True)
        label = myfont.render("S", 1, (255,255,255))
        bckgnd.blit(label, (BAR_X_1, BAR_Y_S))
        bckgnd.blit(label, (BAR_X_2, BAR_Y_S))
        label = myfont.render("E", 1, (255,255,255))
        bckgnd.blit(label, (BAR_X_1, BAR_Y_E))
        bckgnd.blit(label, (BAR_X_2, BAR_Y_E))
    return bckgnd

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

    def draw_debug(self, screen):
        pos = self.get_center()
        pygame.draw.circle(screen, COLOR_DEBUG, pos, self.radio, 2)
        x, y = self.get_point_to()
        pygame.draw.line(screen, COLOR_DEBUG, pos, (x, y), 2)

    def update(self):
        pass

    def get_center(self):
        x, y = self.images[0].get_size()
        return self.position[0] + x/2, self.position[1] + y/2

    def get_point_to(self, offset=0):
        return coord(self.get_center(), self.radio + offset, self.orientation)

    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

class Ship(GameObject):
    def __init__(self, ini_position, angle=0, add_new_element_function=None, remove_element_function=None):
        GameObject.__init__(self, ini_position, angle, 15, mass=5)
        self.accelerating = False
        self.add_new_element = add_new_element_function
        self.remove_element = remove_element_function
        self.visible = True
        self.energy = SPACESHIP_ENERGY
        self.life = SPACESHIP_LIFE

    def load_sprites(self, img_path, size):
        from controllers import ROTATION_VELOCITY
        image = pygame.image.load(img_path)
        image = pygame.transform.scale(image, (size, size))
        return [self.rot_center(image, v * ROTATION_VELOCITY) for v in xrange(0, 360 / ROTATION_VELOCITY)]

    def update(self):
        self.acceleration = 1 if self.accelerating else 0

    def fire_missile(self):
        pass

    def fire_laser(self):
        if self.energy - LASER_ENERGY < 0:
            return
        self.energy -= LASER_ENERGY
        self.add_new_element(Laser(self))
        s = sound.sound(SOUND_LASER)
        s.play()

    def teleport(self):
        pass

    def change_energy(self, value):
        value *= SPACESHIP_ENERGY_CHANGE
        if self.life + (value*-1) > 5 and (value > 0 or self.energy + value > 5):
            self.energy += value
            self.life += (value*-1)

class SpaceShip1(Ship):
    def __init__(self, ini_position, angle=0, add_new_element_function=None, remove_element_function=None):
        Ship.__init__(self, ini_position, angle,
                      add_new_element_function=add_new_element_function,
                      remove_element_function=remove_element_function)

        global SPACESHIP1_SPRITES
        if SPACESHIP1_SPRITES is None:
            SPACESHIP1_SPRITES = self.load_sprites(SPACESHIP1_FILE, SPACESHIP_SIZE)
        self.images = SPACESHIP1_SPRITES

class SpaceShip2(Ship):
    def __init__(self, ini_position, angle=0, add_new_element_function=None, remove_element_function=None):
        Ship.__init__(self, ini_position, angle, add_new_element_function=add_new_element_function,
                      remove_element_function=remove_element_function)

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
        self.salarm = sound.sound(SOUND_ALARM, play=False)
        self.in_alarm = False
        if left:
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
            if not self.in_alarm:
                self.in_alarm = True
                self.salarm.play(loops=-1)
        elif self.in_alarm:
            self.salarm.stop()
            self.in_alarm = False

class Laser(GameObject):
    def __init__(self, ship):
        GameObject.__init__(self)
        self.life = LASER_LIFE
        self.remove_element = ship.remove_element
        self.orientation = ship.orientation
        self.pos1 = ship.get_point_to(offset=LASER_OFFSET)
        self.pos2 = coord(self.pos1, LASER_LENGTH, self.orientation)

    def draw(self, screen):
        pygame.draw.line(screen, (255, 255, 255), self.pos1, self.pos2, LASER_WIDTH)

    def update(self):
        self.life -= 1
        if not self.life:
            self.remove_element(self)

    def draw_debug(self, screen):
        pass
