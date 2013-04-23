#
#	Overall Connect-4 game playing module
# 	Author: Tom Renn
#
import gameboard as gb
import nodeModule as nm
import re
import sys
import cProfile

# MiniMax algorithm
#
# node: Root node to calculate minimax on
# depth: How far down into the node to search
# returnNode: Optional parameter, True if this call is to return the resulting child node to pick
#		otherwise miniMax returns the heuristic value of the node it is given
def miniMax(node, depth, returnNode=False):
	isLeaf = False
	children = node.generateChildren()
	availableMoves = node.getAvailableMoves()
	result = 0;
	resultNode = node

	if len(availableMoves) == 0: 	# we're at a leaf
		result = node.heuristic2()
	elif  depth < 1: 				# reached max depth
		result = node.heuristic2()
	else:
		# look at each child for the moves available
		for nextMove in availableMoves:
			child = nm.Node(node, nextMove)
			# value of child node
			result = miniMax(child, depth-1)

			if node.player == nm.PLAYER_MAX:	# player is MAX
				if result >= node.alpha: 
					node.alpha = result
					resultNode = child
			else: 								# player is MIN	
				if result <= node.beta:
					node.beta = result
					resultNode = child
			
			# determine if we need to stop searching children	
			if node.alpha >= node.beta:
				break
				
	if (returnNode):
		# clear alpha-beta values from this traversal
		resultNode.resetAlphaBeta()
		return resultNode
	else:
		return result

# Overall method that plays connect4
def playGame():
	state = nm.Node()
	print 'Welcome to connect4. You are P, the player. C is the computer opponent'
	print "Type 'quit' or 'q' to exit the game at any time"

	if askPlayerPreference():	# player moves first if desired
		move = getPlayerMove(state)
		state = state.placeChipAt(move)
	else:						# always have computer act as MAX player
		state.setPlayerType(nm.PLAYER_MAX)

	winningPlayer = 'initalization'
	# Game continues until someone wins
	while True: 
		depth = 4
		state = miniMax(state, depth, True)
		state.gameboard.fancyPrint()

		if state.isGameOver():
			winningPlayer = 'Computer wins!'
			break

		move = getPlayerMove(state)
		if move == -1:
			winningPlayer = 'You quit, loser!'
			break

		state = state.placeChipAt(move)

		if state.isGameOver():
			# print winning gameboard
			state.gameboard.fancyPrint() 
			winningPlayer = 'You win!'
			break

	print winningPlayer

# get the players next move for a particular node
# continues until player enters an available move
# or until player types quit, which case returns -1
def getPlayerMove(node):
	availableMoves = node.getAvailableMoves()
	move = -1
	while move == -1 or move not in availableMoves:
		move = raw_input("Choose your next move (0-6): ")
		if re.match('\d', move): # move is a digit
			move = int(move)
		elif re.match('quit|q', move):
			move = -1
			break
	return move

# ask the player if they would like to move first
# returns True if player moves first
def askPlayerPreference():
	yes = ["yes", "y", "Y"]
	no = ["no", "n", "N"]
	userInput = raw_input("Would you like to move first? (y/n): ")
	if userInput in yes:
		return True
	elif userInput in no:
		return False
	else:
		print "Sorry that is not an acceptable answer"
		return askPlayerPreference()


playGame()


