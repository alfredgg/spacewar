#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

# IT MUST BE 360 % ROTATION_VELOCITY = 0
ROTATION_VELOCITY = 15

class Controller(object):
    def __init__(self):
        self.ship = None
        self.rotation = 0
        self.energy_change = 0

    def keypressed(self, key):
        pass

    def rotate_left(self):
        self.rotation += 1

    def rotate_right(self):
        self.rotation -= 1

    def increase_energy(self):
        self.energy_change += 1

    def decrease_energy(self):
        self.energy_change -= 1

    def accelerate(self):
        self.ship.accelerating = not self.ship.accelerating

    def invisibility(self):
        self.ship.visible = not self.ship.visible

    def update(self):
        self.ship.orientation += (self.rotation * ROTATION_VELOCITY)
        self.ship.orientation %= 360
        self.ship.change_energy(self.energy_change)

    def keyup(self, key):
        pass

    def fire_missile(self):
        self.ship.fire_missile()

    def fire_laser(self):
        self.ship.fire_laser()

    def teleport(self):
        self.ship.teleport()


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
            pygame.K_s: self.accelerate,
            pygame.K_w: self.invisibility,
            pygame.K_q: self.fire_missile,
            pygame.K_e: self.fire_laser,
            pygame.K_x: self.teleport,
            pygame.K_z: self.increase_energy,
            pygame.K_c: self.decrease_energy
        }

    def get_keyups(self):
        return {
            pygame.K_d: self.rotate_left,
            pygame.K_a: self.rotate_right,
            pygame.K_s: self.accelerate,
            pygame.K_w: self.invisibility,
            pygame.K_z: self.decrease_energy,
            pygame.K_c: self.increase_energy
        }

class Player2Controller(PlayerController):
    def __init__(self):
        PlayerController.__init__(self)

    def get_keys(self):
        return {
            pygame.K_KP6: self.rotate_left,
            pygame.K_KP4: self.rotate_right,
            pygame.K_KP1: self.increase_energy,
            pygame.K_KP3: self.decrease_energy
        }

    def get_keyups(self):
        return {
            pygame.K_KP4: self.rotate_left,
            pygame.K_KP6: self.rotate_right,
            pygame.K_KP1: self.decrease_energy,
            pygame.K_KP3: self.increase_energy
        }

class RobotController(Controller):
    pass