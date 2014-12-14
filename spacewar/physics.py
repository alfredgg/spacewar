#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import pymunk as pm

COLOR_SIZE = (255, 0, 0)

class SpaceWarWorld(object):
    def __init__(self):
        self.space = pm.Space()
        self.space.gravity = (0.0, -900.0)

    def update(self, game_elements):
        self.space.step(1/50.0)
        for ge in game_elements:
            pass

    def set_body(self, element):
        element.body = pm.Body()

    def draw(self, screen, game_elements):
        for ge in game_elements:
            pygame.draw.circle(screen, COLOR_SIZE, ge.position, ge.radio, 1)
            pygame.draw.line(screen, COLOR_SIZE, ge.position, (ge.position[0]+ge.radio, ge.position[1]), 1)
