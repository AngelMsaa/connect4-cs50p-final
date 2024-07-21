import os
from colorama import Fore
from terminaltables import SingleTable


def main():
    clear()
    Game(start_game())


def start_game():
    """Get the board size from the user and return it."""

    print(f"WELCOME TO CONNECT 4")
    size = get_board_size()
    return size


def get_board_size():
    """Prompt the user to enter the board size."""

    while True:
        try:
            size = input(f"\n{Fore.RESET}Enter the width of your board (min. 4, max. 50): {Fore.RESET}")

            if not 4 <= int(size) <= 50:
                raise IndexError

            if size.isdigit():
                return int(size)
            else:
                raise ValueError

        except IndexError:
            print(f"{Fore.RED}Invalid size, please enter a number between 4 and 50.{Fore.RED}")
        except ValueError:
            print(f"{Fore.RED}Invalid input, please enter a number.{Fore.RED}")


def clear():
    """Clear the terminal."""

    os.system('cls' if os.name == 'nt' else 'clear')


class Game:
    """
    The main game class that initiates the board, manages the game loop, the turn system, and checks for win conditions.
    """

    def __init__(self, size):
        self.board = Board(self, size)
        self.player_turn = "Yellow"
        self.turn_count_yellow = 0
        self.turn_count_red = 0
        self.game_loop()

    def game_loop(self):
        """
        The main game loop that manages the game loop and checks for a win or draw.
        """

        while True:
            clear()
            print(f"\n{self.board}\n")
            self.board.place_coin()
            self.turn_manager()

            if self.check_win():
                break
            elif self.check_draw():
                break

    def turn_manager(self):
        """
        Switch the turn between Yellow and Red.
        """

        if self.player_turn == "Yellow":
            self.turn_count_yellow += 1
            self.player_turn = "Red"
        else:
            self.player_turn = "Yellow"
            self.turn_count_red += 1

    def check_win(self):
        """
        Iterate over all cells in the board, checks if there is a coin, and then checks for either a horizontal, vertical, or diagonal win.
        """
        for row_index, row_data in enumerate(self.board.coins):
            for col_index, value in enumerate(row_data):
                if "●" in value:
                    if (self.check_horizontal_win(row_index, col_index) or
                            self.check_vertical_win(row_index, col_index) or
                            self.check_diagonal_win(row_index, col_index)):
                        winner_turns = str((self.turn_count_yellow if self.player_turn == "Yellow" else self.turn_count_red) + 1)
                        clear()
                        print(f"\n{self.board}\n")
                        if self.player_turn == "Yellow":
                            print(f"{Fore.RED}RED{Fore.GREEN} won in {winner_turns} moves!")
                        elif self.player_turn == "Red":
                            print(f"{Fore.YELLOW}YELLOW{Fore.GREEN} won in {winner_turns} moves!")
                        return True
        return False

    def check_horizontal_win(self, row_index, col_index):
        """
        Check if there is a horizontal win by checking the same row_index and the next 3 columns.
        """
        row_data = self.board.coins[row_index]
        try:
            if row_data[col_index] == row_data[col_index + 1] == row_data[col_index + 2] == row_data[col_index + 3] != "   ":
                return True
            return False
        except IndexError:
            return False

    def check_vertical_win(self, row_index, col_index):
        """
        Check if there is a vertical win by checking the same col_index in the next 3 rows.
        """
        coins_list = self.board.coins
        try:
            if row_index + 3 < len(coins_list) and coins_list[row_index][col_index] == coins_list[row_index + 1][col_index] == coins_list[row_index + 2][col_index] == coins_list[row_index + 3][col_index] != "   ":
                return True
            return False
        except IndexError:
            return False

    def check_diagonal_win(self, row_index, col_index):
        """
        Check if there is a diagonal win by checking the next 3 rows and columns in both directions.
        """
        coins_list = self.board.coins
        try:
            if row_index + 3 < len(coins_list) and col_index + 3 < len(coins_list[row_index]) and coins_list[row_index][col_index] == coins_list[row_index + 1][col_index + 1] == coins_list[row_index + 2][col_index + 2] == coins_list[row_index + 3][col_index + 3] != "   ":
                return True
            if row_index + 3 < len(coins_list) and col_index - 3 >= 0 and coins_list[row_index][col_index] == coins_list[row_index + 1][col_index - 1] == coins_list[row_index + 2][col_index - 2] == coins_list[row_index + 3][col_index - 3] != "   ":
                return True
            return False
        except IndexError:
            return False

    def check_draw(self):
        """
        Check if the game is a draw by checking if all cells are filled with coins.
        """

        if all("●" in value for row in self.board.coins for value in row):
            clear()
            print(f"\n{self.board}\n")
            print(f"{Fore.BLUE}DRAW!{Fore.BLUE}")
            return True
        return False


class Board:
    """
    The board class that manages the game board and the coin placement.
    """

    def __init__(self, game, size=7):
        self.game = game
        self.size = int(size)
        self.board_height = 6
        self.coins = [["   " for _ in range(self.size)] for _ in range(self.board_height)]  # Stores the columns, rows, and coins in the board
        self.table = SingleTable(self.coins)
        self.table.inner_row_border = True

    def __str__(self):
        return self.table.table

    def place_coin(self):
        """
        Place a coin in the selected column.
        """

        print(f"Enter a column number to introduce your coin.\n{self.game.player_turn}'s turn.")
        while True:
            y = input(f"\n{Fore.RESET}>>> {Fore.RESET}")
            try:
                y = int(y) - 1  # Reduces the column number by 1 to match the index
            except ValueError:
                clear()
                print(f"\n{self}\n")
                print(f"Enter a column number to introduce your coin.\n{self.game.player_turn}'s turn.")
                print(f"{Fore.RED}Invalid input, please enter a number between 1 and {self.size}.{Fore.RED}{Fore.RESET}")
                continue

            if y < 0 or y >= len(self.coins[0]):
                clear()
                print(f"\n{self}\n")
                print(f"Enter a column number to introduce your coin.\n{self.game.player_turn}'s turn.")
                print(f"{Fore.RED}Invalid column number, please enter a valid one (1 to {self.size}).{Fore.RED}{Fore.RESET}")
                continue

            if self.game.player_turn == "Yellow":
                coin = f"{Fore.YELLOW} ● {Fore.RESET}"
            else:
                coin = f"{Fore.RED} ● {Fore.RESET}"

            x = self.coin_gravity(y)
            if x == -1:
                clear()
                print(f"\n{self}\n")
                print(f"Enter a column number to introduce your coin.\n{self.game.player_turn}'s turn.")
                print(f"{Fore.RED}This column is full, please choose another one.{Fore.RED}{Fore.RESET}")
                continue

            self.coins[x][y] = coin
            break

    def coin_gravity(self, y):
        """
        Return the row index where the coin should be placed by checking from bottom to top the first empty cell.
        """

        for i in range(5, -1, -1):
            if self.coins[i][y] == "   ":
                return i
        return -1


if __name__ == '__main__':
    main()
