/*
 * wrap.cc
 *
 *  Created on: 9 באוג 2013
 *      Author: eli
 */

#include "wrap.h"

#include <algorithm>
#include <iterator>
#include <stdexcept>

#include <boost/bind.hpp>
#include <boost/iterator/counting_iterator.hpp>
#include <boost/random/mersenne_twister.hpp>
#include <boost/random/uniform_int.hpp>
#include <boost/ref.hpp>
#include <boost/scoped_array.hpp>
#include <boost/shared_ptr.hpp>

#include <sudoku-pub.h>

namespace {

class BoardGenerator {
public:
	BoardGenerator(size_t block_width, size_t block_height);
	~BoardGenerator();

	Board generate(size_t);

private:
	static const size_t          MAX_TRIALS = 16;

	t_board_p                    m_board;
	int                          m_num_cells;
	int                          m_num_symbols;
	boost::scoped_array<size_t>  m_cells;
	boost::scoped_array<size_t>  m_symbols;
	boost::scoped_array<char>    m_given;
	boost::mt19937               m_random_generator;

	size_t                       m_block_width;
	size_t                       m_block_height;

	size_t rnd(size_t max);
	size_t rnd(size_t min, size_t max);
};

BoardGenerator::BoardGenerator(size_t block_width, size_t block_height):
		m_board(ConstructCustomBoard(block_width, block_height,
				FALSE, 0 ,NULL, NULL)),
		m_num_cells(m_board != NULL ? GetNumCells(m_board) : 0),
		m_num_symbols(m_board != NULL ? GetNumSymbols(m_board) : 0),
		m_cells(new size_t[m_num_cells]),
		m_symbols(new size_t[m_num_cells]),
		m_given(new char[m_num_cells]),
		m_block_width(block_width),
		m_block_height(block_height) {
	if (m_board == NULL) {
		throw std::bad_alloc();
	}
}

BoardGenerator::~BoardGenerator() {
	if (m_board != NULL) {
		DestroyBoard(m_board);
	}
}

Board BoardGenerator::generate(size_t) {
	CleanBoard(m_board);

	size_t n = 0;
	size_t trials = 0;
	e_state state;

	// This loop generates a solved board
	do {
		size_t cell;
		do {
			cell = rnd(m_num_cells);
		} while (GetNumPossValuesOfCell(m_board, cell) == 1);

		size_t symbol = rnd(GetNumPossValuesOfCell(m_board, cell));
		for (size_t i = 0, j = 0; i < m_num_symbols; ++i) {
			if (GetPossValuesOfCell(m_board, cell) & (1ul << i)) {
				if (j == symbol) {
					symbol = i;
					break;
				} else {
					++j;
				}
			}
		}
		SetSymbolInCell(m_board, symbol, cell);

		Solve(m_board, 0, FALSE);
		state = GetState(m_board);

		if (state == impossible) {
			CleanBoard(m_board);
			if (trials < MAX_TRIALS) {
				for (size_t i = 0; i < n; ++i) {
					SetSymbolInCell(m_board, m_symbols[i], m_cells[i]);
				}
				++trials;
			} else {
				n = trials = 0;
			}
			continue;
		}

		m_symbols[n] = symbol;
		m_cells[n] = cell;
		++n;
	} while(state != solved);

	// Do something wiered (TODO)
	size_t j = 0;
	while (j < n) {
		CleanBoard(m_board);
		for (size_t i = 0; i < n; ++i) {
			if (i != j) {
				SetSymbolInCell(m_board, m_symbols[i], m_cells[i]);
			}
		}
		Solve(m_board, 0, FALSE);
		if (GetState(m_board) == solved) {
			--n;
			// TODO s = 1; ?
			for (size_t i = j; i < n; ++i) {
				m_symbols[i] = m_symbols[i+1];
				m_cells[i] = m_cells[i+1];
			}
		} else {
			++j;
		}
	}

	// Do something wiered (TODO)
	CleanBoard(m_board);
	for (size_t i = 0; i < n; ++i) {
		SetSymbolInCell(m_board, m_symbols[i], m_cells[i]);
	}
	Solve(m_board, 0, FALSE);
	if (!GetNumRulesNGt1(m_board)) {
		size_t k = rnd(m_num_cells / 5, m_num_cells / 2);
		std::fill(m_given.get(), m_given.get() + m_num_cells, 0);
		for (size_t i = 0; i < n; ++i) {
			m_given[m_cells[i]] = 1;
		}

		if (n < k) {
			for (; n < k; ++n) {
				size_t cell;
				do {
					cell = rnd(m_num_cells);
				} while (m_given[cell]);
				m_symbols[n] = GetSymbolOfCell(m_board, cell);
				m_cells[n] = cell;
				m_given[n] = 1;
				++n;
			}
		}
	}

	// Fill the board and get the problem
	CleanBoard(m_board);
	for (size_t i = 0; i < n; ++i) {
		SetSymbolInCell(m_board, m_symbols[i], m_cells[i]);
	}
	GetBoardRaw(m_board, m_given.get(), NULL, " X");
	std::string problem(m_given.get(), m_num_cells);

	// Solve the board and get the solution
	Solve(m_board, 0, FALSE);
	GetBoardRaw(m_board, m_given.get(), NULL, " X");
	std::string solution(m_given.get(), m_num_cells);

	return Board(problem, solution, m_block_width, m_block_height);
}

size_t BoardGenerator::rnd(size_t max) {
	return rnd(0, max);
}

size_t BoardGenerator::rnd(size_t min, size_t max) {
	boost::uniform_int<size_t> dist(min, max - 1);
	return dist(m_random_generator);
}

}  // anonymous namespace

Board::Board(const std::string& solution, size_t block_width, size_t block_height):
		m_problem(solution),
		m_solution(solution),
		m_block_width(block_width),
		m_block_height(block_height) {
	// Nothing here
}

Board::Board(const std::string& problem, const std::string& solution,
		size_t block_width, size_t block_heght):
		m_problem(problem),
		m_solution(solution),
		m_block_width(block_width),
		m_block_height(block_heght) {
	// Nothing here
}

const std::string& Board::get_problem() const {
	return m_problem;
}

const std::string& Board::get_solution() const {
	return m_solution;
}

size_t Board::get_block_width() const {
	return m_block_width;
}

size_t Board::get_block_height() const {
	return m_block_height;
}

char Board::get(size_t x, size_t y, bool solution) const {
	if (solution) {
		return get_solution(x, y);
	} else {
		return get_problem(x, y);
	}
}

char Board::get_problem(size_t x, size_t y) const {
	return m_problem[calc_index(x, y)];
}

char Board::get_solution(size_t x, size_t y) const {
	return m_solution[calc_index(x, y)];
}

size_t Board::calc_index(size_t x, size_t y) const {
	size_t line_width = m_block_width * m_block_height;
	return x + y * line_width;
}

std::vector<Board> create_board(size_t block_width, size_t block_height,
		size_t num_boards) {
	BoardGenerator generator(block_width, block_height);
	std::vector<Board> res;
	res.reserve(num_boards);
	std::transform(boost::counting_iterator<size_t>(0),
			boost::counting_iterator<size_t>(num_boards),
			std::back_inserter(res),
			boost::bind(&BoardGenerator::generate, boost::ref(generator), _1));
	return res;
}

Board create_board(size_t block_width, size_t block_height) {
	return create_board(block_width, block_height, 1)[0];
}
