# Connect Four Game in Python

This project is a Python implementation of the classic Connect Four game using the Pygame library. The game features a graphical user interface where two players can take turns dropping pieces into a grid, aiming to connect four pieces in a row vertically, horizontally, or diagonally.

## Features

- Two-player game with alternating turns
- Graphical user interface using Pygame
- Visual indication of the current player's turn
- Check for winning conditions (horizontal, vertical, and diagonal)
- Display a winning message when a player wins
- Basic error handling for invalid moves

## Installation

1. Make sure you have Python installed. You can download it from [python.org](https://www.python.org/).

2. Install the required libraries:
   ```bash
   pip install pygame numpy
   ```

## Usage

1. Clone this repository or download the files.
2. Run the `connect_four.py` script:
   ```bash
   python connect_four.py
   ```

## Code Overview

The game logic and user interface are encapsulated in the `ConnectFour` class. Here is a brief overview of the main components:

- **createBoard**: Initializes the game board.
- **printBoard**: Prints the game board to the console (mainly for debugging).
- **drawBoard**: Draws the game board and pieces using Pygame.
- **dropPiece**: Drops a piece in the selected column.
- **isValidLocation**: Checks if a column is valid for a move.
- **getNextOpenRow**: Gets the next open row in a column.
- **winningMove**: Checks for a winning move.
- **handlePlayerMove**: Handles a player's move.
- **runGame**: Main game loop that handles user input and updates the game state.

## Error Handling

- Handles invalid column selections by printing an error message.
- Gracefully handles Pygame initialization errors.

## Future Improvements

- Add AI for single-player mode.
- Implement different game modes and difficulty levels.
- Enhance the graphics and animations.
- Add sound effects and background music.
- Implement an online multiplayer mode.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
