"""All game constants, colors, presets, and type definitions."""

# ── Window ──
WIDTH, HEIGHT = 900, 700
FPS = 60
TITLE = "HIGHWAY FURY"

# ── Colors ──
WHITE       = (255, 255, 255)
BLACK       = (0, 0, 0)
GRAY        = (100, 100, 100)
DARK_GRAY   = (60, 60, 60)
RED         = (220, 50, 50)
YELLOW      = (255, 220, 50)
GREEN       = (50, 180, 80)
DARK_GREEN  = (30, 120, 50)
BLUE        = (50, 120, 220)
SKY_BLUE    = (135, 200, 235)
ORANGE      = (255, 140, 0)
BROWN       = (139, 90, 43)
LIGHT_GRAY  = (180, 180, 180)
ROAD_COLOR  = (55, 55, 65)
SHOULDER_COLOR = (90, 90, 90)
CYAN        = (0, 255, 255)
MAGENTA     = (255, 0, 255)
NEON_GREEN  = (57, 255, 20)
NEON_PINK   = (255, 16, 240)

# ── Road geometry ──
ROAD_LEFT  = 200
ROAD_RIGHT = 700
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT
LANE_COUNT = 4
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT
LANE_CENTERS = [ROAD_LEFT + LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(LANE_COUNT)]

# ── Enemy color palette ──
ENEMY_COLORS = [
    (220, 50, 50), (50, 120, 220), (255, 200, 50),
    (50, 200, 100), (200, 100, 220), (255, 140, 0),
    (100, 200, 220), (220, 220, 220), (180, 50, 180),
]

# ── Obstacle type keys ──
OBS_CAR        = "car"
OBS_TRUCK      = "truck"
OBS_MOTORCYCLE = "motorcycle"
OBS_BARRIER    = "barrier"
OBS_CONE       = "cone"
OBS_OIL        = "oil"
OBS_BROKEN     = "broken"
OBS_POLICE     = "police"

# ── Power-up type keys ──
POWERUP_NITRO  = "nitro"
POWERUP_SHIELD = "shield"
POWERUP_MAGNET = "magnet"

# ── Difficulty presets ──
DIFFICULTY_PRESETS = {
    "easy":   {"hp": 8, "spawn_mult": 0.6, "speed_mult": 0.8, "diff_rate": 0.012,
               "label": "EASY",   "color": GREEN,  "desc": "HP 8 | Slow enemies | Relaxed spawn"},
    "normal": {"hp": 5, "spawn_mult": 1.0, "speed_mult": 1.0, "diff_rate": 0.020,
               "label": "NORMAL", "color": YELLOW, "desc": "HP 5 | Normal speed | Standard"},
    "hard":   {"hp": 3, "spawn_mult": 1.5, "speed_mult": 1.3, "diff_rate": 0.035,
               "label": "HARD",   "color": RED,    "desc": "HP 3 | Fast enemies | Insane spawn"},
}

# ── Character presets ──
CHARACTERS = {
    "rabbit": {"name": "Rabbit", "color": (240, 230, 230), "accent": (255, 180, 190),
               "desc": "Fast steering! Handling +20%"},
    "croc":   {"name": "Croc",   "color": (80, 160, 80),   "accent": (50, 120, 50),
               "desc": "Tough skin! HP+1, less damage"},
    "tiger":  {"name": "Tiger",  "color": (240, 180, 50),  "accent": (60, 40, 20),
               "desc": "Nitro master! Boost +30%"},
    "lion":   {"name": "Lion",   "color": (220, 170, 60),  "accent": (180, 120, 30),
               "desc": "Guts! Combo bonus x2"},
}

DIFFICULTY_KEYS = ["easy", "normal", "hard"]
CHARACTER_KEYS  = ["rabbit", "croc", "tiger", "lion"]
MENU_BUTTONS    = ["START GAME", "HOW TO PLAY", "CHARACTER"]
