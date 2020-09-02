#!/bin/env python3
'''
Created on Aug 5, 2020

@author: julien
'''


import pyxel
## https://github.com/kitao/pyxel

from playground import PlayGround
from player import Player
from objectOnGame import ObjectOnGame

TILE_SIZE = 16

class Game:
    
    def __init__(self):
        pyxel.init(160, 120, caption="Game")
        pyxel.load("assets/game.pyxres")
        self.walls = []
        self.interaction_objects = []

        self.playground = PlayGround()
        self.player = Player(2 * TILE_SIZE, 2 * TILE_SIZE)

        coin = ObjectOnGame("COIN", 3 * TILE_SIZE, 3 * TILE_SIZE)
        coin.width = 10
        coin.height = 10
        self.interaction_objects.append(coin)

        bush = ObjectOnGame("BUSH", 5 * TILE_SIZE, 3 * TILE_SIZE)
        self.walls.append(bush)


        # Run the main loop
        pyxel.run(self.update, self.draw)

    """Update objects for animation
    """
    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        self.playground.update()
        
        for wall_object in self.walls:
            wall_object.update()

        ## Handle interaction
        for simple_object in self.interaction_objects:
            if not simple_object.is_visible:
                ## Bypass non-visible objects
                continue

            simple_object.update()
            if self.player.detect_collision(simple_object):
                ## Transform the COIN object as COIN-BONUS
                simple_object.is_visible = False # TODO: Remove this object from the array

                coin_bonus = ObjectOnGame("COIN-BONUS", loop_animation=False)
                coin_bonus.pos_x = simple_object.pos_x
                coin_bonus.pos_y = simple_object.pos_y
                coin_bonus.dy = -2 ## Move to UP
                self.playground.background_objects.append(coin_bonus)
        
        self.player.update(self.walls)

    """Draw objects in the screen
    """
    def draw(self):
        self.playground.draw()

        for simple_object in self.interaction_objects:
            simple_object.draw()

        for wall_object in self.walls:
            wall_object.draw()

        # Draw the player at the end
        self.player.draw()
    
        
Game()