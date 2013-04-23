#
#	GameBoard module
#	-
#	Represent a board to play on using a 2d array from NumPy
# 	NumPy : http://sourceforge.net/projects/numpy/files/NumPy/1.7.1/
#
#	Author: Tom Renn
#
import numpy as np
import nodeModule

BOARD_WIDTH = 7
BOARD_HEIGHT = 6
EMPTY_SPOT = 0

class GameBoard:

	# Constructor
	# If no board is given, create one containing all 0s
	def __init__(self, baseBoard=None):
		if baseBoard is None:
			self.board = np.zeros( (BOARD_HEIGHT, BOARD_WIDTH), dtype=np.int16)
		else:
			self.board = baseBoard

	# place chip in a given column index
	# return (row, col) of newly placed chip, or (-1, -1) if unable to be placed
	def moveAt(self, index, player):
		if index not in range(BOARD_WIDTH):
			return (-1, -1)
		
		# go from bottom of the board up
		for i in reversed(range(BOARD_HEIGHT)):
			row = self.board[i] 
			if row[index] == EMPTY_SPOT:	# found empty row
				row[index] = player
				return (i, index)
			else:							# row occupied 
				continue

		# if we got this far, the move is not able to be made
		return (-1, -1)

	# return the chip at the given row and column
	# returns EMPTY_SPOT if board bounds are exceeded
	def getChipAt(self, row, col):
		if row >= 0 and row < BOARD_HEIGHT:
			if col >= 0 and col < BOARD_WIDTH:
				return self.board[row][col]
		return EMPTY_SPOT

	# return indexes of available moves
	def getAvailableMoves(self):
		movesAvailable = []
		for i in range(BOARD_WIDTH):
			if self.board[0][i] == EMPTY_SPOT:
				movesAvailable.append(i)
		return movesAvailable

	# prints the gameboard in a nice format
	def fancyPrint(self):
		for row in range(BOARD_HEIGHT):
			rowString = '|'
			for col in range(BOARD_WIDTH):
				pos = self.board[row][col]
				if pos == EMPTY_SPOT:
					# if bottom row and empty show _ 
					if row == (BOARD_HEIGHT - 1):
						pos = '_'
					else:
						pos = ' '
				elif pos == nodeModule.PLAYER_MIN:
					pos = 'P'
				else:
					pos = 'C'
				rowString = rowString + pos + '|'
			print rowString
		# print index on bottom
		rowString = '|'
		for row in range(BOARD_WIDTH):
			rowString = rowString + str(row) + '|'
		print rowString

	# number of available moves
	def availableMoves(self):
		count = 0
		for i in range(BOARD_WIDTH):
			if self.board[0][i] == EMPTY_SPOT:
				count = count + 1
		return count
