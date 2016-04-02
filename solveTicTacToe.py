import random

class GameState():

	def __init__(self):
		self.board = {}
		self.board['A'] = [['0','1','2'],
						['3','4','5'],
						['6','7','8']]
		self.board['B'] = [['0','1','2'],
						['3','4','5'],
						['6','7','8']]
		self.board['C'] = [['0','1','2'],
						['3','4','5'],
						['6','7','8']]
		self.board['T'] = [['0','X','X'],
						['3','X','5'],
						['X','7','8']]

		self.playerIndex = 'AI'

		boardNum = random.choice(['A','B','C'])
		pos = random.randint(0,8)
		self.latestPosition = (boardNum, pos)
		self.placeTo(boardNum, pos)

	def display(self):
		#print self.playerIndex + ': ' + self.latestPosition[0] + str(self.latestPosition[1])
		if not self.isDead('A'):
			print 'A:    ',
		if not self.isDead('B'):
			print 'B:    ',
		if not self.isDead('C'):
			print 'C:    ',
		print

		for i in range(3):

			if not self.isDead('A'):
				for j in range(3):
					print self.board['A'][i][j],
				print '',

			if not self.isDead('B'):
				for j in range(3):
					print self.board['B'][i][j],
				print '',

			if not self.isDead('C'):
				for j in range(3):
					print self.board['C'][i][j],
				print '',
			print '\n',
		pass

	def placeTo(self, boardNum='A', pos=0):
		self.board[boardNum][pos/3][pos%3] = 'X'
		self.latestPosition = boardNum + str(pos)

	def isOkToPlace(self, boardNum='A', pos=0):
		if self.isDead(boardNum):
			return False
		if self.board[boardNum][pos/3][pos%3] == 'X':
			return False
		return True

	def aiPlace(self):
		while True:
			boardNum = random.choice(['A','B','C'])
			pos = random.randint(0,8)
			if self.isOkToPlace(boardNum, pos):
				break
		self.placeTo(boardNum, pos)
		

	def isLose(self):
		if self.isDead('A') and self.isDead('B') and self.isDead('C'):
			return True
		else:
			return False

	def isDead(self, boardNum='A'):
		if self.board[boardNum][0][0] == 'X' and self.board[boardNum][0][1] == 'X' and self.board[boardNum][0][2] == 'X':
			return True
		if self.board[boardNum][1][0] == 'X' and self.board[boardNum][1][1] == 'X' and self.board[boardNum][1][2] == 'X':
			return True
		if self.board[boardNum][2][0] == 'X' and self.board[boardNum][2][1] == 'X' and self.board[boardNum][2][2] == 'X':
			return True
		if self.board[boardNum][0][0] == 'X' and self.board[boardNum][1][0] == 'X' and self.board[boardNum][2][0] == 'X':
			return True
		if self.board[boardNum][0][1] == 'X' and self.board[boardNum][1][1] == 'X' and self.board[boardNum][2][1] == 'X':
			return True
		if self.board[boardNum][0][2] == 'X' and self.board[boardNum][1][2] == 'X' and self.board[boardNum][2][2] == 'X':
			return True
		if self.board[boardNum][0][0] == 'X' and self.board[boardNum][1][1] == 'X' and self.board[boardNum][2][2] == 'X':
			return True
		if self.board[boardNum][0][2] == 'X' and self.board[boardNum][1][1] == 'X' and self.board[boardNum][2][0] == 'X':
			return True
		return False


if __name__ == '__main__':
	game = GameState()
	while not game.isLose():

		#last move is AI move
		if game.playerIndex == 'AI':
			print game.playerIndex + ': ' + game.latestPosition[0] + str(game.latestPosition[1])
			game.display()
			humanInput = raw_input('Your move: ')
			try:
				if game.isOkToPlace(humanInput[0],int(humanInput[1])) and len(humanInput) == 2:
					game.playerIndex = 'HM'
					game.placeTo(humanInput[0],int(humanInput[1]))
				else:
					print 'WRONG INPUT!!'
					continue
			except:
				print 'ERROR INPUT!!'
				continue

		
		#last move is HM move
		#if game.playerIndex == 'HM':
		else: 
			game.display()
			game.playerIndex = 'AI'
			game.aiPlace()
	print game.playerIndex + ' is LOSSER!!'





















