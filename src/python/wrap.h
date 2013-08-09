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
	Board(const std::string& solution);
	Board(const std::string& problem, const std::string& solution);

	const std::string& get_problem() const;
	const std::string& get_solution() const;
private:
	std::string m_problem;
	std::string m_solution;
};

std::vector<Board> create_board(size_t block_width, size_t block_height,
		size_t num_boards);
Board create_board(size_t block_width, size_t block_height);

#endif /* WRAP_H_ */
