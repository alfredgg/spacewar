#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

ACCELERATION = 1

class GameObject(object):
    def __init__(self, ini_position, angle, radio, mass=1, image_path=None):
        self.position = ini_position
        self.orientation = angle
        self.radio = radio
        self.acceleration = 0
        self.velocity = 0
        self.image = pygame.image.load(image_path) if image_path else None
        self.visible = self.image is not None
        self.mass = mass
        self.body = None

    def draw(self, screen):
        if self.visible:
            image = pygame.transform.rotate(self.image, self.orientation)
            screen.blit(image, self.position)

    def update(self):
        pass

class Ship(GameObject):
    def __init__(self, ini_position, image_path, angle=0, points=0, energy=50, life=50, add_new_element_function=None):
        GameObject.__init__(self, ini_position, angle, 10, mass=5, image_path=image_path)
        self.points = points
        self.energy = energy
        self.life = life
        self.accelerating = False
        self.add_new_element = add_new_element_function

    def update(self):
        self.acceleration = 1 if self.accelerating else 0

class SpaceShip1(Ship):
    def __init__(self, ini_position, angle=0, points=50, add_new_element_function=None):
        Ship.__init__(self, ini_position, 'pictures/ship1.png', angle, points, add_new_element_function=add_new_element_function)


class SpaceShip2(Ship):
    def __init__(self, ini_position, angle=0, points=50, add_new_element_function=None):
        Ship.__init__(self, ini_position, 'pictures/ship2.png', angle, points, add_new_element_function=add_new_element_function)

class Planet(GameObject):
    def __init__(self, ini_position):
        GameObject.__init__(self, ini_position, 0, 30, mass=300, image_path='pictures/planet.png')

class Explosion(object):
    pass

class Bar(object):
    pass

class Missil(GameObject):
    pass

class Laser(GameObject):
    pass
