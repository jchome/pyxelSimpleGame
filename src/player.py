
import pyxel
import yaml

TRANSPARENT_COLOR = 15
TILE_SIZE = 16


class Player:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.direction = "UP"
        # Detect when the player is running, to start the animation
        self.is_running = False
        self.animation_flow = 0  # Float version of the animation step
        self.read_configuration()
        self.life = 4

    def read_configuration(self):
        with open(r'src/assets/player.yaml') as file:
            player_data = yaml.load(file)["player"]
            self.width = player_data["width"]
            self.height = player_data["height"]
            self.velocity = player_data["velocity"]
            if "footprint" in player_data:
                self.footprint = self._get_coordinates(
                    player_data["footprint"])
            else:
                self.footprint = (0, 0, 16, 16)  # default footprint

            self.sprites = {}
            for sprite_data in player_data["sprites"]:
                direction = sprite_data.upper()
                sprites_for_one_direction = player_data["sprites"][sprite_data]
                data_for_direction = []
                for coordinates_str in sprites_for_one_direction:
                    coordinate_converted = self._get_coordinates(
                        coordinates_str)
                    data_for_direction.append(coordinate_converted)
                self.sprites[direction] = data_for_direction

    """Cut the string_of_4_int as "a,b,c,d" and convert as array of int
    """

    def _get_coordinates(self, string_of_4_int):
        coordinate_array = string_of_4_int.split(',')
        return [int(x) for x in coordinate_array]

    def detect_wall(self, walls, old_x, old_y):
        for wall in walls:
            if self.detect_collision(wall):
                if wall.hit_player is not None:
                    self.pos_x = self.pos_x - ((self.pos_x - old_x) * 5)
                    self.pos_y = self.pos_y - ((self.pos_y - old_y) * 5)
                    self.damage()
                else:
                    self.pos_x = old_x
                    self.pos_y = old_y

    """Get key pressed
    """

    def update(self, walls_objects):
        # If the player is not alive, don't update the move
        if self.life <= 0:
            return

        # Update the direction of the player
        old_x = self.pos_x
        old_y = self.pos_y
        player_is_moving = False
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
            player_is_moving = True
            self.pos_x = max(self.pos_x - self.velocity, 0)
            self.detect_wall(walls_objects, old_x, old_y)
            self.direction = "LEFT"
            if not self.is_running:
                self.is_running = True
                # Force to restart the animation to frame #0
                self.animation_flow = 0

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
            player_is_moving = True
            self.pos_x = min(self.pos_x + self.velocity, pyxel.width - 16)
            self.detect_wall(walls_objects, old_x, old_y)
            self.direction = "RIGHT"
            if not self.is_running:
                self.is_running = True
                # Force to restart the animation to frame #0
                self.animation_flow = 0

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_1_UP):
            player_is_moving = True
            self.pos_y = max(self.pos_y - self.velocity, 0)
            self.detect_wall(walls_objects, old_x, old_y)
            self.direction = "UP"
            if not self.is_running:
                self.is_running = True
                # Force to restart the animation to frame #0
                self.animation_flow = 0

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
            player_is_moving = True
            self.pos_y = min(self.pos_y + self.velocity, pyxel.width - 16)
            self.detect_wall(walls_objects, old_x, old_y)
            self.direction = "DOWN"
            if not self.is_running:
                self.is_running = True
                # Force to restart the animation to frame #0
                self.animation_flow = 0
        if not player_is_moving:
            self.is_running = False
            self.animation_flow = 0

    """Draw the player
    Use "pyxeleditor game.pyxres" to edit the player sprite
    """

    def draw(self):
        image_bank = 0

        # If the player is not alive, draw the dead player

        # Cut the sprite in the image bank #0
        u, v, w, h = self.sprites[self.direction][int(self.animation_flow)]

        # self._draw_bounding_box()
        # bltm(x on screen, y on screen, image map, u, v, w, h, [colkey])
        pyxel.blt(self.pos_x, self.pos_y, image_bank,
                  u, v, w, h, TRANSPARENT_COLOR)

        if self.is_running:
            if self.animation_flow >= len(self.sprites[self.direction])-1:
                # Restart the animation from the beginning
                self.animation_flow = 0
                self.is_running = False
            else:
                # One more step of the animation
                self.animation_flow = self.animation_flow + 0.25

        # if not was_running and self.is_running:
        #    # The user moves
        #    u,v,w,h = self.sprites["DUST"][int(self.dust_flow)]
        #    pyxel.blt(self.pos_x,self.pos_y, image_bank, u,v, w,h, TRANSPARENT_COLOR)
        #pyxel.text(100,80, self.direction, 0)

        # Draw the footprint, to check coordinates
        # pyxel.rectb(self.pos_x+self.footprint[0],self.pos_y+self.footprint[1],self.footprint[2],self.footprint[3],8)

    """Damage the player of a part of its life
    """

    def damage(self):
        # Reduce of 1 point of 4 (4 --> 3 --> 2 --> 1 --> 0)
        self.life -= 1

        if self.life <= 0:
            self.life = 0
            self.direction = "DEAD"

    def is_alive(self):
        return self.life > 0

    """Draw the bounding box around the player
    """

    def _draw_bounding_box(self):
        pyxel.rectb(self.pos_x, self.pos_y, self.width, self.height, 3)

    """AABB detection
    Use the footprint
        if self.pos_x < another_object.pos_x+another_object.width and self.pos_x+self.width > another_object.pos_x:
            if self.pos_y < another_object.pos_y+another_object.height and self.pos_y+self.height > another_object.pos_y:

    """

    def detect_collision(self, another_object):
        player_pos_x = self.pos_x+self.footprint[0]
        player_pos_y = self.pos_y+self.footprint[1]
        another_object_pos_x = another_object.pos_x+another_object.footprint[0]
        another_object_pos_y = another_object.pos_y+another_object.footprint[1]
        if player_pos_x < another_object_pos_x+another_object.footprint[2] and player_pos_x+self.footprint[2] > another_object_pos_x:
            if player_pos_y < another_object_pos_y+another_object.footprint[3] and player_pos_y+self.footprint[3] > another_object_pos_y:
                return True
        return False
