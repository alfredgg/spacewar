#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

class Ship(object):
    def __init__(self, ini_position, path_image, angle=0, points=0):
        self.position = ini_position
        self.angle = angle
        self.image = pygame.image.load(path_image)
        self.points = points

    def draw(self, screen):
        image = pygame.transform.rotate(self.image, self.angle)
        screen.blit(image, self.position)

class SpaceShip1(Ship):
    def __init__(self, ini_position, angle=0, points=0):
        Ship.__init__(self, ini_position, 'pictures/ship1.png', angle, points)


class SpaceShip2(Ship):
    def __init__(self, ini_position, angle=0, points=0):
        Ship.__init__(self, ini_position, 'pictures/ship2.png', angle, points)

class Planet(object):
    pass

class Explosion(object):
    pass

class Bar(object):
    pass

class Gravity(object):
    pass

class Misil(object):
    pass

class Laser(object):
    pass

class Invisivility(object):
    pass
