"""
Tic Tac Toe Game with AI Implementation
Features minimax algorithm with alpha-beta pruning for optimal gameplay
Created by: [Your Name]
"""

import random
import time

# Game constants
X = "X"
O = "O"
EMPTY = None

# Difficulty levels
EASY = "EASY"
MEDIUM = "MEDIUM"
HARD = "HARD"
IMPOSSIBLE = "IMPOSSIBLE"

# AI statistics
ai_stats = {
    "nodes_explored": 0,
    "time_taken": 0,
    "prunings": 0,
    "depth_reached": 0
}


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[None, None, None],
            [None, None, None],
            [None, None, None]]


def player(board):
    """
    Determines whose turn it is based on the current board state.
    X always goes first, so if X has more pieces, it's O's turn.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return O if x_count > o_count else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    Each action represents a valid move coordinate where a player can place their symbol.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == None}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    Creates a deep copy to avoid modifying the original board state.
    """
    if not isinstance(action, tuple) or len(action) != 2:
        raise ValueError(f"Invalid action format: {action}")

    # Create a deep copy of the board to avoid side effects
    new_board = [row[:] for row in board]
    current_player = player(board)
    new_board[action[0]][action[1]] = current_player
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row[0] == row[1] == row[2] != EMPTY:
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != EMPTY:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(cell is not None for row in board for cell in row)
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    return 0


def reset_ai_stats():
    """Reset AI statistics for tracking performance"""
    global ai_stats
    ai_stats = {
        "nodes_explored": 0,
        "time_taken": 0,
        "prunings": 0,
        "depth_reached": 0
    }

def get_ai_stats():
    """Get current AI statistics"""
    return ai_stats.copy()

def minimax_with_depth(board, depth, maximizing_player, alpha=float('-inf'), beta=float('inf'), max_depth=9):
    """
    Core minimax algorithm implementation with alpha-beta pruning optimization.

    This function recursively evaluates all possible game states to find the optimal move.
    Alpha-beta pruning eliminates branches that won't affect the final decision,
    significantly improving performance without changing the result.

    Args:
        board: Current game state
        depth: Current search depth
        maximizing_player: True if maximizing (X), False if minimizing (O)
        alpha: Best value maximizer can guarantee
        beta: Best value minimizer can guarantee
        max_depth: Maximum search depth limit

    Returns:
        Tuple of (best_score, best_action)
    """
    global ai_stats
    ai_stats["nodes_explored"] += 1
    ai_stats["depth_reached"] = max(ai_stats["depth_reached"], depth)
    
    if terminal(board) or depth == max_depth:
        score = utility(board)
        # Add depth bonus to prefer quicker wins
        if score == 1:  # X wins
            return score + (10 - depth), None
        elif score == -1:  # O wins
            return score - (10 - depth), None
        else:
            return score, None

    best_action = None
    
    if maximizing_player:  # X's turn (maximize)
        max_eval = float('-inf')
        # Prioritize center and corners for better play
        action_list = list(actions(board))
        action_list.sort(key=lambda x: move_priority(x))
        
        for action in action_list:
            eval_score, _ = minimax_with_depth(result(board, action), depth + 1, False, alpha, beta, max_depth)
            if eval_score > max_eval:
                max_eval = eval_score
                best_action = action
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                ai_stats["prunings"] += 1
                break  # Alpha-beta pruning
        return max_eval, best_action
    else:  # O's turn (minimize)
        min_eval = float('inf')
        # Prioritize center and corners for better play
        action_list = list(actions(board))
        action_list.sort(key=lambda x: move_priority(x))
        
        for action in action_list:
            eval_score, _ = minimax_with_depth(result(board, action), depth + 1, True, alpha, beta, max_depth)
            if eval_score < min_eval:
                min_eval = eval_score
                best_action = action
            beta = min(beta, eval_score)
            if beta <= alpha:
                ai_stats["prunings"] += 1
                break  # Alpha-beta pruning
        return min_eval, best_action

def move_priority(action):
    """
    Assign priority to moves: center > corners > edges
    """
    i, j = action
    if i == 1 and j == 1:  # Center
        return 0
    elif (i, j) in [(0, 0), (0, 2), (2, 0), (2, 2)]:  # Corners
        return 1
    else:  # Edges
        return 2

def minimax(board, difficulty=IMPOSSIBLE):
    """
    Main minimax function with difficulty levels
    """
    start_time = time.time()
    reset_ai_stats()
    
    current_player = player(board)
    maximizing = current_player == X
    
    if difficulty == EASY:
        # 30% chance of random move, 70% chance of decent move
        if random.random() < 0.3:
            available_actions = list(actions(board))
            return 0, random.choice(available_actions)
        else:
            # Use minimax with limited depth
            value, action = minimax_with_depth(board, 0, maximizing, max_depth=2)
    elif difficulty == MEDIUM:
        # 15% chance of suboptimal move
        if random.random() < 0.15:
            available_actions = list(actions(board))
            return 0, random.choice(available_actions)
        else:
            # Use minimax with moderate depth
            value, action = minimax_with_depth(board, 0, maximizing, max_depth=4)
    elif difficulty == HARD:
        # 5% chance of suboptimal move
        if random.random() < 0.05:
            available_actions = list(actions(board))
            top_moves = sorted(available_actions, key=lambda x: move_priority(x))[:3]
            return 0, random.choice(top_moves)
        else:
            # Use minimax with high depth
            value, action = minimax_with_depth(board, 0, maximizing, max_depth=6)
    else:  # IMPOSSIBLE
        # Perfect play - full depth minimax
        value, action = minimax_with_depth(board, 0, maximizing, max_depth=9)
    
    ai_stats["time_taken"] = time.time() - start_time
    return value, action

def get_best_moves(board, num_moves=3):
    """
    Get the top N best moves for hint system
    """
    current_player = player(board)
    maximizing = current_player == X
    
    move_scores = []
    for action in actions(board):
        value, _ = minimax_with_depth(result(board, action), 0, not maximizing, max_depth=5)
        move_scores.append((action, value))
    
    # Sort by score (descending for X, ascending for O)
    move_scores.sort(key=lambda x: x[1], reverse=(current_player == X))
    return [move for move, _ in move_scores[:num_moves]]

def evaluate_position(board):
    """
    Evaluate the current position strength
    """
    if terminal(board):
        return utility(board)
    
    score = 0
    
    # Check all lines (rows, columns, diagonals)
    lines = []
    # Rows
    for i in range(3):
        lines.append([board[i][j] for j in range(3)])
    # Columns
    for j in range(3):
        lines.append([board[i][j] for i in range(3)])
    # Diagonals
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2-i] for i in range(3)])
    
    for line in lines:
        score += evaluate_line(line)
    
    return score

def evaluate_line(line):
    """
    Evaluate a single line (row, column, or diagonal)
    """
    x_count = line.count(X)
    o_count = line.count(O)
    
    if x_count == 3:
        return 100
    elif o_count == 3:
        return -100
    elif x_count == 2 and o_count == 0:
        return 10
    elif o_count == 2 and x_count == 0:
        return -10
    elif x_count == 1 and o_count == 0:
        return 1
    elif o_count == 1 and x_count == 0:
        return -1
    else:
        return 0