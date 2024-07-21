import pytest
from project import start_game, get_board_size, clear
from unittest.mock import patch

def test_start_game():
    with patch('builtins.input', return_value='4'):
        assert isinstance(start_game(), int)

def test_get_board_size():
    with patch("builtins.input", return_value="4"):
        size = get_board_size()
        assert isinstance(size, int)
        assert 4 <= size <= 50

def test_clear():
    assert callable(clear)