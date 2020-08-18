
import pyxel

TRANSPARENT_COLOR = 15
TILE_SIZE = 16

class Player:
    def __init__(self, tile_x,tile_y):
        self.pos_x = tile_x * TILE_SIZE
        self.pos_y = tile_y * TILE_SIZE
        self.width = 12
        self.height = 16
        ## Velocity of 1 = small speed, 2 = great speed, 3 = running fast
        self.velocity = 1
        self.direction = "UP"
        ## Detect when the player is running, to start the animation
        self.is_running = False
        self.animation_flow = 0 # Float version of the animation step
        self.sprites = {
            "LEFT":     [(0,32,-12,16), (0,16,-12,16), (0,0,-12,16), (0,16,-12,16), (0,32,-12,16)],
            "RIGHT":    [(0,32,12,16), (0,16,12,16), (0,0,12,16), (0,16,12,16), (0,32,12,16)],
            "UP":       [(16,32,12,16), (16,16,12,16), (16,0,-12,16), (16,16,-12,16), (16,0,-12,16)],
            "DOWN":     [(32,32,12,16), (32,16,12,16), (32,0,-12,16), (32,16,-12,16), (32,0,-12,16)]
        }
        

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
    
    

    """AABB detection
    """
    def detect_collision(self, another_object):
        if self.pos_x < another_object.pos_x+another_object.width and self.pos_x+self.width > another_object.pos_x:
            if self.pos_y < another_object.pos_y+another_object.height and self.pos_y+self.height > another_object.pos_y:
                return True
        return False
        