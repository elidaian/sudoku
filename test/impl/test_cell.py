import pytest

from sudoku.exceptions import SymbolNotPossible
from sudoku.impl import Cell

__author__ = "Eli Daian <elidaian@gmail.com>"


def test_cell_legal_alphabet(alphabet):
    cell = Cell(0, 0, alphabet, "2")


def test_cell_illegal_alphabet(alphabet):
    with pytest.raises(SymbolNotPossible):
        cell = Cell(0, 0, alphabet, "A")


def test_cell_set_symbol_legal_at_first_time(alphabet):
    cell = Cell(0, 0, alphabet)

    cell.set_symbol("1")
    with pytest.raises(SymbolNotPossible):
        cell.set_symbol("2")


def test_cell_set_symbol_illegal1(alphabet):
    cell = Cell(0, 0, alphabet, "2")

    with pytest.raises(SymbolNotPossible):
        cell.set_symbol("a")


def test_cell_set_symbol_illegal2(alphabet):
    cell = Cell(0, 0, alphabet)

    with pytest.raises(SymbolNotPossible):
        cell.set_symbol("a")
