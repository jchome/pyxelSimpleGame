#!/bin/env python3
'''
Created on Aug 5, 2020

@author: julien
'''

import pyxel
from random import randrange

TILE_SIZE = 16
BACKGROUND_COLOR = 11
TRANSPARENT_COLOR = 15

class PlayGround:
    def __init__(self):
        self.sprite_v_h = (16,16)
        self.flowers = (16,64)
        self.grass = (16,80)
        self.salad = (16,96)
        self.big_flower = (16,48)

        
    def draw(self):
        pyxel.cls(col=BACKGROUND_COLOR)
        ## Draw a grid
        for i in range(0, int(pyxel.width / TILE_SIZE)):
            pyxel.line(i*TILE_SIZE, 0, i*TILE_SIZE , pyxel.height, 0)
        for j in range(0, int(pyxel.height / TILE_SIZE)):
            pyxel.line(0, j*TILE_SIZE, pyxel.width, j*TILE_SIZE, 0)
    
    def get_random_position(self):
        # Snap on the grid of size TILE_SIZE
        return (randrange(int(pyxel.width / TILE_SIZE)) * TILE_SIZE, randrange(int(pyxel.height / TILE_SIZE)) * TILE_SIZE)