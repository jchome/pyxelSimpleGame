#!/bin/env python3
'''
Created on Aug 5, 2020

@author: julien
'''

import pyxel
from random import randrange

class PlayGround:
    def __init__(self):
        self.background_color = 3
        self.transparent_color = 10
        self.carot = (10,0,11,10)

        self.carot_position = self.get_random_position()

    def draw(self):
        pyxel.cls(col=self.background_color)
        
        # TODO: draw the baground
        #image_bank = 0
        #pos_x,pos_y = self.carot_position
        #u,v, w,h = self.carot
        #pyxel.blt(pos_x,pos_y, image_bank, u,v, w,h, self.transparent_color)
    
    def get_random_position(self):
        return (randrange(pyxel.width), randrange(pyxel.height))