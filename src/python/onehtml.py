#!/usr/bin/python

import os

html_header = "<html><head><title>Sudoku</title><style type=\"text/css\">table.main{border-collapse:collapse;border:4pt solid black}table.lower{border-collapse:collapse;border:2pt solid black}td{border:1pt solid black;padding:0pt 0pt 0pt 0pt;font-size:20pt}div.head{font-size:20pt;font-weigth:bold}p.pagebreak{page-break-before:always}</style></head><body>"
html_footer = "</body></html>"

game_header = "<center><div class=\"head\">Eli Daian's Sudoku</div></center><center><table width=\"420\" height=\"420\" class=\"main\">"
game_footer1 = "</table></center><center><i>"
game_footer2 = "</i></center><p class=\"pagebreak\"></p>"

blocks_line_header = "<tr height=\"4%\">"
blocks_line_footer = "</tr>"

block_header = "<td width=\"33%\"><table width=\"100%\" height=\"100%\" class=\"lower\">"
block_footer = "</table></td>"

inblock_line_header = "<tr height=\"33%\">"
inblock_line_footer = "</tr>"

inblock_cell_header = "<td width=\"25%\" align=\"center\">"
inblock_cell_footer = "</td>"

dir_name = raw_input('What is the dirname? ')
out_name = raw_input('What is the output file name? ')
block_width = input('What is the block width? ')
block_height = input('What is the block height? ')

line_size = block_width * block_height

fout = file(out_name,'w')
fout.write(html_header)

dir_files = os.listdir(dir_name)

for filename in dir_files:
	if filename[-8:]=='-raw.txt':
		in_lines = file(dir_name+os.sep+filename, 'r').read().splitlines()
		if in_lines[2]=='#':		# Good file
			game_name = in_lines[1][:-8]
			game = in_lines[3]
			
			fout.write(game_header)
			
			# Organize game matrix
			game_matrix = [[]]
			col = 0
			for c in game:
				if col == line_size:
					game_matrix.append([])
					col = 0
				
				if c == '.':
					to_append = '&nbsp;'
				else:
					to_append = c
				game_matrix[-1].append(to_append);
				
				col += 1
			
			for blocks_line in xrange(block_width):
				fout.write(blocks_line_header)
				
				line1 = block_height * blocks_line
				for blocks_col in xrange(block_height):
					fout.write(block_header)
					
					col1 = block_width * blocks_col
					for inblock_line in xrange(block_height):
						fout.write(inblock_line_header)
						
						line = line1 + inblock_line
						for inblock_col in xrange(block_width):
							fout.write(inblock_cell_header)
							
							col = col1 + inblock_col
							fout.write(game_matrix[line][col])
							
							fout.write(inblock_cell_footer)
						
						fout.write(inblock_line_footer)
					
					fout.write(block_footer)
				
				fout.write(blocks_line_footer)
			
			fout.write(game_footer1)
			fout.write(game_name)
			fout.write(game_footer2)

fout.write(html_footer)
fout.close()
