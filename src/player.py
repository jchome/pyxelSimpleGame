
import pyxel

class Player:
    def __init__(self):
        self.is_alive = True
        self.pos_x = 0
        self.pos_y = 0
        ## Velocity of 1 = small speed, 2 = great speed, 3 = rinning fast
        self.velocity = 3
        self.direction = "LEFT"
        self.transparent_color = 15 # Skin color
        ## Detect when the player is running, to start the animation
        self.is_running = False
        self.animation_step = 0
        self.sprite_rabbit = {
            "LEFT": [(0,0,16,16), (0,16,16,16), (0,32,16,16), (0,48,16,16), (0,64,16,16), (0,80,16,16), (0,96,16,16)],
            "RIGHT": [(0,0,-16,16), (0,16,-16,16), (0,32,-16,16), (0,48,-16,16), (0,64,-16,16), (0,80,-16,16), (0,96,-16,16)]
        }
        

    """Get key pressed
    """
    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
            self.pos_x = max(self.pos_x - self.velocity, 0)
            ## Update the direction of the player
            self.direction = "LEFT"
            if not self.is_running:
                self.is_running = True
                ## Force to restart the animation to frame #0
                self.animation_step = 0

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
            self.pos_x = min(self.pos_x + self.velocity, pyxel.width - 16)
            ## Update the direction of the player
            self.direction = "RIGHT"
            if not self.is_running:
                self.is_running = True
                ## Force to restart the animation to frame #0
                self.animation_step = 0

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_1_UP):
            self.pos_y = max(self.pos_y - self.velocity, 0)
            if not self.is_running:
                self.is_running = True
                ## Force to restart the animation to frame #0
                self.animation_step = 0

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
            self.pos_y = min(self.pos_y + self.velocity, pyxel.width - 16)
            if not self.is_running:
                self.is_running = True
                ## Force to restart the animation to frame #0
                self.animation_step = 0

    """Draw the player
    Use "pyxeleditor game.pyxres" to edit the player sprite
    """
    def draw(self):
        image_bank = 0
        ## Cut the sprite in the image bank #0
        u,v,w,h = self.sprite_rabbit[self.direction][self.animation_step]
        
        #bltm(x on screen, y on screen, image map, u, v, w, h, [colkey])
        pyxel.blt(self.pos_x,self.pos_y, image_bank, u,v, w,h, self.transparent_color)
        
        if self.is_running:
            if self.animation_step == 6:
                self.animation_step = 0
                self.is_running = False
            else:
                self.animation_step = self.animation_step + 1
        #pyxel.text(100,80, self.direction, 0)

    #def change_direction(self, direction):
        