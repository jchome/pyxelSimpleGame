#!/bin/env python3
'''
Created on Aug 5, 2020

@author: julien
'''

import pyxel
from random import randrange

class PlayGround:
    def __init__(self):
        self.background_color = 11
        self.transparent_color = 15
        self.sprite_v_h = (16,16)
        self.flowers = (16,0)
        self.grass = (16,16)
        self.salad = (16,32)
        self.big_flower = (16,48)

        self.flower_position = self.get_random_position()
        self.grass_position = self.get_random_position()
        self.salad_position = self.get_random_position()
        self.big_flower_position = self.get_random_position()

    def draw(self):
        pyxel.cls(col=self.background_color)
        w,h = self.sprite_v_h
        
        # TODO: draw the baground
        image_bank = 0
        pos_x,pos_y = self.flower_position
        u,v = self.flowers
        pyxel.blt(pos_x,pos_y, image_bank, u,v, w,h, self.transparent_color)

        pos_x,pos_y = self.grass_position
        u,v = self.grass
        pyxel.blt(pos_x,pos_y, image_bank, u,v, w,h, self.transparent_color)

        pos_x,pos_y = self.salad_position
        u,v = self.salad
        pyxel.blt(pos_x,pos_y, image_bank, u,v, w,h, self.transparent_color)

        pos_x,pos_y = self.big_flower_position
        u,v = self.big_flower
        pyxel.blt(pos_x,pos_y, image_bank, u,v, w,h, self.transparent_color)
    
    def get_random_position(self):
        return (randrange(pyxel.width), randrange(pyxel.height))