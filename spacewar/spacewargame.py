#!/usr/bin/env python
# -*- coding: utf-8 -*-

from game import PyGame
from stages import Menu

UPDATE_RATIO = 75

class SpaceWarGame(PyGame):
    def __init__(self):
        PyGame.__init__(self)
        self.current_stage = None

    def setup(self):
        self.set_title("SPACEWAR")
        self.update_ratio = UPDATE_RATIO
        self.current_stage = Menu(self)

    def draw(self):
        self.current_stage.draw(self.screen)

    def change_stage(self, stage):
        self.current_stage = stage

    def keypressed(self, key):
        self.current_stage.keypressed(key)

    def keyup(self, key):
        self.current_stage.keyup(key)

    def update(self):
        self.current_stage.update()