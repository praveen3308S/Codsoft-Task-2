import pygame
import sys
import time
import math

import tictactoe as ttt
import config

pygame.init()
size = width, height = config.WINDOW_WIDTH, config.WINDOW_HEIGHT

# Load colors from config
black = config.COLORS['black']
white = config.COLORS['white']
dark_gray = config.COLORS['dark_gray']
light_gray = config.COLORS['light_gray']
blue = config.COLORS['blue']
light_blue = config.COLORS['light_blue']
green = config.COLORS['green']
light_green = config.COLORS['light_green']
red = config.COLORS['red']
light_red = config.COLORS['light_red']
gold = config.COLORS['gold']
purple = config.COLORS['purple']
orange = config.COLORS['orange']

# Gradient background colors
bg_start = config.COLORS['background_start']
bg_end = config.COLORS['background_end']

screen = pygame.display.set_mode(size)
pygame.display.set_caption(config.WINDOW_TITLE)

# Load fonts from config
smallFont = pygame.font.Font("OpenSans-Regular.ttf", config.FONT_SIZES['small'])
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", config.FONT_SIZES['medium'])
largeFont = pygame.font.Font("OpenSans-Regular.ttf", config.FONT_SIZES['large'])
xlFont = pygame.font.Font("OpenSans-Regular.ttf", config.FONT_SIZES['xlarge'])
moveFont = pygame.font.Font("OpenSans-Regular.ttf", config.FONT_SIZES['move'])

# Game state variables
user = None
board = ttt.initial_state()
ai_turn = False
difficulty = ttt.IMPOSSIBLE
game_stats = {"user_wins": 0, "ai_wins": 0, "ties": 0}
show_stats = config.FEATURES['show_stats_default']
show_ai_info = config.FEATURES['show_ai_info_default']
hint_mode = config.FEATURES['hint_mode_default']
animations = config.FEATURES['animations_enabled']
thinking_animation = 0
last_move = None
move_history = []

def draw_gradient_background(surface, start_color, end_color):
    """Draw a vertical gradient background"""
    for y in range(height):
        ratio = y / height
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))

