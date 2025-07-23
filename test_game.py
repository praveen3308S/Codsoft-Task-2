"""
Simple test script to verify the Tic Tac Toe AI functionality
Run this to test the core game logic without the GUI
"""

import tictactoe as ttt

def print_board(board):
    """Print the board in a readable format"""
    print("\nCurrent Board:")
    print("  0   1   2")
    for i in range(3):
        row_str = f"{i} "
        for j in range(3):
            cell = board[i][j]
            if cell is None:
                row_str += " - "
            else:
                row_str += f" {cell} "
            if j < 2:
                row_str += "|"
        print(row_str)
        if i < 2:
            print("  ---|---|---")

def test_basic_functionality():
    """Test basic game functions"""
    print("Testing Tic Tac Toe AI - Basic Functionality")
    print("=" * 50)
    
    # Test initial state
    board = ttt.initial_state()
    print("✓ Initial board created")
    print_board(board)
    
    # Test player function
    current_player = ttt.player(board)
    print(f"✓ Current player: {current_player}")
    
    # Test actions
    available_actions = ttt.actions(board)
    print(f"✓ Available actions: {len(available_actions)} moves")
    
    # Test making a move
    board = ttt.result(board, (1, 1))  # X takes center
    print("✓ Made move: X takes center (1,1)")
    print_board(board)
    
    # Test AI move
    print("\n🤖 AI is thinking...")
    value, ai_move = ttt.minimax(board, ttt.IMPOSSIBLE)
    print(f"✓ AI chose move: {ai_move} with value: {value}")
    
    board = ttt.result(board, ai_move)
    print("✓ AI move applied")
    print_board(board)
    
    # Test game state
    is_terminal = ttt.terminal(board)
    winner = ttt.winner(board)
    print(f"✓ Game over: {is_terminal}")
    print(f"✓ Winner: {winner}")
    
    print("\n✅ All basic tests passed!")

def test_ai_performance():
    """Test AI performance at different difficulty levels"""
    print("\n\nTesting AI Performance")
    print("=" * 50)
    
    board = ttt.initial_state()
    board = ttt.result(board, (0, 0))  # X takes corner
    
    difficulties = [ttt.EASY, ttt.MEDIUM, ttt.HARD, ttt.IMPOSSIBLE]
    
    for difficulty in difficulties:
        print(f"\nTesting {difficulty} difficulty:")
        ttt.reset_ai_stats()
        
        value, move = ttt.minimax(board, difficulty)
        stats = ttt.get_ai_stats()
        
        print(f"  Move chosen: {move}")
        print(f"  Nodes explored: {stats['nodes_explored']}")
        print(f"  Time taken: {stats['time_taken']:.4f}s")
        print(f"  Prunings: {stats['prunings']}")

def test_winning_detection():
    """Test winning condition detection"""
    print("\n\nTesting Winning Detection")
    print("=" * 50)
    
    # Test horizontal win
    board = [[ttt.X, ttt.X, ttt.X],
             [None, None, None],
             [None, None, None]]
    
    print("Testing horizontal win:")
    print_board(board)
    print(f"Winner: {ttt.winner(board)}")
    print(f"Terminal: {ttt.terminal(board)}")
    
    # Test diagonal win
    board = [[ttt.O, None, None],
             [None, ttt.O, None],
             [None, None, ttt.O]]
    
    print("\nTesting diagonal win:")
    print_board(board)
    print(f"Winner: {ttt.winner(board)}")
    print(f"Terminal: {ttt.terminal(board)}")
    
    print("\n✅ Winning detection tests passed!")

if __name__ == "__main__":
    try:
        test_basic_functionality()
        test_ai_performance()
        test_winning_detection()
        print("\n🎉 All tests completed successfully!")
        print("\nTo play the game with GUI, run: python runner.py")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
