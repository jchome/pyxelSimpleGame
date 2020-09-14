
import pyxel
import yaml


TRANSPARENT_COLOR = 15
TILE_SIZE = 16

class ObjectOnGame:
    def __init__(self, sprite_name, pos_x=0, pos_y=0, loop_animation = True):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self._animation_flow = 0 # Float version of the animation step
        self.sprite_name = sprite_name
        self._is_visible = True
        self._sprites = []
        self.init_with_key(sprite_name)
        ## Moving during animation
        self.dx = 0
        self.dy = 0

    def init_with_key(self, key_name):
        with open(r'src/assets/objects.yaml') as file:
            #print("Loading %s..." % key_name)
            object_data = yaml.load(file)[key_name]
            self.width = object_data["width"]
            self.height = object_data["height"]
            if "velocity" in object_data:
                self.velocity = object_data["velocity"]
            if "loop-animation" in object_data:
                self._loop_animation = object_data["loop-animation"]
            
            if "footprint" in object_data:
                self.footprint = self._get_coordinates(object_data["footprint"])
            else:
                self.footprint = (0,0,16,16) # default footprint

            self._sprites = []
            for coordinates_str in object_data["sprites"]:
                coordinate_converted = self._get_coordinates(coordinates_str)
                self._sprites.append(coordinate_converted)

    @property
    def is_visible(self):
        return self._is_visible
    
    @is_visible.setter
    def is_visible(self, value):
        self._is_visible = value
        ## Stop the animation if the object is not visible
        if not self._is_visible:
            self._animation_flow = 0
    
    """Cut the string_of_4_int as "a,b,c,d" and convert as array of int
    """
    def _get_coordinates(self, string_of_4_int):
        coordinate_array = string_of_4_int.split(',')
        return [int(x) for x in coordinate_array]

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
        ## Cut the sprite in the image bank #0
        u,v,w,h =  self._sprites[int(self._animation_flow)]
        
        #self._draw_bounding_box()
        #bltm(x on screen, y on screen, image map, u, v, w, h, [colkey])
        pyxel.blt(self.pos_x,self.pos_y, image_bank, u,v, w,h, TRANSPARENT_COLOR)

        ### Draw the footprint, to check coordinates
        #pyxel.rectb(self.pos_x+self.footprint[0],self.pos_y+self.footprint[1],self.footprint[2],self.footprint[3],8)

        ## Animate the sprite
        if len( self._sprites) == 1:
            ## There is no animation
            return
        
        if self._animation_flow >= len( self._sprites)-1:
            if self._loop_animation:
                ## Restart the animation from the beginning
                self._animation_flow = 0
            else:
                ## Hide the object
                self.is_visible = False
        else:
            ## Step the animation
            self._animation_flow = self._animation_flow + self.velocity
            self.pos_x += self.dx
            self.pos_y += self.dy
        

    """Draw the bounding box around the player
    """
    def _draw_bounding_box(self):
        pyxel.rectb(self.pos_x,self.pos_y, self.width, self.height, 3)
    