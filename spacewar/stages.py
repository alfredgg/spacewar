#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from controllers import Player1Controller, Player2Controller, RobotController
from elements import SpaceShip1, SpaceShip2, Planet, Gravity

class Stage(object):
    def __init__(self, game):
        self.game = game

    def keypressed(self, key):
        pass

    def update(self):
        pass

    def next_stage(self):
        pass

    def draw(self, screen):
        pass

    def keyup(self, key):
        pass

class Menu(Stage):
    def __init__(self, game, points1=0, points2=0, robot1=False, robot2=True, planet=False, gravity=False):
        Stage.__init__(self, game)
        image = pygame.image.load('pictures/menu1.png')
        self.image = pygame.transform.scale(image, self.game.screen_size)
        self.controller1 = RobotController() if robot1 else Player1Controller()
        self.controller2 = RobotController() if robot2 else Player2Controller()
        self.keys = {
            pygame.K_ESCAPE: exit,
            pygame.K_SPACE: self.next_stage,
            pygame.K_F1: self.toogle_player1,
            pygame.K_F2: self.toogle_player2,
            pygame.K_F3: self.toogle_planet,
            pygame.K_F4: self.toogle_gravity
        }
        self.show_planet = planet
        self.gravity = gravity

    def next_stage(self):
        self.game.change_stage(Game(self.game, self.controller1, self.controller2, self.show_planet, self.gravity))

    def run(self):
        pass

    def toogle_player1(self):
        self.controller1 = Player1Controller() if isinstance(self.controller1, RobotController) else RobotController()

    def toogle_player2(self):
        self.controller2 = Player2Controller() if isinstance(self.controller2, RobotController) else RobotController()

    def toogle_gravity(self):
        self.gravity = not self.gravity

    def toogle_planet(self):
        self.show_planet = not self.show_planet

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
        if isinstance(self.controller1, RobotController):
            self.game.draw_alpha_rect((255, 255, 255), 150, (300, 430), (120, 20))
        if isinstance(self.controller2, RobotController):
            self.game.draw_alpha_rect((255, 255, 255), 150, (430, 430), (120, 20))
        if self.show_planet:
            self.game.draw_alpha_rect((255, 255, 255), 150, (180, 457), (120, 20))
        if self.gravity:
            self.game.draw_alpha_rect((255, 255, 255), 150, (310, 457), (120, 20))

    def keypressed(self, key):
        func = self.keys.get(key, None)
        if func:
            func()

class Game(Stage):
    def __init__(self, game, controller1, controller2, planet=False, gravity=False):
        Stage.__init__(self, game)
        image = pygame.image.load('pictures/background.png')
        self.image = pygame.transform.scale(image, self.game.screen_size)
        self.controller1 = controller1
        self.controller2 = controller2
        x_pos1 = (self.game.screen_size[0] / 4) * 1
        x_pos2 = (self.game.screen_size[0] / 4) * 3
        y_pos = (self.game.screen_size[1] / 4) * 3
        self.controller1.ship = self.spaceship1 = SpaceShip1((x_pos1, y_pos))
        self.controller2.ship = self.spaceship2 = SpaceShip2((x_pos2, y_pos), angle=180)
        self.planet = Planet() if planet else None
        self.gravity = Gravity() if gravity else None

    def next_stage(self):
        self.game.change_stage(Menu(self.game, self.spaceship1.points, self.spaceship2.points,
                                    isinstance(self.controller1, RobotController),
                                    isinstance(self.controller2, RobotController),
                                    self.planet is not None, self.gravity is not None))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
        self.spaceship1.draw(self.game.screen)
        self.spaceship2.draw(self.game.screen)

    def keypressed(self, key):
        if key == pygame.K_ESCAPE:
            self.next_stage()
            return
        self.controller1.keypressed(key)
        self.controller2.keypressed(key)

    def keyup(self, key):
        self.controller1.keyup(key)
        self.controller2.keyup(key)

    def update(self):
        self.controller1.update()
        self.controller2.update()