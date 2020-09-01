
import pyxel
import yaml

TRANSPARENT_COLOR = 15
TILE_SIZE = 16

class Player:
    def __init__(self, pos_x,pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.direction = "UP"
        ## Detect when the player is running, to start the animation
        self.is_running = False
        self.animation_flow = 0 # Float version of the animation step
        self.read_configuration()

    def read_configuration(self):
        with open(r'src/assets/player.yaml') as file:
            player_data = yaml.load(file)["player"]
            self.width = player_data["width"]
            self.height = player_data["height"]
            self.velocity = player_data["velocity"]
            self.sprites = {}
            for sprite_data in player_data["sprites"]:
                direction = sprite_data.upper()
                sprites_for_one_direction = player_data["sprites"][sprite_data]
                data_for_direction = []
                for coordinates_str in sprites_for_one_direction:
                    coordinate_array = coordinates_str.split(',')
                    coordinate_converted = [int(x) for x in coordinate_array]
                    data_for_direction.append(coordinate_converted)
                self.sprites[direction] = data_for_direction

    """Get key pressed
    """
    def update(self):
        ## Update the direction of the player
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
            self.pos_x = max(self.pos_x - self.velocity, 0)
            self.direction = "LEFT"
            if not self.is_running:
                self.is_running = True
                ## Force to restart the animation to frame #0
                self.animation_flow = 0

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
            self.pos_x = min(self.pos_x + self.velocity, pyxel.width - 16)
            self.direction = "RIGHT"
            if not self.is_running:
                self.is_running = True
                ## Force to restart the animation to frame #0
                self.animation_flow = 0

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_1_UP):
            self.pos_y = max(self.pos_y - self.velocity, 0)
            self.direction = "UP"
            if not self.is_running:
                self.is_running = True
                ## Force to restart the animation to frame #0
                self.animation_flow = 0

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
            self.pos_y = min(self.pos_y + self.velocity, pyxel.width - 16)
            self.direction = "DOWN"
            if not self.is_running:
                self.is_running = True
                ## Force to restart the animation to frame #0
                self.animation_flow = 0

    """Draw the player
    Use "pyxeleditor game.pyxres" to edit the player sprite
    """
    def draw(self):
        image_bank = 0
        ## Cut the sprite in the image bank #0
        u,v,w,h = self.sprites[self.direction][int(self.animation_flow)]
        
        #self._draw_bounding_box()
        #bltm(x on screen, y on screen, image map, u, v, w, h, [colkey])
        pyxel.blt(self.pos_x,self.pos_y, image_bank, u,v, w,h, TRANSPARENT_COLOR)
        
        if self.is_running:
            if self.animation_flow >= len(self.sprites[self.direction])-1:
                # Restart the animation from the beginning
                self.animation_flow = 0
                self.is_running = False
            else:
                # One more step of the animation
                self.animation_flow = self.animation_flow + 0.25
        
        #if not was_running and self.is_running:
        #    # The user moves
        #    u,v,w,h = self.sprites["DUST"][int(self.dust_flow)]
        #    pyxel.blt(self.pos_x,self.pos_y, image_bank, u,v, w,h, TRANSPARENT_COLOR)
        #pyxel.text(100,80, self.direction, 0)
        
    
    """Draw the bounding box around the player
    """
    def _draw_bounding_box(self):
        pyxel.rectb(self.pos_x,self.pos_y, self.width, self.height, 3)
    

    """AABB detection
    """
    def detect_collision(self, another_object):
        if self.pos_x < another_object.pos_x+another_object.width and self.pos_x+self.width > another_object.pos_x:
            if self.pos_y < another_object.pos_y+another_object.height and self.pos_y+self.height > another_object.pos_y:
                return True
        return False
        