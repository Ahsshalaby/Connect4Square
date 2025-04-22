import numpy as np
import pygame
import sys
import math
import random
import time
import tkinter
from tkinter import *

# from https://www.youtube.com/watch?v=d_MrsYUJPGI following way to make a GUI



#Set up first GUI window
Gui_window = Tk()
Gui_window.title("Connect 4 in a Box Menu")
Gui_window.columnconfigure(0, weight = 1)
Gui_window.columnconfigure(1, weight = 1)


#set name of player
name_label = Label(Gui_window, text = "Player name")
name_label.grid(column = 0, row = 2)
name_field = Entry()
name_field.grid(column=1, row=2)


name = "Player"

def getName():
	global name
	name = name_field.get()
	return name



#Submit Button
submit_button = Button(Gui_window, text = "Submit Name", command = getName )
submit_button.grid(column=0, row =3)


End_label = Label(Gui_window, text = "Close when done")
End_label.grid(column = 0, row = 4)
mainloop()


#Set up GUI window
Gui_window = Tk()
Gui_window.title("Connect 4 in a Box Menu")
Gui_window.columnconfigure(0, weight = 1)
Gui_window.columnconfigure(1, weight = 1)

# choosing who goes first with buttons and storing value
first_player_label = Label(Gui_window, text = "Who Goes First?")
first_player_label.grid(column = 0, row = 4)
first_player_var = IntVar()
radio_button_player = Radiobutton(Gui_window, text = name + " Goes First", padx = 20, 
	variable = first_player_var, value = 0)
radio_button_Ai = Radiobutton(Gui_window, text = "Ai Goes First", padx = 20, 
	variable = first_player_var, value = 1)
radio_button_player.grid(column = 0, row = 5)
radio_button_Ai.grid(column = 0, row = 6)

# choosing difficulty with dropdown and storing value
difficulty_label = Label(Gui_window, text = "What Difficulty 1-5")
difficulty_label.grid(column = 0, row = 8)
difficulty_list = [0,1,2,3,4,5]
difficulty_value = IntVar()
difficulty_menu = OptionMenu(Gui_window, difficulty_value, *difficulty_list)
difficulty_menu.grid(column=0, row=10, columnspan=2)

#Choose Gray Level with Scale Input and storing value
Gray_label = Label(Gui_window, text = "How Light do You want the Board")
Gray_label.grid(column = 0, row = 12)
Gray_variable = IntVar()
Gray_label_scale = Scale(Gui_window, from_ = 0, to= 15, variable = Gray_variable, orient=HORIZONTAL)
Gray_label_scale.grid(column = 0, row = 14, columnspan=2, sticky=W+E)

End_label = Label(Gui_window, text = "Close when done")
End_label.grid(column = 0, row =20)

mainloop()



moves = 0

G = Gray_variable.get() * 15 # DEGREE OF GRAY from GUI
GRAY = (G,G,G)

GREEN = (0, 255, 0)
WHITE = (255,255,255)

BLUE = (0,0,255) 
#BLACK = (0,0,0) 
RED = (255,0,0) 
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7


player = 0
Ai = 1

play_first_choice = first_player_var.get() # from GUI

playerPiece = 1
aiPiece = 2

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

# new function. replacing wining move with different requirements
def winning_move(board, piece):
	#need a box to win
	for c in range (COLUMN_COUNT-1):
		for r in range (ROW_COUNT - 1):
			if board[r][c] == piece and board[r][c+1] == piece and board [r+1][c] == piece and board[r+1][c+1] == piece:
				return True

# new function. implementing a draw function			
def draw_move(board):
	#if is not valid location for all rows. 
		if all(not is_valid_location(board, c) for c in range(COLUMN_COUNT)):
			return True

		

# scoring 

# gives scores based on positions for minmax function
# did not follow the tutorial as I think the four box is simpler to implement than four in a row
def score_position(board, piece):
	
	
	score = 0

	

	# if position is won. make sure to win
	for c in range (COLUMN_COUNT-1):
		for r in range (ROW_COUNT - 1):
			if board[r][c] == piece and board[r][c+1] == piece and board [r+1][c] == piece and board[r+1][c+1] == piece:
				score = score + 2000

	# having the AI preference putting peices, not alongside the 2 edges. since on edge less possible boxes
	edge_array1 = [int(i) for i in list(board[:, COLUMN_COUNT-1])]	
	edge_array2 = [int(i) for i in list(board[:, 0])]
	edge_count = edge_array1.count(piece) + edge_array2.count(piece) # counting either 1 or 2
	score = score - edge_count*3

	# prefer to have peices next to each other
	for c in range (COLUMN_COUNT-1):
		for r in range (ROW_COUNT - 1):
			if board[r][c] == piece and board[r][c+1] == piece:
				score = score + 25
	
	# prefer to have peices on top of each other
	for c in range (COLUMN_COUNT-1):
		for r in range (ROW_COUNT - 1):
			if board[r][c] == piece and board[r+1][c] == piece:
				score = score + 25

	# prefer three in a row that can result in victory
	for c in range (COLUMN_COUNT-1):
		for r in range (ROW_COUNT - 1):
			if board[r][c] == piece and board[r][c+1] == piece and board[r+1][c+1] == piece:
				score = score + 50

	# prefer three in a row that can result in victory
	for c in range (COLUMN_COUNT-1):
		for r in range (ROW_COUNT - 1):
			if board[r][c] == piece and board[r+1][c]== piece and board[r][c+1] == piece:
				score = score + 50	


	# needs to block opponent three in a row but not at expense of win. Basically if opponent has 3 in a row and our piece is not blocking it we lose 1000 points
	# this will urge AI to block an opponent 3 in a row
	for c in range (COLUMN_COUNT-1):
		for r in range (ROW_COUNT - 1):
			if board[r][c] == playerPiece and board[r][c+1] == playerPiece and board[r+1][c+1] == playerPiece and board[r+1][c] != piece:
				score = score - 1000
	
	# needs to block other opponent three in a row but not at expense of win
	for c in range (COLUMN_COUNT-1):
		for r in range (ROW_COUNT - 1):
			if board[r][c] == playerPiece and board[r+1][c]== playerPiece and board[r][c+1] == playerPiece and board[r+1][c + 1] != piece:
				score = score - 1000

	return score

