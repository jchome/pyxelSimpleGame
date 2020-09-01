
import pyxel


TRANSPARENT_COLOR = 15
TILE_SIZE = 16

class ObjectOnGame:
    def __init__(self, sprite_name, pos_x=0, pos_y=0, loop_animation = True):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = 16
        self.height = 16
        self._animation_flow = 0 # Float version of the animation step
        self._sprites = {
            "DUST":         [(34,48,12,8), (34,56, 12,8), (35,64,12,8)],
            "FLOWER":       [(16,48,16,16)],
            "COIN":         [(0,48,10,10), (0,58,10,10), (0,68,10,10), (0,58,10,10)],
            "COIN-BONUS":   [(0,80,10,10), (0,90,10,10), (0,100,10,10), (0,90,10,10), (0,80,10,10), (0,90,10,10), (0,100,10,10)]
        }
        self.sprite_name = sprite_name
        self._is_visible = True
        self._loop_animation = loop_animation
        self.velocity = 0.25

    @property
    def is_visible(self):
        return self._is_visible
    
    @is_visible.setter
    def is_visible(self, value):
        self._is_visible = value
        ## Stop the animation if the object is not visible
        if not self._is_visible:
            self._animation_flow = 0
    
    """Get key pressed
    """
    def update(self):
        pass


    """Draw the object
    Use "pyxeleditor game.pyxres" to edit the player sprite
    """
    def draw(self):
        if not self.is_visible:
            return

        image_bank = 0
        sprite_set = self._sprites[self.sprite_name]
        ## Cut the sprite in the image bank #0
        u,v,w,h = sprite_set[int(self._animation_flow)]
        
        #self._draw_bounding_box()
        #bltm(x on screen, y on screen, image map, u, v, w, h, [colkey])
        pyxel.blt(self.pos_x,self.pos_y, image_bank, u,v, w,h, TRANSPARENT_COLOR)

        ## Animate the sprite
        if len(sprite_set) == 1:
            ## There is no animation
            return
        
        if self._animation_flow >= len(sprite_set)-1:
            if self._loop_animation:
                ## Restart the animation from the beginning
                self._animation_flow = 0
            else:
                ## Hide the object
                self.is_visible = False
        else:
            self._animation_flow = self._animation_flow + self.velocity
        

    """Draw the bounding box around the player
    """
    def _draw_bounding_box(self):
        pyxel.rectb(self.pos_x,self.pos_y, self.width, self.height, 3)
    