

no_of_games = 1000
depth = 8


# board[]
# col
# player = human 1
# comp 2
def montecarlomove(board)
	possible_moves = [0] * board_width

	board1 = copy.deepcopy(board)

	for evalcol in board_width:
		
		if lowest_space(board, evalcol) == -1
			possible_moves[evalcol] = -100000
			continue

		else
			lowestrow = lowest_space(board, evalcol)
			board[evalcol][lowestrow] = 2
			board2 = copy.deepcopy(board)
			if currentmove_win(2 , board, currcol, currrow):  ##
				possible_moves[evalcol] = 100000
				continue

			sum1 = 0
			board2 = copy.deepcopy(board)
			for games in no_of_games:
				stage = 0
				
				for stage in depth:
					if is_full(board):
						break
					
					else:
						if stage%2 == 1:
							
							
							currcol = random.randit(0, board_width-1)
							currrow = lowest_space(board, currcol)
							while currrow == -1:		#### Check if board gets full
								currcol = random.randit(0, board_width-1)
								currrow = lowest_space(board, currcol)
							board[currcol][currrow] = 2

							if currentmove_win(2 , board, currcol, currrow):  ##
								sum1 += 10*(depth - stage)
								break

						else:
							
							
							currcol = random.randit(0,board_width-1)
							currrow = lowest_space(board, currcol)
							while currrow == -1:		#### Check if board gets full
								currcol = random.randit(0,board_width-1)
								currrow = lowest_space(board, currcol)
							board[currcol][currrow] = 1

							if currentmove_win(1, board, currcol, currrow):  ##
								sum1 -= 10*(depth - stage)
								break
		
				
				board = copy.deepcopy(board2)
		possible_moves[evalcol] = sum1
		board = copy.deepcopy(board1)

	maxvalue = possible_moves[maxcol] 
	maxcol = 0
		for col in board_width:
			if maxvalue < possible_moves[col]:
				maxvalue = possible_moves[col]
				maxcol = col

	return maxcol

def currentmove_win(player, board, col, row)
	#code for checking horizontal connections
	if col+3 < board_width:
		if board[col][row] == board[col+1][row] == board[col+2][row] == board[col+3][row] == player:
			return True
	if col-3 >= 0:
		if board[col][row] == board[col-1][row] == board[col-2][row] == board[col-3][row] == player:
			return True
	# code for checking vertical connections
	if row+3 < board_height:
		if board[col][row] == if board[col][row+1] == board[col][row+2] == board[col][row+3] == player:		
			return True
	if row-3 >= 0:
		if board[col][row] == board[col][row-1] == board[col][row-2] == board[col][row-3] == player:
			return True
	# code for checking diagonal connections
	
	if row+3 < board_height and col+3 < board_width:
		if board[col][row] == board[col+1][row+1] == board[col+2][row+2] == board[col+3][row+3] == player:		
			return True
	if row+3 < board_height and col-3 >= 0:
		if board[col][row] == board[col-1][row+1] == board[col-2][row+2] == board[col-3][row+3] == player:		
			return True
	if row-3 >= 0 and col+3 < board_width:
		if board[col][row] == board[col+1][row-1] == board[col+2][row-2] == board[col+3][row-3] == player:		
			return True
	if row-3 >= 0 and col-3 >= 0:
		if board[col][row] == board[col-1][row-1] == board[col-2][row-2] == board[col-3][row-3] == player:		
			return True
	return False
