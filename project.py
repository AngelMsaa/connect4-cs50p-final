import os
from colorama import Fore
from terminaltables import SingleTable


def main():
    clear()
    Game(start_game())


def start_game():
    '''Start the game by getting the board size.'''

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
    '''Clear the terminal.'''
    os.system('cls' if os.name == 'nt' else 'clear')


class Game:
    '''
    The main game class that manages the game loop and the turn system.
    '''

    def __init__(self, size, input_test=input):
        self.board = Board(self, size, input_test)
        self.turn = "Yellow"
        self.turn_count_yellow = 0
        self.turn_count_red = 0
        self.input_test = input_test  # To provide custom input during testing
        self.game_loop()

    def game_loop(self):
        '''
        The main game loop that manages the game turns and checks for a win or draw.
        '''

        while True:
            clear()
            print(f"\n{self.board}\n")
            self.board.place_coin()
            if self.check_win():
                break
            elif self.check_draw():
                break

    def turn_manager(self):

        '''
        Switch the turn between Yellow and Red.
        '''

        if self.turn == "Yellow":
            self.turn_count_yellow += 1
            self.turn = "Red"
        else:
            self.turn = "Yellow"
            self.turn_count_red += 1

    def check_win(self):

        '''
        Check if there is a win by checking horizontal, vertical, and diagonal wins.
        '''

        coins_list = self.board.coins
        for row_index, row_data in enumerate(coins_list):
            for col_index, value in enumerate(row_data):
                if "●" in value:
                    if (check_horizontal_win(row_data, col_index) or
                            check_vertical_win(coins_list, row_index, col_index) or
                            check_diagonal_win(coins_list, row_index, col_index)):
                        winner_turns = str((self.turn_count_yellow if self.turn == "Yellow" else self.turn_count_red) + 1)
                        clear()
                        print(f"\n{self.board}\n")
                        if self.turn == "Yellow":
                            print(f"{Fore.RED}RED{Fore.GREEN} won in {winner_turns} moves!")
                        elif self.turn == "Red":
                            print(f"{Fore.YELLOW}YELLOW{Fore.GREEN} won in {winner_turns} moves!")
                        return True
        return False

    def check_draw(self):
        '''
        Check if the game is a draw.
        '''

        if all("●" in value for row in self.board.coins for value in row):
            clear()
            print(f"\n{self.board}\n")
            print(f"{Fore.BLUE}DRAW!{Fore.BLUE}")
            return True
        return False


class Board:
    '''
    The board class that manages the game board and the coin placement.
    '''

    def __init__(self, game, size=7, input_test=input):
        self.game = game
        self.size = int(size)
        self.board_height = 6
        self.coins = [["   " for _ in range(self.size)] for _ in range(self.board_height)]
        self.input_test = input_test
        self.table = SingleTable(self.coins)
        self.table.inner_row_border = True

    def __str__(self):
        return self.table.table

    def place_coin(self, column=None):
        '''
        Place a coin in the selected column.
        '''

        print(f"Enter a column number to introduce your coin.\n{self.game.turn}'s turn.")
        while True:
            if column is None:
                y = self.input_test(f"\n{Fore.RESET}>>> {Fore.RESET}")
                try:
                    y = int(y) - 1
                except ValueError:
                    clear()
                    print(f"\n{self}\n")
                    print(f"Enter a column number to introduce your coin.\n{self.game.turn}'s turn.")
                    print(f"{Fore.RED}Invalid input, please enter a number between 1 and {self.size}.{Fore.RED}{Fore.RESET}")
                    continue
            else:
                y = column
                column = None

            if y < 0 or y >= len(self.coins[0]):
                clear()
                print(f"\n{self}\n")
                print(f"Enter a column number to introduce your coin.\n{self.game.turn}'s turn.")
                print(f"{Fore.RED}Invalid column number, please enter a valid one (1 to {self.size}).{Fore.RED}{Fore.RESET}")
                continue

            if self.game.turn == "Yellow":
                coin = f"{Fore.YELLOW} ● {Fore.RESET}"
            else:
                coin = f"{Fore.RED} ● {Fore.RESET}"

            x = self.coin_gravity_x(y)
            if x == -1:
                clear()
                print(f"\n{self}\n")
                print(f"Enter a column number to introduce your coin.\n{self.game.turn}'s turn.")
                print(f"{Fore.RED}This column is full, please choose another one.{Fore.RED}{Fore.RESET}")
                continue

            self.coins[x][y] = coin
            self.game.turn_manager()
            break

    def coin_gravity_x(self, y):
        '''
        Apply gravity to the coin and return the row index.
        '''

        for i in range(5, -1, -1):
            if self.coins[i][y] == "   ":
                return i
        return -1


def check_horizontal_win(h_row_data, h_col_index):
    '''
    Check if there is a horizontal win.
    '''

    try:
        if h_row_data[h_col_index] == h_row_data[h_col_index + 1] == h_row_data[h_col_index + 2] == h_row_data[h_col_index + 3] != "   ":
            return True
        return False
    except IndexError:
        return False


def check_vertical_win(v_coins_list, v_row_index, v_col_index):
    '''
    Check if there is a vertical win.
    '''

    try:
        if v_row_index + 3 < len(v_coins_list) and v_coins_list[v_row_index][v_col_index] == v_coins_list[v_row_index + 1][v_col_index] == v_coins_list[v_row_index + 2][v_col_index] == v_coins_list[v_row_index + 3][v_col_index] != "   ":
            return True
        return False
    except IndexError:
        return False


def check_diagonal_win(d_coins_list, d_row_index, d_col_index):
    '''
    Check if there is a diagonal win.
    '''

    try:
        if d_row_index + 3 < len(d_coins_list) and d_col_index + 3 < len(d_coins_list[d_row_index]) and d_coins_list[d_row_index][d_col_index] == d_coins_list[d_row_index + 1][d_col_index + 1] == d_coins_list[d_row_index + 2][d_col_index + 2] == d_coins_list[d_row_index + 3][d_col_index + 3] != "   ":
            return True
        if d_row_index + 3 < len(d_coins_list) and d_col_index - 3 >= 0 and d_coins_list[d_row_index][d_col_index] == d_coins_list[d_row_index + 1][d_col_index - 1] == d_coins_list[d_row_index + 2][d_col_index - 2] == d_coins_list[d_row_index + 3][d_col_index - 3] != "   ":
            return True
        return False
    except IndexError:
        return False


if __name__ == '__main__':
    main()
