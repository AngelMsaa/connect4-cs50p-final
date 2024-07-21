# Connect 4
#### Video Demo:  <URL HERE>
## How to play

1. Clone the repository
2. Install the required packages using `pip install -r requirements.txt`
3. Run the game using `python project.py`
4. Find someone to play with (or not!)
4. Follow the instructions in the terminal
5. Enjoy the game!

## Overview
Connect 4 is a classic game where two players drop colored coins in a 6x7 grid with the goal of connecting four of their coins in a row. 

The game is always started by the yellow player, and they take turns dropping their coins from the top of the grid. The game ends when one of the players achieves a win or the board is full, which would force a draw.

This project is a simple Python implementation of the game, designed to be played in the terminal. Notably, the game allows the players to choose 
the board with, with a minimum of 4 and a maximum of 50 rows.

### Files
The code for the project is all stored in `project.py`, and the tests are in `test_project.py`. The project also includes a `requirements.txt` file that lists the Python packages that the project depends on.

### Packages

The project uses the following packages:
- `terminaltables`: This package is used to display the game board in a visually appealing table format.
- `colorama`: This package is used to add color to the terminal, enhancing the user experience.

For testing, the project relies on:
- `pytest`: This package is used for writing and running unit tests for the project.
- `mock`: This package is used to mock the `input` function in the tests to simulate user input.

## Design

#### Classes and Functions

The project is structured around two main classes: 

- `Game`: Initiates the board, manages the game loop, the turn system, and checks for win conditions.

- `Board`: Represents the game board, stores the coins placed by the players, and provides methods for placing coins and  displaying the board (with 
  `__str__`). 

There's also a utility function called `clear_screen` that clears the terminal screen. 


#### Some Key Decisions:

- **Choosing a GUI**: Whilst there are libraries that would allow for a much more visually appealing game board, I thought it was interesting to 
  limit myself to the terminal to stay true to the core of the course and to not overcomplicate the project.


- **Checking for a win condition**: Every time a user places a coin, the game iterates over all placed coins to check if there are win conditions. Whilst potentially less eficient, I thought this was less error prone as it would be easier to maintain and understand. Perfomance should not be 
  a concern, as the game is not too CPU intensive.


- **3 main functions**: The three top-level functions (`main`, `play_game`, and `get_user_input`) were placed like this due to constraints given 
  by the academic team. start_game and get_board_size I would've placed them somewhere else.

4. **Testing**: The decision to include a separate file for tests (`test_project.py`) was made to ensure the reliability and stability of the game. By using `pytest`, the project benefits from a powerful yet simple testing framework that can be expanded to cover more complex test cases in the future.

In conclusion, this Connect 4 project is a comprehensive implementation of the classic game, designed with attention to detail and user experience in mind. It showcases the use of Python for creating interactive terminal-based applications and demonstrates good practices in software development, including modular design, error handling, and automated testing. Be sure to check out the video demo to see the game in action!