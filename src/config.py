import pathlib

# Dimensions and title
SCREEN_TITLE = "Marrrs Explorer"
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

# Arcade style dicts
STYLE_GOLDEN_TANOI = {"font_name": "Dilo World", "font_color": (255, 207, 112), "bg_color": (0, 140, 176),
                      "border_color": (0, 60, 75)}

# Paths
PATH = pathlib.Path(__file__).resolve().parent.parent
ASSET_PATH = pathlib.Path(__file__).resolve().parent.parent / "assets"
SRC_PATH = pathlib.Path(__file__).resolve().parent.parent / "src"