#gives location avaiable to be placed
def get_valid_location(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board,col):
			valid_locations.append(col) # append locations to the array
	return valid_locations
	


def pick_best_move(board, piece):
	bestScore = 1
	valid_locations = get_valid_location(board) # makes an array of valid locations
	bestCol = random.choice(valid_locations)
	
	
	for col in valid_locations:
		row = get_next_open_row(board, col) # get open row in that column
		temp_board = board.copy() # copy is because pointers would modify original board
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > bestScore:
			bestScore = score
			bestCol = col
	return bestCol

def is_terminal_node(board):
	return winning_move(board, playerPiece) or winning_move(board, aiPiece) or draw_move(board)

#implementing the wikipedia / video minimax function
def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_location(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move (board, aiPiece):
				return (None, 100000)
			elif winning_move(board, playerPiece):
				return (None, -100000)
			else:
				return (None, 0) #draw
		else: #depth is 0
			return (None, score_position(board, aiPiece ))
	if maximizingPlayer: # if true
		value = -math.inf # maximizer starts at - infitiny
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			board_copy = board.copy()
			drop_piece(board_copy, row, col, aiPiece)
			new_score = minimax(board_copy, depth-1,alpha, beta, False)[1] # recursion
			if new_score > value:
				value = new_score
				column = col
			alpha = max(value, alpha)
			if alpha >= beta:
				break
		return column, value
	else: #minimizing
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			board_copy = board.copy()
			drop_piece(board_copy, row, col, playerPiece)
			new_score = minimax(board_copy, depth-1,alpha, beta, True)[1] # recursion
			if new_score < value:
				value = new_score
				column = col
			beta = min(value, beta)
			if alpha >= beta:
				break
		return column, value

'''''''''''

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

'''''''''


def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, GRAY, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, WHITE, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == playerPiece:
				pygame.draw.circle(screen, GREEN, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == aiPiece: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()


board = create_board()
print_board(board)
game_over = False

start = time.time()

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 25)

turn = play_first_choice 
while not game_over:


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, WHITE, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == 0:
				pygame.draw.circle(screen, GREEN, (posx, int(SQUARESIZE/2)), RADIUS)
			else: 
				pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, WHITE, (0,0, width, SQUARESIZE))
			#print(event.pos)
			# Ask for Player 1 Input
			if turn == player:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				# checking my draw_move function here
				if draw_move(board):
						end = time.time()
						time_pass = int(end - start)
						label = myfont.render("Draw ,time{}".format(time_pass) + "seconds {}".format(moves) + "moves" , 2, GREEN)
						screen.blit(label, (0,0))
						game_over = True

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, playerPiece) 
					moves = moves + 1
					turn += 1 # moved change turn function only AFTER a correct tile placed. This way turn does not pass after clicking on full column
					turn = turn % 2

					if winning_move(board, playerPiece):
						end = time.time()
						time_pass = int(end - start)
						label = myfont.render(f"{name} wins! ,time {time_pass} seconds, {moves} moves", True, GREEN) # changed label format here to include player name
						screen.blit(label, (0,0))
						game_over = True
						
			

				print_board(board)
				draw_board(board)		
						
							


 
			# Ask for ai Input
	if turn == Ai and not game_over:				
		
		
		if difficulty_value.get() == 0: # if 0 from GUI make random moves
			col = random.randint(0,COLUMN_COUNT-1)
		else: # diffculty = level of depth
			col, minimax_score = minimax(board, difficulty_value.get(), -math.inf, math.inf, True)

		#check if draw before Ai plays
		if draw_move(board):
						end = time.time()
						time_pass = int(end - start)
						label = myfont.render("Draw ,time{}".format(time_pass) + "seconds {}".format(moves) + "moves" , 1, GREEN)
						screen.blit(label, (0,0))
						game_over = True
	
		if is_valid_location(board, col):
			#pygame.time.wait(150) # delay
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, aiPiece)
			moves = moves + 1
			turn += 1
			turn = turn % 2	
			# moving turn here so that the ai has to place a valid move before switch turn

			if winning_move(board, aiPiece):
						end = time.time()
						time_pass = int(end - start)
						label = myfont.render("AI wins! ,time{}".format(time_pass) + "seconds {}".format(moves) + "moves" , 2, GREEN)
						screen.blit(label, (0,0))
						game_over = True

						

		print_board(board)
		draw_board(board)

	
		

	if game_over:
		pygame.time.wait(10000)
		
