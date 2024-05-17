"""
Example of Pymunk Physics Engine Platformer
"""
import math
import pygame
from typing import Optional
from pathlib import Path
from moviepy.editor import VideoFileClip
import threading


"""
Example code showing how to create a button,
and the three ways to process button events.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.gui_flat_button
"""
import arcade
import arcade.gui

# --- Method 1 for handling click events,
# Create a child class.
import arcade.gui.widgets.buttons
import arcade.gui.widgets.layout

class QuitButton(arcade.gui.widgets.buttons.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()


class MyView(arcade.View):
    def __init__(self):
        super().__init__()

        # Initialize pygame mixer
        pygame.mixer.quit()
        pygame.mixer.init(frequency=44100)

        # Load the MP3 file
        self.sound = pygame.mixer.Sound("songs\\MainmenuMusic.wav")
        self.music_started = False

        # Required for all code that uses UI element, a UIManager to handle the UI
        self.ui = arcade.gui.UIManager()
        self.ui.enable()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.widgets.layout.UIBoxLayout(space_between=20)

        # Create the buttons
        start_button = arcade.gui.widgets.buttons.UIFlatButton(
            text="Έναρξη", width=300
        )
        self.v_box.add(start_button)
        start_button.on_click = self.on_click_start


        credits_button = arcade.gui.widgets.buttons.UIFlatButton(
            text="Τίτλοι Τέλους", width=300
        )
        self.v_box.add(credits_button)
        credits_button.on_click = self.on_click_credits

        # Again, method 1. Use a child class to handle events.
        quit_button = QuitButton(text="Έξοδος", width=300)
        self.v_box.add(quit_button)


        # Create a widget to hold the v_box widget, that will center the buttons
        ui_anchor_layout = arcade.gui.widgets.layout.UIAnchorLayout()
        ui_anchor_layout.add(child=self.v_box, anchor_x="center_x", anchor_y="center_y")

        self.ui.add(ui_anchor_layout)

        self.sound1 = pygame.mixer.Sound("songs\\LostInThePixels.wav")

    def setup(self):
        """Set up the game and initialize the variables."""
        # Set a timer to play the MP3 file after 15 seconds
        threading.Timer(15.5, self.start_music).start()



    def start_music(self):
        """Start playing the MP3 file."""
        self.sound.play(-1)
        self.music_started = True

    def stop_music(self):
        if self.music_started:
            self.sound.stop()

    def on_show_view(self):
        #self.window.background_color = arcade.color.DARK_RED
        # Enable UIManager when view is shown to catch window events
        self.ui.enable()

    def on_hide_view(self):
        # Disable UIManager when view gets inactive
        self.ui.disable()

    def on_click_start(self, event):
        print("Start:", event)
        self.stop_music()
        #pygame.mixer.quit()
        #pygame.mixer.init(frequency=44100)
        #self.sound1.play(-1)
        #self.music_started = True
        game=GameView()
        game.setup()
        self.window.show_view(game)
        self.sound1.play(-1)


    def on_click_credits(self, event):
        print("Credits:", event)
        self.stop_music()
        video_player = VideoPlayer("intro\\credits.mp4")
        video_player.play_video(self.window, switch_to_main_menu)



    def on_draw(self):
        # Draw the background image
        arcade.start_render()
        background_texture = arcade.load_texture("main_menu\\main_menu_17.png")
        arcade.draw_texture_rectangle(
            self.window.width // 2,
            self.window.height // 2,
            self.window.width,
            self.window.height,
            background_texture
        )

        # Draw the UI elements on top of the background
        self.ui.draw()

class VideoPlayer:
    def __init__(self, filename):
        self.filename = filename

    def play_video(self, window, callback):
        def play_video_clip():
            video_clip= VideoFileClip(self.filename)
            video_clip.preview(fps=30, audio=True)
            video_clip.close()
            callback(window)

        threading.Thread(target=play_video_clip).start()
class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        self.texture = arcade.load_texture("main_menu\\main_menu_17-picsay.png")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        self.window.default_camera.use()

    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        video_player = VideoFileClip("intro\\credits.mp4")
        video_player.preview(self.window, switch_to_main_menu)
        view = MyView()
        self.window.show_view(view)
    def switch_to_main_menu(self):
        view = MyView()
        self.window.show_view(view)

class YouLostView(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        self.texture = arcade.load_texture("main_menu\\youlost.jpg")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        self.window.default_camera.use()

    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        video_player = VideoFileClip("intro\\credits.mp4")
        video_player.preview(self.window, switch_to_main_menu)
        view = MyView()
        self.window.show_view(view)

    def switch_to_main_menu(self):
        view = MyView()
        self.window.show_view(view)

SCREEN_TITLE = "BioQuest"

# Gravity
GRAVITY = 1500
# Damping - Amount of speed lost per second
DEFAULT_DAMPING = 1.0
PLAYER_DAMPING = 0.4
# Friction between objects
PLAYER_FRICTION = 1.0
WALL_FRICTION = 0.7
DYNAMIC_ITEM_FRICTION = 0.6
# Mass (defaults to 1)
PLAYER_MASS = 2.0
# Keep player from going too fast
PLAYER_MAX_HORIZONTAL_SPEED = 450
PLAYER_MAX_VERTICAL_SPEED = 1600
# How big are our image tiles?
SPRITE_IMAGE_SIZE = 128
# Scale sprites up or down
SPRITE_SCALING_PLAYER = 2
SPRITE_SCALING_TILES = 0.5
# Scaled sprite size for tiles
SPRITE_SIZE = 64
# Size of grid to show on screen, in number of tiles
SCREEN_GRID_WIDTH = 25
SCREEN_GRID_HEIGHT = 15
# Size of screen to show, in pixels
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
# Force applied while on the ground
PLAYER_MOVE_FORCE_ON_GROUND = 8000
# Force applied when moving left/right in the air
PLAYER_MOVE_FORCE_IN_AIR = 900
# Strength of a jump
PLAYER_JUMP_IMPULSE = 1300

DEAD_ZONE = 0.1
# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1
# How many pixels to move before we change the texture in the walking animation
DISTANCE_TO_CHANGE_TEXTURE = 20
# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN_TOP = 60
VIEWPORT_MARGIN_BOTTOM = 60
VIEWPORT_RIGHT_MARGIN = 270
VIEWPORT_LEFT_MARGIN = 270


class PlayerSprite(arcade.Sprite):
    """ Player Sprite """
    def __init__(self):
        """ Init """
        # Let parent initialize
        super().__init__()

        # Set our scale
        self.scale = SPRITE_SCALING_PLAYER

        main_path = "characters\\sprites"
        self.idle_texture_pair = arcade.load_texture_pair(f"{main_path}_idle0.png")
        self.jump_texture_pair = arcade.load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = arcade.load_texture_pair(f"{main_path}_fall.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = arcade.load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Index of our current texture
        self.cur_texture = 0

        # How far have we traveled horizontally since changing the texture
        self.x_odometer = 0

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """ Handle being moved by the pymunk engine """
        # Figure out if we need to face left or right
        if dx < -DEAD_ZONE and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif dx > DEAD_ZONE and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Are we on the ground?
        is_on_ground = physics_engine.is_on_ground(self)

        # Add to the odometer how far we've moved
        self.x_odometer += dx

        # Jumping animation
        if not is_on_ground:
            if dy > DEAD_ZONE:
                self.texture = self.jump_texture_pair[self.character_face_direction]
                return
            elif dy < -DEAD_ZONE:
                self.texture = self.fall_texture_pair[self.character_face_direction]
                return

        # Idle animation
        if abs(dx) <= DEAD_ZONE:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Have we moved far enough to change the texture?
        if abs(self.x_odometer) > DISTANCE_TO_CHANGE_TEXTURE:

            # Reset the odometer
            self.x_odometer = 0

            # Advance the walking animation
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
class GameView(arcade.View):
    """ Main Window """

    def __init__(self):
        """ Create the variables """

        # Init the parent class
        super().__init__()
        pygame.mixer.quit()
        pygame.mixer.init()

        #self.sound1 = pygame.mixer.Sound("songs\\LostInThePixels.wav")
        #self.music_started = False


        self.score = 0
        self.score_text = None
        # Where is the right edge of the map?
        self.top_of_map = 0
        self.end_of_map = 0
        # Should we reset the score?
        self.reset_score = False



        # Level number to load
        self.level = 1


        self.moving_sprites_list: Optional[arcade.SpriteList] = None

        self.gui_camera = None
        self.camera = None

        # Physics engine
        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]

        #self.gameover_sound = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.collect_coin_sound = arcade.load_sound("sounds\\coin1.wav")
        self.open_door_sound = arcade.load_sound("sounds\\Door_opening.wav")

        # Player sprite
        self.player_sprite: Optional[arcade.Sprite] = None

        # Sprite lists we need
        self.player_list: Optional[arcade.SpriteList] = None
        self.wall_list: Optional[arcade.SpriteList] = None
        self.item_list: Optional[arcade.SpriteList] = None
        self.background_layer: Optional[arcade.SpriteList] = None
        self.houses_Layer: Optional[arcade.SpriteList] = None
        self.Acid_Layer: Optional[arcade.SpriteList] = None
        self.decoration_layer: Optional[arcade.SpriteList] = None
        self.removableitems_layer: Optional[arcade.SpriteList] = None
        self.NPC_layer: Optional[arcade.SpriteList] = None
        self.collectables2: Optional[arcade.SpriteList] = None

        self.sound = pygame.mixer.Sound("songs\\Whispered_Echoes_1.wav")

        # Track the current state of what key is pressed
        self.left_pressed: bool = False
        self.right_pressed: bool = False

        self.is_collected: bool = False

        # Set background color
        self.background_color = arcade.color.LIGHT_SKY_BLUE

        # Track the current state of what key is pressed
        self.left_pressed: bool = False
        self.right_pressed: bool = False

    def setup(self):
        # Create the sprite lists
        self.player_list = arcade.SpriteList()
        #self.bullet_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.gui_camera = arcade.camera.Camera2D()
        # Reset the score if we should
        if self.reset_score:
            self.score = 0
        self.reset_score = False
        self.score_text = arcade.Text(f"Ποσοστό Ολοκλήρωσης Αντιδότου: {self.score} %", x=0, y=5)


        self.camera = arcade.camera.Camera2D()

        # Load the Tiled map
        CURRENT_FILE_DIR = Path(__file__).parent
        # If we put the maps folder inside the game project folder, loading gets easier
        self.level_map_filename = CURRENT_FILE_DIR / "maps"

        atlas = self.window.ctx.default_atlas
        for tex in atlas.textures:
            atlas.remove(tex)

        self.map = arcade.load_tilemap(self.level_map_filename / f"lvl{self.level}.tmx", 2)
        self.wall_list = self.map.sprite_lists["ground"]
        self.background_layer = self.map.sprite_lists["background"]
        self.houses_Layer = self.map.sprite_lists["houses"]
        self.item_list = self.map.sprite_lists["collectables"]
        self.Acid_Layer = self.map.sprite_lists["acid"]
        self.NPC_layer = self.map.sprite_lists["NPC"]
        self.removableitems_layer = self.map.sprite_lists["removableitems"]
        self.collectables2_layer = self.map.sprite_lists["collectables2"]
        self.decoration_layer = self.map.sprite_lists["decoration"]

        # Create player sprite
        self.player_sprite = PlayerSprite()

        # Calculate the right edge of the map in pixels
        self.end_of_map = (self.map.width * self.map.tile_width) * self.map.scaling
        self.top_of_map = (self.map.height * self.map.tile_height) * self.map.scaling

        # Set player location
        self.player_sprite.center_x = 475
        self.player_sprite.center_y = 600
        # Add to player sprite list
        self.player_list.append(self.player_sprite)

        # --- Pymunk Physics Engine Setup ---

        # The default damping for every object controls the percent of velocity
        # the object will keep each second. A value of 1.0 is no speed loss,
        # 0.9 is 10% per second, 0.1 is 90% per second.
        # For top-down games, this is basically the friction for moving objects.
        # For platformers with gravity, this should probably be set to 1.0.
        # Default value is 1.0 if not specified.
        damping = DEFAULT_DAMPING

        # Set the gravity. (0, 0) is good for outer space and top-down.
        gravity = (0, -GRAVITY)

        # Create the physics engine
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping,
                                                         gravity=gravity)

        # Add the player.
        # For the player, we set the damping to a lower value, which increases
        # the damping rate. This prevents the character from traveling too far
        # after the player lets off the movement keys.
        # Setting the moment of inertia to PymunkPhysicsEngine.MOMENT_INF prevents it from
        # rotating.
        # Friction normally goes between 0 (no friction) and 1.0 (high friction)
        # Friction is between two objects in contact. It is important to remember
        # in top-down games that friction moving along the 'floor' is controlled
        # by damping.
        self.physics_engine.add_sprite(self.player_sprite,
                                       friction=PLAYER_FRICTION,
                                       mass=PLAYER_MASS,
                                       moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)

        # Create the walls.
        # By setting the body type to PymunkPhysicsEngine.STATIC the walls can't
        # move.
        # Movable objects that respond to forces are PymunkPhysicsEngine.DYNAMIC
        # PymunkPhysicsEngine.KINEMATIC objects will move, but are assumed to be
        # repositioned by code and don't respond to physics forces.
        # Dynamic is default.
        self.physics_engine.add_sprite_list(self.wall_list,
                                            friction=WALL_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        self.physics_engine.add_sprite_list(self.removableitems_layer,
                                            friction=WALL_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)


        # Create the items
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.UP:
            # find out if player is standing on ground
            if self.physics_engine.is_on_ground(self.player_sprite):
                # She is! Go ahead and jump
                impulse = (0, PLAYER_JUMP_IMPULSE)
                self.physics_engine.apply_impulse(self.player_sprite, impulse)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def pan_camera_to_user(self, panning_fraction: float = 1.0):
        """
        Manage Scrolling

        :param panning_fraction: Number from 0 to 1. Higher the number, faster we
                                 pan the camera to the user.
        """

        # This spot would center on the user
        screen_center_x, screen_center_y = self.player_sprite.position
        if screen_center_x < self.camera.viewport_width/2:
            screen_center_x = self.camera.viewport_width/2
        if screen_center_y < self.camera.viewport_height/2:
            screen_center_y = self.camera.viewport_height/2
        if screen_center_x > self.end_of_map - (self.camera.viewport_width/2):
            screen_center_x = self.end_of_map - (self.camera.viewport_width/2)
        user_centered = screen_center_x, screen_center_y

        self.camera.position = user_centered
        self.camera.position = arcade.math.lerp_2d(self.camera.position, user_centered, 0)



    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.camera.use()
        self.background_layer.draw()
        self.Acid_Layer.draw()
        self.wall_list.draw()
        self.houses_Layer.draw()
        self.NPC_layer.draw()
        self.item_list.draw()
        self.collectables2_layer.draw()
        self.decoration_layer.draw()
        self.removableitems_layer.draw()
        self.player_sprite.draw()
        self.gui_camera.use()
        self.score_text.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """
        # Check if the player got to the end of the level
        # Check length of coin list. If it is 100 or self.level = 7, flip to the
        # game over view.
        if self.score >= 100 and self.level == 6 and self.player_sprite.center_x >= self.end_of_map:
            view = GameOverView()
            self.window.show_view(view)
        elif self.score < 100 and self.level == 6 and self.player_sprite.center_x >= self.end_of_map:
            view = YouLostView()
            self.window.show_view(view)
            pygame.mixer.quit()
            pygame.mixer.init()
            threading.Timer(1.8, self.start_music).start()



        if self.player_sprite.center_x >= self.end_of_map and self.level!= 6:
            # Advance to the next level
            self.level += 1

            # Turn off score reset when advancing level
            self.reset_score = False

            # Reload game with new level
            self.setup()

        self.camera.position = self.player_sprite.position
        is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)
        # Update player forces based on keys pressed
        if self.left_pressed and not self.right_pressed:
            # Create a force to the left. Apply it.
            force = (-PLAYER_MOVE_FORCE_ON_GROUND, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.right_pressed and not self.left_pressed:
            # Create a force to the right. Apply it.
            force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.player_sprite, 0)
        else:
            # Player's feet are not moving. Therefore up the friction so we stop.
            self.physics_engine.set_friction(self.player_sprite, 1.0)

        self.physics_engine.step()
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.item_list
        )

        coin_hit_list2 = arcade.check_for_collision_with_list(self.player_sprite, self.collectables2_layer)

        for coin2 in coin_hit_list2:
            coin2.remove_from_sprite_lists()
            arcade.play_sound(self.open_door_sound)
            self.is_collected = True

        if self.is_collected:
            for sprite in self.removableitems_layer:
                self.physics_engine.remove_sprite(sprite)
                self.removableitems_layer.clear()
            self.is_collected = False


        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score+=4
            self.score_text.text=f"Ποσοστό Ολοκλήρωσης Αντιδότου: {self.score} %"
            arcade.play_sound(self.collect_coin_sound)

        # Pan to the user
        self.pan_camera_to_user(panning_fraction=0.12)

        if arcade.check_for_collision_with_list(
                self.player_sprite, self.map.sprite_lists["acid"]
        ):
            #arcade.play_sound(self.gameover_sound)
            self.setup()

    def start_music(self):
        """Start playing the MP3 file."""
        self.sound.play(-1)
        self.music_started = True

    def stop_music(self):
        if self.music_started:
            self.sound.stop()


def switch_to_main_menu(window):
    window.show_view(MyView())

def main():
    """ Main function """

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)
    video_player = VideoPlayer("intro\\alllogos.mp4")
    video_player.play_video(window, switch_to_main_menu)
    view=MyView()
    view.setup()
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()