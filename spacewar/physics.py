#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymunk as pm
import math


def coord(point, dist, ang):
    ang = math.radians(ang)
    x = dist * math.cos(ang)
    y = dist * math.sin(ang)
    return point[0] - x, point[1] + y


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