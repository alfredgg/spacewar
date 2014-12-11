#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

ROTATION_VELOCITY = 25

class Controller(object):
    def __init__(self):
        self.ship = None
        self.rotation = 0

    def keypressed(self, key):
        pass

    def rotate_left(self):
        self.rotation += 1

    def rotate_right(self):
        self.rotation -= 1

    def accelerate(self):
        self.ship.accelerating = not self.ship.accelerating

    def update(self):
        self.ship.orientation += (self.rotation * ROTATION_VELOCITY)

    def keyup(self, key):
        pass


class PlayerController(Controller):
    def __init__(self):
        Controller.__init__(self)
        self.keys = self.get_keys()
        self.keyups = self.get_keyups()

    def keypressed(self, key):
        func = self.keys.get(key, None)
        if func:
            func()

    def get_keys(self):
        pass

    def get_keyups(self):
        pass

    def keyup(self, key):
        func = self.keyups.get(key, None)
        if func:
            func()

class Player1Controller(PlayerController):
    def __init__(self):
        PlayerController.__init__(self)

    def get_keys(self):
        return {
            pygame.K_a: self.rotate_left,
            pygame.K_d: self.rotate_right,
            pygame.K_s: self.accelerate
        }

    def get_keyups(self):
        return {
            pygame.K_d: self.rotate_left,
            pygame.K_a: self.rotate_right,
            pygame.K_s: self.accelerate
        }

class Player2Controller(PlayerController):
    def __init__(self):
        PlayerController.__init__(self)

    def get_keys(self):
        return {
            pygame.K_KP6: self.rotate_left,
            pygame.K_KP4: self.rotate_right
        }

    def get_keyups(self):
        return {
            pygame.K_KP4: self.rotate_left,
            pygame.K_KP6: self.rotate_right
        }

class RobotController(Controller):
    pass