import arcade
from moviepy.editor import VideoFileClip
import threading

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Video Player and Main Menu"

class MainMenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Main Menu", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

class VideoPlayer:
    def __init__(self, filename):
        self.filename = filename

    def play_video(self, callback):
        def play_video_clip():
            video_clip = VideoFileClip(self.filename)
            video_clip.preview(fps=30, audio=True)
            video_clip.close()

        thread = threading.Thread(target=play_video_clip)
        thread.start()
        thread.join()
        callback()

def switch_to_main_menu():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)
    window.show_view(MainMenuView())
    arcade.run()

def main():
    video_player = VideoPlayer("intro\\alllogos.mp4")
    video_player.play_video(switch_to_main_menu)


if __name__ == "__main__":
    main()