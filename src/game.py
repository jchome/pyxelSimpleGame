#!/bin/env python3
'''
Created on Aug 5, 2020

@author: julien
'''


import pyxel
## https://github.com/kitao/pyxel
import yaml

from playground import PlayGround
from player import Player
from objectOnGame import ObjectOnGame

TILE_SIZE = 8

class Game:
    
    def __init__(self):
        pyxel.init(160, 120, caption="Game")
        pyxel.load("assets/game.pyxres")
        self.walls = []
        self.interaction_objects = []
        self.non_interaction_objects = []

        self.playground = PlayGround()
        ## Place the player on the playground
        self.player = Player(5 * TILE_SIZE, 5 * TILE_SIZE)

        # Read all sprite data
        sprite_file = open(r'src/assets/objects.yaml')
        self.sprite_data = yaml.load(sprite_file)
        self.life_sprite = ObjectOnGame("LIFE", self.sprite_data["LIFE"], 0, 0)

        self._read_tiles()

        # Run the main loop
        pyxel.run(self.update, self.draw)

    def _read_tiles(self):
        tile_file = open('src/assets/tiles.txt', 'r') 
        lines = tile_file.readlines()
        start_read_tiles = False
        start_read_objects = False
        objects = {}
        pos_x = 0
        pos_y = 0
        for line in lines:
            if line.strip().startswith("#") or len(line.strip()) == 0:
                continue
            if line.strip() == "[OBJECTS]":
                start_read_objects = True
                start_read_tiles = False
                continue
            if line.strip() == "[TILES]":
                start_read_objects = False
                start_read_tiles = True
                pos_y = 0
                continue
            if start_read_objects :
                sprite_def = line.split('=')
                (key,sprite) = (sprite_def[0], sprite_def[1].strip())
                objects[key] = sprite
            if start_read_tiles:
                pos_x = 0
                for item in line.strip():
                    if item == ' ':
                        ## No sprite to add
                        pos_x = pos_x + 1
                        continue
                    sprite_name = objects[item]
                    sprite = ObjectOnGame(sprite_name, self.sprite_data[sprite_name], pos_x * TILE_SIZE, pos_y * TILE_SIZE)
                    if sprite.wall:
                        self.walls.append(sprite)
                    elif sprite.interaction:
                        self.interaction_objects.append(sprite)
                    else:
                        self.non_interaction_objects.append(sprite)
                    pos_x = pos_x + 1
                pos_y = pos_y + 1

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
                if simple_object.bonus is not None:
                    ## Transform the COIN object as COIN-BONUS
                    simple_object.is_visible = False # TODO: Remove this object from the array

                    coin_bonus = ObjectOnGame(simple_object.bonus, self.sprite_data[simple_object.bonus], loop_animation=False)
                    coin_bonus.pos_x = simple_object.pos_x
                    coin_bonus.pos_y = simple_object.pos_y
                    coin_bonus.dy = -2 ## Move to UP
                    self.playground.background_objects.append(coin_bonus)

        self.player.update(self.walls)
        if self.player.life > 1:
            self.life_sprite.sprite_index = 4 - self.player.life
        else:
            self.life_sprite.sprite_index = 3

    """Draw objects in the screen
    """
    def draw(self):
        ## Empty the screen
        self.playground.draw()

        ## Draw all objects ...
        all_objects = self.interaction_objects + self.walls + self.playground.background_objects + self.non_interaction_objects
        all_objects.append(self.player)

        ## ... BUT sorted by the position on the screen
        for an_object in sorted(all_objects, key=lambda obj: obj.pos_y + obj.footprint[1], reverse=False):
            an_object.draw()
    
        ## Draw the life of the user
        self.life_sprite.draw()

        if self.player.life <= 0:
            game_over_sprite = ObjectOnGame("GAME_OVER", self.sprite_data["GAME_OVER"], 49,44)
            game_over_sprite.draw()

Game()