#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import pymunk as pm

COLOR_SIZE = (255, 0, 0)

def init():
    space = pm.Space()
    space.gravity = (0.0, -900.0)
    return space

def update(space, game_elements):
    space.step(1/50.0)
    for ge in game_elements:
        pass

def set_body(element):
    element.body = pm.Body()

def draw(screen, game_elements):
    for ge in game_elements:
        pygame.draw.circle(screen, COLOR_SIZE, ge.position, ge.radio, 1)
        pygame.draw.line(screen, COLOR_SIZE, ge.position, (ge.position[0]+ge.radio, ge.position[1]), 1)

