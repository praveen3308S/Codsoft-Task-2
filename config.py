"""
Configuration settings for Tic Tac Toe AI Game
Customize game appearance and behavior here
"""

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Tic-Tac-Toe AI - Minimax Algorithm"

# Game board settings
TILE_SIZE = 100
BOARD_MARGIN = 10

# Color scheme (RGB values)
COLORS = {
    'background_start': (25, 25, 40),
    'background_end': (60, 60, 90),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'dark_gray': (64, 64, 64),
    'light_gray': (192, 192, 192),
    'blue': (70, 130, 180),
    'light_blue': (173, 216, 230),
    'green': (46, 125, 50),
    'light_green': (129, 199, 132),
    'red': (198, 40, 40),
    'light_red': (239, 154, 154),
    'gold': (255, 193, 7),
    'purple': (156, 39, 176),
    'orange': (255, 152, 0),
}

# Font settings
FONT_SIZES = {
    'small': 18,
    'medium': 24,
    'large': 32,
    'xlarge': 48,
    'move': 60,
}

# AI settings
AI_SETTINGS = {
    'easy_random_chance': 0.3,
    'medium_random_chance': 0.15,
    'hard_random_chance': 0.05,
    'max_depth': {
        'easy': 2,
        'medium': 4,
        'hard': 6,
        'impossible': 9,
    }
}

# Animation settings
ANIMATION_SETTINGS = {
    'thinking_speed': 0.2,
    'move_delay': 0.5,
    'button_delay': 0.1,
}

# Game features
FEATURES = {
    'show_stats_default': False,
    'show_ai_info_default': False,
    'hint_mode_default': False,
    'animations_enabled': True,
}