def draw_button(surface, rect, text, font, text_color, bg_color, border_color=None, hover=False):
    """Draw an enhanced button with hover effects"""
    if hover:
        # Slightly lighter background on hover
        bg_color = tuple(min(255, c + 20) for c in bg_color)
    
    pygame.draw.rect(surface, bg_color, rect, border_radius=8)
    if border_color:
        pygame.draw.rect(surface, border_color, rect, width=2, border_radius=8)
    
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def draw_enhanced_board(surface, board, tiles, last_move=None):
    """Draw the game board with enhanced graphics"""
    # Draw board background
    board_rect = pygame.Rect(tiles[0][0].left - 10, tiles[0][0].top - 10, 
                           3 * tiles[0][0].width + 20, 3 * tiles[0][0].height + 20)
    pygame.draw.rect(surface, dark_gray, board_rect, border_radius=10)
    
    for i in range(3):
        for j in range(3):
            rect = tiles[i][j]
            # Highlight last move
            if last_move and last_move == (i, j):
                pygame.draw.rect(surface, gold, rect, border_radius=5)
                pygame.draw.rect(surface, white, rect, width=3, border_radius=5)
            else:
                pygame.draw.rect(surface, light_gray, rect, border_radius=5)
                pygame.draw.rect(surface, white, rect, width=2, border_radius=5)
            
            # Draw X or O with enhanced graphics
            if board[i][j] == ttt.X:
                draw_x(surface, rect.center, rect.width // 3, red)
            elif board[i][j] == ttt.O:
                draw_o(surface, rect.center, rect.width // 3, blue)

def draw_x(surface, center, size, color):
    """Draw an enhanced X"""
    x, y = center
    pygame.draw.line(surface, color, (x - size, y - size), (x + size, y + size), 8)
    pygame.draw.line(surface, color, (x + size, y - size), (x - size, y + size), 8)

def draw_o(surface, center, size, color):
    """Draw an enhanced O"""
    pygame.draw.circle(surface, color, center, size, 8)

def draw_thinking_animation(surface, center, frame):
    """Draw AI thinking animation"""
    angle = frame * 0.2
    for i in range(8):
        dot_angle = angle + i * (2 * math.pi / 8)
        dot_x = center[0] + 30 * math.cos(dot_angle)
        dot_y = center[1] + 30 * math.sin(dot_angle)
        # Use size variation for animation effect since pygame doesn't support alpha blending here
        size = max(2, 8 - i)
        pygame.draw.circle(surface, purple, (int(dot_x), int(dot_y)), size)

def draw_stats_panel(surface):
    """Draw game statistics panel"""
    panel_rect = pygame.Rect(width - 200, 10, 180, 150)
    pygame.draw.rect(surface, dark_gray, panel_rect, border_radius=10)
    pygame.draw.rect(surface, white, panel_rect, width=2, border_radius=10)
    
    # Title
    title = smallFont.render("Game Stats", True, white)
    surface.blit(title, (panel_rect.x + 10, panel_rect.y + 10))
    
    # Stats
    stats_text = [
        f"You: {game_stats['user_wins']}",
        f"AI: {game_stats['ai_wins']}",
        f"Ties: {game_stats['ties']}",
        f"Difficulty: {difficulty}"
    ]
    
    for i, text in enumerate(stats_text):
        color = white
        if i == 0 and game_stats['user_wins'] > 0:
            color = light_green
        elif i == 1 and game_stats['ai_wins'] > 0:
            color = light_red
        
        text_surface = smallFont.render(text, True, color)
        surface.blit(text_surface, (panel_rect.x + 10, panel_rect.y + 40 + i * 25))

def draw_ai_info_panel(surface):
    """Draw AI information panel"""
    if not show_ai_info:
        return
        
    panel_rect = pygame.Rect(10, height - 120, 300, 100)
    pygame.draw.rect(surface, dark_gray, panel_rect, border_radius=10)
    pygame.draw.rect(surface, white, panel_rect, width=2, border_radius=10)
    
    # Title
    title = smallFont.render("AI Analysis", True, white)
    surface.blit(title, (panel_rect.x + 10, panel_rect.y + 10))
    
    # AI stats
    stats = ttt.get_ai_stats()
    info_text = [
        f"Nodes explored: {stats['nodes_explored']}",
        f"Time: {stats['time_taken']:.3f}s",
        f"Prunings: {stats['prunings']}"
    ]
    
    for i, text in enumerate(info_text):
        text_surface = smallFont.render(text, True, white)
        surface.blit(text_surface, (panel_rect.x + 10, panel_rect.y + 35 + i * 20))

def check_button_hover(mouse_pos, rect):
    """Check if mouse is hovering over a button"""
    return rect.collidepoint(mouse_pos)

def handle_menu_screen():
    """Handle the main menu screen"""
    global user, difficulty
    
    # Draw title with glow effect
    title = xlFont.render("Tic-Tac-Toe AI", True, gold)
    title_rect = title.get_rect(center=(width // 2, 80))
    screen.blit(title, title_rect)

    subtitle = mediumFont.render("Powered by Minimax Algorithm & Alpha-Beta Pruning", True, light_blue)
    subtitle_rect = subtitle.get_rect(center=(width // 2, 120))
    screen.blit(subtitle, subtitle_rect)
    
    # Player selection buttons
    mouse_pos = pygame.mouse.get_pos()
    
    playXButton = pygame.Rect(width // 2 - 200, 200, 150, 50)
    playOButton = pygame.Rect(width // 2 + 50, 200, 150, 50)
    
    x_hover = check_button_hover(mouse_pos, playXButton)
    o_hover = check_button_hover(mouse_pos, playOButton)
    
    draw_button(screen, playXButton, "Play as X", mediumFont, white, red, white, x_hover)
    draw_button(screen, playOButton, "Play as O", mediumFont, white, blue, white, o_hover)
    
    # Difficulty selection
    diff_y = 300
    diff_buttons = []
    difficulties = [ttt.EASY, ttt.MEDIUM, ttt.HARD, ttt.IMPOSSIBLE]
    colors = [green, orange, red, purple]
    
    for i, (diff, color) in enumerate(zip(difficulties, colors)):
        button_rect = pygame.Rect(width // 2 - 300 + i * 150, diff_y, 140, 40)
        diff_buttons.append((button_rect, diff))
        
        hover = check_button_hover(mouse_pos, button_rect)
        border_color = gold if diff == difficulty else white
        draw_button(screen, button_rect, diff, smallFont, white, color, border_color, hover)
    
    # Options
    stats_button = pygame.Rect(width // 2 - 100, 380, 200, 40)
    stats_hover = check_button_hover(mouse_pos, stats_button)
    draw_button(screen, stats_button, "Toggle Stats", smallFont, white, dark_gray, white, stats_hover)
    
    ai_info_button = pygame.Rect(width // 2 - 100, 430, 200, 40)
    ai_info_hover = check_button_hover(mouse_pos, ai_info_button)
    draw_button(screen, ai_info_button, "Toggle AI Info", smallFont, white, dark_gray, white, ai_info_hover)
    
    return playXButton, playOButton, diff_buttons, stats_button, ai_info_button

while True:
    # Handle events
    click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Reset game
                user = None
                board = ttt.initial_state()
                ai_turn = False
                last_move = None
                move_history = []
            elif event.key == pygame.K_h:  # Toggle hints
                hint_mode = not hint_mode
            elif event.key == pygame.K_s:  # Toggle stats
                show_stats = not show_stats
            elif event.key == pygame.K_i:  # Toggle AI info
                show_ai_info = not show_ai_info

    # Update thinking animation
    thinking_animation += 1

    # Draw gradient background
    draw_gradient_background(screen, bg_start, bg_end)

    # Main menu screen
    if user is None:
        playXButton, playOButton, diff_buttons, stats_button, ai_info_button = handle_menu_screen()
        
        if click:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.1)
                user = ttt.X
                move_history = []
            elif playOButton.collidepoint(mouse):
                time.sleep(0.1)
                user = ttt.O
                move_history = []
            elif stats_button.collidepoint(mouse):
                show_stats = not show_stats
                time.sleep(0.1)
            elif ai_info_button.collidepoint(mouse):
                show_ai_info = not show_ai_info
                time.sleep(0.1)
            
            # Check difficulty buttons
            for button_rect, diff in diff_buttons:
                if button_rect.collidepoint(mouse):
                    difficulty = diff
                    time.sleep(0.1)
                    break

    else:
        # Game screen
        game_over = ttt.terminal(board)
        current_player = ttt.player(board)

        # Draw game board
        tile_size = 100
        tile_origin = (width / 2 - (1.5 * tile_size), height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                row.append(rect)
            tiles.append(row)

        draw_enhanced_board(screen, board, tiles, last_move)

        # Show game status
        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title_text = "Game Over: Tie!"
                title_color = gold
                game_stats["ties"] += 1
            else:
                if winner == user:
                    title_text = f"You Win! ({winner})"
                    title_color = light_green
                    game_stats["user_wins"] += 1
                else:
                    title_text = f"AI Wins! ({winner})"
                    title_color = light_red
                    game_stats["ai_wins"] += 1
        elif user == current_player:
            title_text = f"Your Turn ({user})"
            title_color = light_blue
        else:
            title_text = "AI Thinking..."
            title_color = purple
            # Draw thinking animation
            if animations:
                draw_thinking_animation(screen, (width // 2, 180), thinking_animation)

        title = largeFont.render(title_text, True, title_color)
        title_rect = title.get_rect(center=(width // 2, 80))
        screen.blit(title, title_rect)

        # AI move logic
        if user != current_player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                value, move = ttt.minimax(board, difficulty)
                if move:
                    board = ttt.result(board, move)
                    last_move = move
                    move_history.append((current_player, move))
                ai_turn = False
            else:
                ai_turn = True

        # Handle user moves
        if click and user == current_player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse):
                        board = ttt.result(board, (i, j))
                        last_move = (i, j)
                        move_history.append((user, (i, j)))
                        break

        # Draw hint system
        if hint_mode and not game_over and user == current_player:
            best_moves = ttt.get_best_moves(board, 2)
            for i, move in enumerate(best_moves):
                row, col = move
                rect = tiles[row][col]
                if board[row][col] == ttt.EMPTY:
                    color = light_green if i == 0 else light_blue
                    pygame.draw.rect(screen, color, rect, 4, border_radius=5)

        # Game over screen
        if game_over:
            # Play again button
            again_button = pygame.Rect(width // 2 - 100, height - 120, 200, 50)
            mouse_pos = pygame.mouse.get_pos()
            again_hover = check_button_hover(mouse_pos, again_button)
            draw_button(screen, again_button, "Play Again", mediumFont, white, green, white, again_hover)
            
            # Menu button
            menu_button = pygame.Rect(width // 2 - 100, height - 60, 200, 40)
            menu_hover = check_button_hover(mouse_pos, menu_button)
            draw_button(screen, menu_button, "Main Menu", smallFont, white, dark_gray, white, menu_hover)
            
            if click:
                mouse = pygame.mouse.get_pos()
                if again_button.collidepoint(mouse):
                    board = ttt.initial_state()
                    ai_turn = False
                    last_move = None
                    move_history = []
                    time.sleep(0.1)
                elif menu_button.collidepoint(mouse):
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False
                    last_move = None
                    move_history = []
                    time.sleep(0.1)

        # Draw side panels
        if show_stats:
            draw_stats_panel(screen)
        
        draw_ai_info_panel(screen)

        # Draw controls help
        help_text = [
            "Controls:",
            "R - Reset Game",
            "H - Toggle Hints",
            "S - Toggle Stats",
            "I - Toggle AI Info"
        ]
        
        for i, text in enumerate(help_text):
            color = light_gray if i == 0 else white
            font = smallFont if i == 0 else smallFont
            text_surface = font.render(text, True, color)
            screen.blit(text_surface, (10, 10 + i * 20))

    pygame.display.flip()
