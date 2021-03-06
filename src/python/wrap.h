/*
 * wrap.h
 *
 *  Created on: 9 באוג 2013
 *      Author: eli
 */

#ifndef WRAP_H_
#define WRAP_H_

#include <string>
#include <vector>

class Board {
public:
	Board(const std::string& solution, size_t block_width, size_t block_height);
	Board(const std::string& problem, const std::string& solution,
			size_t block_width, size_t block_height);

	const std::string& get_problem() const;
	const std::string& get_solution() const;

	size_t get_block_width() const;
	size_t get_block_height() const;

	char get(size_t x, size_t y, bool solution) const;
	char get_problem(size_t x, size_t y) const;
	char get_solution(size_t x, size_t y) const;
private:
	std::string m_problem;
	std::string m_solution;

	size_t      m_block_width;
	size_t      m_block_height;

	size_t calc_index(size_t x, size_t y) const;
};

std::vector<Board> create_board(size_t block_width, size_t block_height,
		size_t num_boards);
Board create_board(size_t block_width, size_t block_height);

#endif /* WRAP_H_ */
