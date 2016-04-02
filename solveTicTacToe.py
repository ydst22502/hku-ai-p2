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

		self.playerIndex = 'AI'

		boardNum = random.choice(['A','B','C'])
		pos = random.randint(0,8)
		self.latestPosition = (boardNum, pos)
		self.placeTo(boardNum, pos)

	def display(self):
		print self.playerIndex + ': ' + self.latestPosition[0] + str(self.latestPosition[1])
		print 'A:     B:     C:'
		for i in range(3):
			for j in range(3):
				print self.board['A'][i][j],
			print '',
			for j in range(3):
				print self.board['B'][i][j],
			print '',
			for j in range(3):
				print self.board['C'][i][j],
			print '',
			print '\n',

	def placeTo(self, boardNum='A', pos=0):
		self.board[boardNum][pos/3][pos%3] = 'X'


if __name__ == '__main__':
	newGameState = GameState()
	newGameState.display()