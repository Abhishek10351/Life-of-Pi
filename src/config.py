import pathlib
import arcade.color as color
# Dimensions and title
SCREEN_TITLE = "Marrrs Explorer"
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

# Arcade style dicts
STYLE_GOLDEN_TANOI = {"font_name": "Dilo World", "font_color": (255, 207, 112), "bg_color": (0, 140, 176),
                      "border_color": (0, 60, 75)}
STYLE_DANGER = {
    "font_color": color.WHITE,
    "border_width": 2,
    "bg_color": (217, 4, 41),
    "bg_color_pressed": (255, 166, 158),
    "border_color_pressed": (255, 166, 158)

}

STYLE_PRIMARY = {
    "font_color": color.WHITE,
    "border_width": 2,
    "bg_color": (52, 152, 219),
    "bg_color_pressed": (41, 128, 185),
    "border_color_pressed": (41, 128, 185)
}

# Paths
PATH = pathlib.Path(__file__).resolve().parent.parent
ASSET_PATH = pathlib.Path(__file__).resolve().parent.parent / "assets"
SRC_PATH = pathlib.Path(__file__).resolve().parent.parent / "src"

# Camera
CAMERA_MOVEMENT_SPEED = 5
