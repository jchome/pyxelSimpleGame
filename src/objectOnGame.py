
import pyxel

TRANSPARENT_COLOR = 15
TILE_SIZE = 16

class ObjectOnGame:
    def __init__(self, sprite_name, tile_x,tile_y):
        self.pos_x = tile_x * TILE_SIZE
        self.pos_y = tile_y * TILE_SIZE
        self.width = 16
        self.height = 16
        self.animation_flow = 0 # Float version of the animation step
        self.sprites = {
            "DUST":     [(34,48,12,8), (34,56, 12,8), (35,64,12,8)],
            "FLOWER":   [(16,48,16,16)],
            "COIN":     [(0,48,16,16), (0,64,16,16), (0,80,16,16), (0,64,16,16)]
        }
        self.sprite_name = sprite_name

    
    """Get key pressed
    """
    def update(self):
        pass


    """Draw the object
    Use "pyxeleditor game.pyxres" to edit the player sprite
    """
    def draw(self):
        image_bank = 0
        sprite_set = self.sprites[self.sprite_name]
        ## Cut the sprite in the image bank #0
        u,v,w,h = sprite_set[int(self.animation_flow)]
        
        #bltm(x on screen, y on screen, image map, u, v, w, h, [colkey])
        pyxel.blt(self.pos_x,self.pos_y, image_bank, u,v, w,h, TRANSPARENT_COLOR)

        ## Animate the sprite
        if len(sprite_set) == 1:
            ## There is no animation
            return
        if self.animation_flow >= len(sprite_set)-1:
            # Restart the animation from the beginning
            self.animation_flow = 0
        else:
            self.animation_flow = self.animation_flow + 0.25
