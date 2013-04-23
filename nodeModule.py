#
#	Node module
#	-
#	Represent the state of connect4 at a single point
#	Each node contains the current GameBoard, current player, lastMove, and alpha and beta values
#	Note: Nodes keep track of PLAYER_MAX moves for calculation of the heuristic algorithm
#	
#	Author: Tom Renn
#
import gameboard as gb
import copy
import sys
PLAYER_MAX = 1
PLAYER_MIN = -1
WINNING_SUM = 4

class Node:

	# constructor
	# creates a root node with no parent given
	# creates a child node when parent and moveIndex are provided
	def __init__(self, parent=None, moveIndex=None):
		self.parent = parent
		if parent is None:		# create root node
			self.gameboard = gb.GameBoard()
			self.maxPlayerMoves = []
			self.player = PLAYER_MIN
			self.alpha = -10000
			self.beta = 10000
		else: 					# create child node from parent and new chip position
			# copy parent state information
			self.gameboard = copy.deepcopy(parent.gameboard)
			self.maxPlayerMoves = copy.deepcopy(parent.maxPlayerMoves)
			self.alpha = copy.copy(parent.alpha)
			self.beta = copy.copy(parent.beta)
			# switch player of this node
			self.player = parent.player * -1

		# place the chip the parent placed
		if moveIndex is not None:
			newChipLocation = self.gameboard.moveAt(moveIndex, parent.getPlayerSign())
			if parent.player == PLAYER_MAX:
				self.maxPlayerMoves.append(newChipLocation)
			self.lastMove = newChipLocation

	# find out if the game is over from the lastMove 
	def isGameOver(self):
		horizontal = self.scoreHorizontal(self.lastMove)
		vertical = self.scoreVertical(self.lastMove)
		dLeft = self.scoreLeftDiagonal(self.lastMove)
		dRight = self.scoreRightDiagonal(self.lastMove)
		if horizontal >= WINNING_SUM or \
		   vertical >= WINNING_SUM	 or \
		   dLeft >= WINNING_SUM 	 or \
		   dRight >= WINNING_SUM:
			return True
		else:
			return False

	# resets the alpha-beta values of this node
	def resetAlphaBeta(self):
		self.alpha = -10000
		self.beta = 10000

	# sums up all connected chips in the possible directions
	# : Horizontal, Vertical, Left Diagonal, Right Diagonal
	# For each direction, sum the connected chip score for each chip line
	# To prevent chips from being counted more than once, scoring methods are 
	# given a copy of the moveList and remove chips that are counted
	def heuristic2(self):
		h = 0
		maxMoves = copy.deepcopy(self.maxPlayerMoves)
		while len(maxMoves) > 0:
			horizontal = self.scoreHorizontal(maxMoves.pop(), maxMoves)
			horizontal = self.scaleConnecting(horizontal)
			h = h + horizontal

		maxMoves = copy.deepcopy(self.maxPlayerMoves)
		while len(maxMoves) > 0:
			vertical = self.scoreVertical(maxMoves.pop(), maxMoves)
			# divide by 2 to prevent AI from always going straight up
			vertical = self.scaleConnecting(vertical) / 2
			h = h + vertical

		maxMoves = copy.deepcopy(self.maxPlayerMoves)
		while len(maxMoves) > 0:
			dia = self.scoreLeftDiagonal(maxMoves.pop(), maxMoves)
			dia = self.scaleConnecting(dia) / 2
			h = h + dia

		maxMoves = copy.deepcopy(self.maxPlayerMoves)
		while len(maxMoves) > 0:
			dia = self.scoreRightDiagonal(maxMoves.pop(), maxMoves)
			dia = self.scaleConnecting(dia) / 2
			h = h + dia

		# try blocking min from winning
		for maxMove in self.maxPlayerMoves:
			minHorz = self.scoreHorizontal(maxMove, None, True)
			minVert = self.scoreVertical(maxMove, None, True)
			ldia = self.scoreLeftDiagonal(maxMove, None, True)
			rdia = self.scoreRightDiagonal(maxMove, None, True)

			# if move by max blocked 3 or more chips
			if minHorz > 2 or minVert > 2 or ldia > 2 or rdia > 2:
				h = h + 100

		return h

	# take the number of connecting chips and increase the score
	# very high value when 4 chips are connecting
	# otherwise just square the number of connecting chips
	def scaleConnecting(self, numConnecting):
		if numConnecting >= WINNING_SUM:
			return 200
		else:
			return numConnecting**2

	# return num of horizontal chips connected to chip
	# inverseChip tells method to count opposite connecting chips around given chip
	# remove connected chips from moveList if given
	# TODO: could be refactored to use scoreDiagonal
	def scoreHorizontal(self, chip, moveList=None, inverseChip=False):
		row = chip[0]
		col = chip[1]
		# print chip
		playerChipType = self.gameboard.getChipAt(row, col)
		if (inverseChip):
			playerChipType = playerChipType * -1
		# print "player chip type - %d" % playerChipType
		left = 0
		for i in range(1, gb.BOARD_WIDTH):
			leftChip = self.gameboard.getChipAt(row, col - i)
			# print 'left chip'
			# print leftChip
			if leftChip == playerChipType:
				if moveList is not None:
					moveList.remove( (row, col-i) )
				left = left + 1
			else:
				break
		right = 0
		for i in range(1, gb.BOARD_WIDTH):
			rightChip = self.gameboard.getChipAt(row, col + i)
			# print 'right chip'
			# print rightChip
			if rightChip == playerChipType:
				if moveList is not None:
					moveList.remove( (row, col+i) )
				right = right + 1
			else:
				break
		numConnected = left + right + 1
		if inverseChip:
			numConnected = numConnected - 1

		return numConnected

	# return num of chips that are connected vertically to the given chip location
	# inverseChip tells method to count opposite connecting chips around given chip
	# remove connecting chips from the list given
	# TODO: could be refactored to use scoreDiagonal
	def scoreVertical(self, chip, moveList=None, inverseChip=None):
		row = chip[0]
		col = chip[1]
		# print chip
		playerChipType = self.gameboard.getChipAt(row, col)
		if inverseChip:
			playerChipType = playerChipType * -1
		# print "player chip type - %d" % playerChipType
		up = 0
		for i in range(1, gb.BOARD_HEIGHT):
			upChip = self.gameboard.getChipAt(row-i, col)
			if upChip == playerChipType:
				if moveList is not None:
					moveList.remove( (row-i, col) )
				up = up + 1
			else:
				break
		down = 0
		for i in range(1, gb.BOARD_HEIGHT):
			downChip = self.gameboard.getChipAt(row+i, col)
			if downChip == playerChipType:
				if moveList is not None:
					moveList.remove( (row+i, col) )
				down = down + 1
			else:
				break
		numConnected = up + down + 1
		if inverseChip:
			numConnected = numConnected - 1

		return numConnected

	# calls score diagonal with direction list to sum chips in a right diagonal
	def scoreRightDiagonal(self, chip, moveList=None, inverseChip=None):
		diagonalUp = (-1, 1)
		diagonalDown = (1, -1)
		diagonalList = [diagonalUp, diagonalDown]
		return self.scoreDiagonal(diagonalList, chip, moveList, inverseChip)

	# calls score diagonal with direction list to sum chips in a left diagonal
	def scoreLeftDiagonal(self, chip, moveList=None, inverseChip=None):
		diagonalUp = (-1, -1)
		diagonalDown = (1, 1)
		diagonalList = [diagonalUp, diagonalDown]
		return self.scoreDiagonal(diagonalList, chip, moveList, inverseChip)

	# count the number of connecting diagonal chips from a chip location
	# inverseChip tells method to count opposite connecting chips around given chip
	# removes the chips counted from a given list of moves
	def scoreDiagonal(self, diagonalDirection, chip, moveList=None, inverseChip=None):
		diagonalUp = diagonalDirection[0]
		diagonalDown = diagonalDirection[1]
		row = chip[0]
		col = chip[1]
		playerChipType = self.gameboard.getChipAt(row, col)
		if inverseChip:
			playerChipType = playerChipType * -1

		up = 0
		i = playerChipType
		temp_row = row
		temp_col = col
		while i == playerChipType:
			temp_row = temp_row + diagonalUp[0]
			temp_col = temp_col + diagonalUp[1]
			i = self.gameboard.getChipAt(temp_row, temp_col)
			if i == playerChipType:
				up = up + 1
				if moveList is not None:
					moveList.remove( (temp_row, temp_col))

		down = 0
		i = playerChipType
		temp_row = row
		temp_col = col
		while i == playerChipType:
			temp_row = temp_row + diagonalDown[0]
			temp_col = temp_col + diagonalDown[1]
			i = self.gameboard.getChipAt(temp_row, temp_col)
			if i == playerChipType:
				down = down + 1
				if moveList is not None:
					moveList.remove( (temp_row, temp_col))

		if inverseChip:
			return up + down

		return up + down + 1

	# changes the type of player the node represents
	def setPlayerType(self, playerType):
		self.player = playerType

	# place the chip for this particular node/state
	# return the resulting child node
	def placeChipAt(self, index):
		return Node(self, index)

	# return a list of the available child nodes
	def generateChildren(self):
		children = [] 
		for i in self.gameboard.getAvailableMoves():
			children.append(Node(self, i))
		return children

	# determine how many moves or children available to generate
	def getNumOfChildren(self):
		return self.gameboard.availableMoves()

	# return a list of the available column indexs
	def getAvailableMoves(self):
		return self.gameboard.getAvailableMoves()

	# get the player represetation for the board
	def getPlayerSign(self):
		if self.player == PLAYER_MAX:
			return PLAYER_MAX
		else:
			return PLAYER_MIN # representation of player min
