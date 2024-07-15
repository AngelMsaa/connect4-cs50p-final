import pytest
from unittest.mock import patch
from colorama import Fore
from project import Game, Board, get_board_size

def test_board_initialization():
    board = Board(None, size=7)
    assert board.size == 7
    assert len(board.coins) == 6
    assert all(len(row) == 7 for row in board.coins)

@patch('project.get_board_size', return_value=7)
def test_game_initialization(mock_get_board_size):
    game = Game(size=7, input_test=lambda _: "1")
    assert game.turn == "Yellow"
    assert game.turn_count_yellow == 0
    assert game.turn_count_red == 0

@patch('project.get_board_size', return_value=7)
def test_turn_manager(mock_get_board_size):
    game = Game(size=7, input_test=lambda _: "1")
    initial_turn = game.turn
    game.turn_manager()
    assert game.turn != initial_turn
    game.turn_manager()
    assert game.turn == initial_turn

def test_coin_gravity():
    board = Board(None, size=7)
    x = board.coin_gravity_x(2)
    board.coins[x][2] = Fore.YELLOW + " ● " + Fore.RESET
    assert board.coins[5][2] == Fore.YELLOW + " ● " + Fore.RESET

@patch('project.get_board_size', return_value=7)
def test_place_coin(mock_get_board_size):
    game = Game(size=7, input_test=lambda _: "1")
    board = game.board
    game.turn = "Yellow"
    board.coins[5][0] = "   "
    with patch('builtins.input', return_value='1'):  # Mock input to simulate placing a coin in column 1
        board.place_coin()
    assert board.coins[5][0] == Fore.YELLOW + " ● " + Fore.RESET
    assert game.turn == "Red"  # Check if turn switched correctly

@patch('project.get_board_size', return_value=7)
def test_check_horizontal_win(mock_get_board_size):
    game = Game(size=7, input_test=lambda _: "1")
    game.board.coins = [
        ["   ", "   ", "   ", "   ", "   ", "   ", "   "],
        ["   ", "   ", "   ", "   ", "   ", "   ", "   "],
        ["   ", "   ", "   ", "   ", "   ", "   ", "   "],
        ["   ", "   ", "   ", "   ", "   ", "   ", "   "],
        ["   ", "   ", "   ", "   ", "   ", "   ", "   "],
        ["   ", "   ", "   ", "   ", "   ", "   ", "   "]
    ]
    assert game.check_win() == False

    game.board.coins[5][0] = Fore.YELLOW + " ● " + Fore.RESET
    game.board.coins[5][1] = Fore.YELLOW + " ● " + Fore.RESET
    game.board.coins[5][2] = Fore.YELLOW + " ● " + Fore.RESET
    game.board.coins[5][3] = Fore.YELLOW + " ● " + Fore.RESET
    assert game.check_win() == True

@patch('project.get_board_size', return_value=7)
def test_check_vertical_win(mock_get_board_size):
    game = Game(size=7, input_test=lambda _: "1")
    game.board.coins = [
        ["   ", "   ", "   ", "   ", "   ", "   ", "   "],
        ["   ", "   ", "   ", "   ", "   ", "   ", "   "],
        ["   ", "   ", "   ", "   ", "   ", "   ", "   "],
        ["   ", "   ", "   ", "   ", "   ", "   ", "   "],
        ["   ", "   ", "   ", "   ", "   ", "   ", "   "],
        ["   ", "   ", "   ", "   ", "   ", "   ", "   "]
    ]
    assert game.check_win() == False

    game.board.coins[5][0] = Fore.YELLOW + " ● " + Fore.RESET
    game.board.coins[4][0] = Fore.YELLOW + " ● " + Fore.RESET
    game.board.coins[3][0] = Fore.YELLOW + " ● " + Fore.RESET
    game.board.coins[2][0] = Fore.YELLOW + " ● " + Fore.RESET
    assert game.check_win() == True

