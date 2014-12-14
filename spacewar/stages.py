#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import physics
from controllers import Player1Controller, Player2Controller, RobotController
import elements

TEXT_OFFSET = 10
MENU_OFFSET = 25
MENU_YPART = 9
SOUNDS_LOADED = False

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
        self.points1 = points1
        self.points2 = points2
        self.menu_y = 0
        self.menu_robot1_x = 0
        self.menu_robot2_x = 0
        self.menu_planet_x = 0
        self.menu_gravity_x = 0
        self.image = self.create_image()
        if not SOUNDS_LOADED:
            self.load_sounds()

    def create_image(self):
        image = elements.background(self.game.screen_size)
        ship1 = pygame.transform.scale(pygame.image.load(elements.SPACESHIP1_FILE),
                                       (elements.SPACESHIP_SIZE, elements.SPACESHIP_SIZE))
        ship2 = pygame.transform.scale(pygame.image.load(elements.SPACESHIP2_FILE),
                                       (elements.SPACESHIP_SIZE, elements.SPACESHIP_SIZE))
        x_pos1 = (self.game.screen_size[0] / 4) * 1
        x_pos2 = (self.game.screen_size[0] / 4) * 2.5
        y_pos = (self.game.screen_size[1] / 4) * 3
        image.blit(ship1, (x_pos1, y_pos))
        image.blit(ship2, (x_pos2, y_pos))
        title = pygame.image.load(elements.TITLE_FILE)
        tit_w = (self.game.screen_size[0] / 10) * 8
        tit_h = (tit_w * title.get_height()) / title.get_width()
        title = pygame.transform.scale(title, (tit_w, tit_h))
        image.blit(title, ((self.game.screen_size[0] / 2) - (tit_w / 2),
                           (self.game.screen_size[1] / 2) - (tit_h / 2)))
        planet = pygame.image.load(elements.PLANET_FILE)
        planet = pygame.transform.scale(planet, (elements.PLANET_SIZE, elements.PLANET_SIZE))
        image.blit(planet, ((self.game.screen_size[0] / 8) * 6, self.game.screen_size[0] / 20))
        myfont = pygame.font.SysFont("monospace", 25, bold=True)
        label = myfont.render("=" + str(self.points1), 1, (255,255,255))
        image.blit(label, (x_pos1 + TEXT_OFFSET + elements.SPACESHIP_SIZE, y_pos))
        label = myfont.render("=" + str(self.points2), 1, (255,255,255))
        image.blit(label, (x_pos2 + TEXT_OFFSET + elements.SPACESHIP_SIZE, y_pos))
        myfont = pygame.font.SysFont("monospace", 17, bold=True)
        menu_offset = self.game.screen_size[0] / MENU_OFFSET
        self.menu_y = (self.game.screen_size[0] / MENU_YPART) * 6
        image.blit(myfont.render("[Esc]Exit", 1, (255,255,255)), (menu_offset * 0, self.menu_y))
        image.blit(myfont.render("[Space]Play", 1, (255,255,255)), (menu_offset * 3.75, self.menu_y))
        self.menu_robot1_x = menu_offset * 8.5
        image.blit(myfont.render("[F1]Robot1", 1, (255,255,255)), (self.menu_robot1_x, self.menu_y))
        self.menu_robot2_x = menu_offset * 12.5
        image.blit(myfont.render("[F2]Robot2", 1, (255,255,255)), (self.menu_robot2_x, self.menu_y))
        self.menu_planet_x = menu_offset * 16.75
        image.blit(myfont.render("[F3]Planet", 1, (255,255,255)), (self.menu_planet_x, self.menu_y))
        self.menu_gravity_x = menu_offset * 21
        image.blit(myfont.render("[F4]Gravity", 1, (255,255,255)), (self.menu_gravity_x, self.menu_y))
        return image

    def load_sounds(self):
        global SOUNDS_LOADED
        import sound
        sound.register_sound(elements.SOUND_ALARM, 'sounds/alarm.wav')
        sound.register_sound(elements.SOUND_EXPLOSION, 'sounds/explosion.wav')
        sound.register_sound(elements.SOUND_IMPACT, 'sounds/impact.wav')
        sound.register_sound(elements.SOUND_LASER, 'sounds/laser.wav')
        sound.register_sound(elements.SOUND_MISSILE, 'sounds/missile.wav')
        sound.register_sound(elements.SOUND_TELEPORT, 'sounds/teleport.wav')
        SOUNDS_LOADED = True

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
            self.game.draw_alpha_rect((255, 255, 255), 150, (self.menu_robot1_x, self.menu_y),
                                      (self.menu_robot2_x-self.menu_robot1_x, 20))
        if isinstance(self.controller2, RobotController):
            self.game.draw_alpha_rect((255, 255, 255), 150, (self.menu_robot2_x, self.menu_y),
                                      (self.menu_planet_x - self.menu_robot2_x, 20))
        if self.show_planet:
            self.game.draw_alpha_rect((255, 255, 255), 150, (self.menu_planet_x, self.menu_y),
                                      (self.menu_gravity_x - self.menu_planet_x, 20))
        if self.gravity:
            self.game.draw_alpha_rect((255, 255, 255), 150, (self.menu_gravity_x, self.menu_y),
                                      (self.game.screen_size[0] - self.menu_gravity_x, 20))

    def keypressed(self, key):
        func = self.keys.get(key, None)
        if func:
            func()

