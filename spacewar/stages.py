#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import physics
from controllers import Player1Controller, Player2Controller, RobotController
from elements import SpaceShip1, SpaceShip2, Planet

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
    def __init__(self, game, points1=0, points2=0, robot1=False, robot2=True, planet=False, gravity=False, debug=False):
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
            pygame.K_F4: self.toogle_gravity,
            pygame.K_F12: self.toogle_debug
        }
        self.show_planet = planet
        self.gravity = gravity
        self.debug = debug

    def next_stage(self):
        self.game.change_stage(Game(self.game, self.controller1, self.controller2, self.show_planet, self.gravity, self.debug))

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

    def toogle_debug(self):
        self.debug = not self.debug

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
    def __init__(self, game, controller1, controller2, planet=False, gravity=False, debug=False):
        Stage.__init__(self, game)
        image = pygame.image.load('pictures/background.png')
        self.image = pygame.transform.scale(image, self.game.screen_size)

        self.controller1 = controller1
        self.controller2 = controller2
        x_pos1 = (self.game.screen_size[0] / 4) * 1
        x_pos2 = (self.game.screen_size[0] / 4) * 3
        y_pos = (self.game.screen_size[1] / 4) * 3
        self.controller1.ship = self.spaceship1 = SpaceShip1((x_pos1, y_pos),
                                                             add_new_element_function=self.add_new_element)
        self.controller2.ship = self.spaceship2 = SpaceShip2((x_pos2, y_pos),
                                                             angle=180,
                                                             add_new_element_function=self.add_new_element)
        self.planet = planet
        self.gravity = gravity
        self.debug = debug
        self.game_elements = []

        self.physic_world = physics.init()
        self.add_new_element(self.spaceship1)
        self.add_new_element(self.spaceship2)
        if planet:
            self.add_new_element(Planet((self.game.screen_size[0]/2, self.game.screen_size[1]/2)))

    def next_stage(self):
        self.game.change_stage(Menu(self.game, self.spaceship1.points, self.spaceship2.points,
                                    isinstance(self.controller1, RobotController),
                                    isinstance(self.controller2, RobotController),
                                    self.planet, self.gravity, self.debug))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
        for ge in self.game_elements:
            ge.draw(self.game.screen)
        if self.debug:
            physics.draw(self.game.screen, self.game_elements)

    def keypressed(self, key):
        if key == pygame.K_ESCAPE:
            self.next_stage()
            return
        elif key == pygame.K_F12:
            self.debug = not self.debug
        self.controller1.keypressed(key)
        self.controller2.keypressed(key)

    def keyup(self, key):
        self.controller1.keyup(key)
        self.controller2.keyup(key)

    def update(self):
        self.controller1.update()
        self.controller2.update()
        physics.update(self.physic_world, self.game_elements)

    def add_new_element(self, ge):
        physics.set_body(ge)
        self.game_elements.append(ge)
