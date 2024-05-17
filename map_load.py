import arcade
from pathlib import Path

# Define constants for your window dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Tiled Map Example"

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen=True)
        arcade.set_background_color(arcade.color.AMAZON)
        self.camera = None
        self.gui_camera = None

    def setup(self):
        # Set up the Cameras
        self.camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        CURRENT_FILE_DIR = Path(__file__).parent
        self.level_map_filename = CURRENT_FILE_DIR / "map6"
        self.map = arcade.load_tilemap(self.level_map_filename / f"lvl6.tmx", 2.5)
        self.wall_list = self.map.sprite_lists["ground"]
        self.background_layer = self.map.sprite_lists["background"]
        self.houses_Layer = self.map.sprite_lists["houses"]
        self.item_list = self.map.sprite_lists["collectables"]
        self.Acid_Layer = self.map.sprite_lists["acid"]
        self.NPC_layer = self.map.sprite_lists["NPC"]
        self.removableitems_layer = self.map.sprite_lists["removableitems"]
        self.collectables2_layer = self.map.sprite_lists["collectables2"]
        self.decoration_layer = self.map.sprite_lists["decoration"]

    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.background_layer.draw()
        #self.Acid_Layer.draw()
        self.wall_list.draw()
        #self.Acid_Layer.draw()
        self.houses_Layer.draw()
        self.NPC_layer.draw()
        self.item_list.draw()
        self.collectables2_layer.draw()
        self.decoration_layer.draw()
        self.Acid_Layer.draw()
        self.removableitems_layer.draw()

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
