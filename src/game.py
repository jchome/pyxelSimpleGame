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


class Game:
    
    def __init__(self):
        pyxel.init(160, 120, caption="Game")
        pyxel.load("assets/game.pyxres")

        self.playground = PlayGround()
        self.player = Player(2,2)
        self.flower = ObjectOnGame("FLOWER", 5,5)
        self.coin = ObjectOnGame("COIN", 3,3)
        
        # Run the main loop
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()
        
        self.flower.update()
        self.coin.update()
        self.player.update()

        if self.player.detect_collision(self.coin):
            print("Get Coin !")
            
    def draw(self):
        self.playground.draw()
        self.flower.draw()
        self.coin.draw()

        # Draw the player at the end
        self.player.draw()
    
        
Game()