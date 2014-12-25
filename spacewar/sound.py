#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

AVAILABLE_SOUNDS = dict()

def register_sound(key, path):
    global AVAILABLE_SOUNDS
    AVAILABLE_SOUNDS[key] = pygame.mixer.Sound(path)

def sound(key, play=True, bucle=False):
    value = AVAILABLE_SOUNDS[key]
    loop = -1 if bucle else 0
    if play:
        value.play(loops=loop)
    return value