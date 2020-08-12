#!/bin/env python3
'''
Created on Aug 5, 2020

@author: julien
'''

import pyxel
## https://github.com/kitao/pyxel

from playground import PlayGround
from player import Player


class Game:
    
    def __init__(self):
        pyxel.init(160, 120, caption="Game")
        pyxel.load("assets/game.pyxres")

        self.playground = PlayGround()
        self.player = Player()
        
        # Run the main loop
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()
        
        self.player.update()
            
    def draw(self):
        self.playground.draw()
        self.player.draw()
    
        
Game()