@patch('project.get_board_size', return_value=7)
def test_check_diagonal_win(mock_get_board_size):
    game = Game(size=7, input_test=lambda _: "1")
    game.board.coins = [
        ["   ", "   ", "   ", "   ", "   ", "   ", "   "],
        ["   ", "   ", "   ", "   ", "   ", "   ", "   "],
        ["   ", "   ", "   ", "   ", "   ", "   ", "   "],
        ["   ", "   ", "   ", "   ", "   ", "   ", "   "],
        ["   ", "   ", "   ", "   ", "   ", "   ", "   "],
        ["   ", "   ", "   ", "   ", "   ", "   ", "   "]
    ]
    assert game.check_win() == False

    game.board.coins[5][0] = Fore.YELLOW + " ● " + Fore.RESET
    game.board.coins[4][1] = Fore.YELLOW + " ● " + Fore.RESET
    game.board.coins[3][2] = Fore.YELLOW + " ● " + Fore.RESET
    game.board.coins[2][3] = Fore.YELLOW + " ● " + Fore.RESET
    assert game.check_win() == True

@patch('project.get_board_size', return_value=7)
def test_check_draw(mock_get_board_size):
    game = Game(size=7, input_test=lambda _: "1")
    game.board.coins = [
        [Fore.YELLOW + " ● " + Fore.RESET, Fore.RED + " ● " + Fore.RESET, Fore.YELLOW + " ● " + Fore.RESET, Fore.RED + " ● " + Fore.RESET, Fore.YELLOW + " ● " + Fore.RESET, Fore.RED + " ● " + Fore.RESET, Fore.YELLOW + " ● " + Fore.RESET],
        [Fore.RED + " ● " + Fore.RESET, Fore.YELLOW + " ● " + Fore.RESET, Fore.RED + " ● " + Fore.RESET, Fore.YELLOW + " ● " + Fore.RESET, Fore.RED + " ● " + Fore.RESET, Fore.YELLOW + " ● " + Fore.RESET, Fore.RED + " ● " + Fore.RESET],
        [Fore.YELLOW + " ● " + Fore.RESET, Fore.RED + " ● " + Fore.RESET, Fore.YELLOW + " ● " + Fore.RESET, Fore.RED + " ● " + Fore.RESET, Fore.YELLOW + " ● " + Fore.RESET, Fore.RED + " ● " + Fore.RESET, Fore.YELLOW + " ● " + Fore.RESET],
        [Fore.RED + " ● " + Fore.RESET, Fore.YELLOW + " ● " + Fore.RESET, Fore.RED + " ● " + Fore.RESET, Fore.YELLOW + " ● " + Fore.RESET, Fore.RED + " ● " + Fore.RESET, Fore.YELLOW + " ● " + Fore.RESET, Fore.RED + " ● " + Fore.RESET],
        [Fore.YELLOW + " ● " + Fore.RESET, Fore.RED + " ● " + Fore.RESET, Fore.YELLOW + " ● " + Fore.RESET, Fore.RED + " ● " + Fore.RESET, Fore.YELLOW + " ● " + Fore.RESET, Fore.RED + " ● " + Fore.RESET, Fore.YELLOW + " ● " + Fore.RESET],
        [Fore.RED + " ● " + Fore.RESET, Fore.YELLOW + " ● " + Fore.RESET, Fore.RED + " ● " + Fore.RESET, Fore.YELLOW + " ● " + Fore.RESET, Fore.RED + " ● " + Fore.RESET, Fore.YELLOW + " ● " + Fore.RESET, Fore.RED + " ● " + Fore.RESET]
    ]
    assert game.check_draw() == True

def test_invalid_column():
    board = Board(None, size=7)
    for i in range(6):
        board.coins[i][0] = Fore.YELLOW + " ● " + Fore.RESET
    assert board.coin_gravity_x(0) == -1

def test_get_board_size():
    with patch('builtins.input', return_value='7'):
        size = get_board_size()
        assert size == 7

    with patch('builtins.input', side_effect=['invalid', '51', '4']):
        size = get_board_size()
        assert size == 4

if __name__ == '__main__':
    pytest.main(['-s'])
