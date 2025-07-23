# Tic Tac Toe AI with Minimax Algorithm

A sophisticated Tic Tac Toe game implementation featuring an AI opponent powered by the Minimax algorithm with Alpha-Beta pruning optimization. This project demonstrates advanced game theory concepts and AI decision-making in a classic strategy game.

## Features

### 🎮 Game Modes
- **Human vs AI**: Challenge the computer at various difficulty levels
- **Multiple Difficulty Levels**: Easy, Medium, Hard, and Impossible
- **Interactive GUI**: Beautiful pygame-based graphical interface

### 🤖 AI Implementation
- **Minimax Algorithm**: Perfect decision-making for optimal gameplay
- **Alpha-Beta Pruning**: Performance optimization reducing computation time
- **Difficulty Scaling**: Adjustable AI strength from beginner-friendly to unbeatable
- **Move Prioritization**: Strategic move ordering (center > corners > edges)

### 📊 Advanced Features
- **Performance Analytics**: Real-time AI statistics and analysis
- **Hint System**: Get suggestions for optimal moves
- **Game Statistics**: Track wins, losses, and ties
- **Move History**: Review game progression
- **Smooth Animations**: Enhanced visual experience

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/tic-tac-toe-ai.git
   cd tic-tac-toe-ai
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**:
   ```bash
   python runner.py
   ```

## How to Play

1. **Choose Your Symbol**: Select X or O from the main menu
2. **Select Difficulty**: Choose from Easy, Medium, Hard, or Impossible
3. **Make Your Move**: Click on any empty cell to place your symbol
4. **Win Condition**: Get three symbols in a row (horizontal, vertical, or diagonal)

### Controls
- **R**: Reset current game
- **H**: Toggle hint mode (shows best moves)
- **S**: Toggle game statistics panel
- **I**: Toggle AI analysis information

## AI Difficulty Levels

| Level | Description | Strategy |
|-------|-------------|----------|
| **Easy** | Beginner-friendly | 30% random moves, limited depth search |
| **Medium** | Moderate challenge | 15% suboptimal moves, moderate depth |
| **Hard** | Advanced play | 5% suboptimal moves, high depth search |
| **Impossible** | Perfect play | Full minimax with alpha-beta pruning |

## Technical Implementation

### Minimax Algorithm
The AI uses the minimax algorithm to evaluate all possible game states and choose the optimal move. The algorithm:
- Explores all possible future moves
- Assigns scores to terminal states (+1 for AI win, -1 for player win, 0 for tie)
- Maximizes AI advantage while minimizing player advantage

### Alpha-Beta Pruning
Optimization technique that:
- Reduces the number of nodes evaluated in the search tree
- Maintains the same result as standard minimax
- Significantly improves performance for deeper searches

### Performance Metrics
The game tracks and displays:
- **Nodes Explored**: Total game states evaluated
- **Computation Time**: Time taken for AI decision
- **Pruning Count**: Number of branches eliminated
- **Search Depth**: Maximum depth reached in game tree

## Project Structure

```
tic-tac-toe-ai/
├── tictactoe.py          # Core game logic and AI implementation
├── runner.py             # GUI and game interface
├── requirements.txt      # Python dependencies
├── OpenSans-Regular.ttf  # Font file for UI
├── README.md            # Project documentation
└── .gitignore           # Git ignore rules
```

## Contributing

Contributions are welcome! Feel free to:
- Report bugs or suggest features
- Improve the AI algorithm
- Enhance the user interface
- Add new game modes

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Minimax algorithm implementation based on game theory principles
- Alpha-beta pruning optimization for enhanced performance
- Pygame library for the graphical interface