class Game(Stage):
    def __init__(self, game, controller1, controller2, planet=False, gravity=False, debug=False, points1= 0, points2=0):
        Stage.__init__(self, game)
        self.image = elements.background(self.game.screen_size, add_bars=True)

        self.controller1 = controller1
        self.controller2 = controller2
        x_pos1 = (self.game.screen_size[0] / 8) * 1
        y_pos1 = (self.game.screen_size[1] / 5) * 1
        x_pos2 = (self.game.screen_size[0] / 8) * 7
        y_pos2 = (self.game.screen_size[1] / 5) * 4
        self.controller1.ship = self.spaceship1 = elements.SpaceShip1((x_pos1, y_pos1),
                                                                      angle=180,
                                                                      add_new_element_function=self.add_new_element)
        self.controller2.ship = self.spaceship2 = elements.SpaceShip2((x_pos2, y_pos2),
                                                                      add_new_element_function=self.add_new_element)
        self.planet = planet
        self.gravity = gravity
        self.debug = debug
        self.game_elements = []

        self.world = physics.SpaceWarWorld()
        self.add_new_element(self.spaceship1)
        self.add_new_element(self.spaceship2)
        self.points1 = points1
        self.points2 = points2
        if planet:
            self.add_new_element(elements.Planet(
                ((self.game.screen_size[0]/2) - (elements.PLANET_SIZE/2),
                 (self.game.screen_size[1]/2) - (elements.PLANET_SIZE/2))))
        self.bar1 = elements.Bar(self.spaceship1, True)
        self.bar2 = elements.Bar(self.spaceship2, False)

    def next_stage(self):
        self.game.change_stage(Menu(self.game, points1=self.points1, points2=self.points2,
                                    robot1=isinstance(self.controller1, RobotController),
                                    robot2=isinstance(self.controller2, RobotController),
                                    planet=self.planet, gravity=self.gravity, debug=self.debug))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
        for ge in self.game_elements:
            ge.draw(self.game.screen)
        self.bar1.draw(self.game.screen)
        self.bar2.draw(self.game.screen)
        if self.debug:
            self.world.draw(self.game.screen, self.game_elements)

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
        self.bar1.update()
        self.bar2.update()
        self.world.update(self.game_elements)

    def add_new_element(self, ge):
        self.world.set_body(ge)
        self.game_elements.append(ge)
