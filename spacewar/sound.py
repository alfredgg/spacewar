#!/usr/bin/env python
# -*- coding: utf-8 -*-

AVAILABLE_SOUNDS = dict()

def register_sound(key, file):
    pass

def play(key, bucle=False):
    value = AVAILABLE_SOUNDS[key]
    return Bucle(value) if bucle else Effect(value)

class Sound(object):
    pass

class Effect(Sound):
    pass

class Bucle(Sound):
    pass