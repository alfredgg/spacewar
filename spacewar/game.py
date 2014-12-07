#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

DRAWEVENT = USEREVENT + 1

class PyGame(object):
    def __init__(self):
        self.background_color = (0, 0, 0)
        self.screen_size = (640, 480)
        self.screen = None
        self.grid = (10, 10)
        self.update_ratio = 200

    def background(self, r, g, b):
        self.background_color = (r, g, b)

    def size(self, w, h):
        self.screen_size = (w, h)

    def grid(self, w, h):
        self.grid = (w, h)

    def set_title(self, text):
        pygame.display.set_caption(text)

    def _draw(self):
        self.screen.fill(self.background_color)
        self.draw()
        pygame.display.flip()

    def setup(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def keypressed(self, key):
        pass

    def keyup(self, key):
        pass

    def event(self, evt):
        return True

    def run(self):
        pygame.init()
        self.setup()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.time.set_timer(DRAWEVENT, self.update_ratio)
        while True:
            for event in pygame.event.get():
                if not self.event(event):
                    continue
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == KEYDOWN:
                    self.keypressed(event.key)
                elif event.type == KEYUP:
                    self.keyup(event.key)
                elif event.type == DRAWEVENT:
                    self.update()
            self._draw()

    def draw_rect(self, position, color):
        tamx = self.screen.get_width() / self.grid[0]
        tamy = self.screen.get_height() / self.grid[1]
        pygame.draw.rect(self.screen, color, Rect(position[0] * tamx, position[1] * tamy, tamx, tamy))

    def draw_alpha_rect(self, color, alpha, position, size):
        s = pygame.Surface(size)
        s.set_alpha(alpha)
        s.fill(color)
        self.screen.blit(s, position)