import random


class Brain:
	def __init__(self, goal):
		self.goal = goal

	def think(self, board):
		return self.choose(board)

	def choose(self, board):
		return random.randint(0, len(board[0])-1)



def test_brain():
	b = Brain(4)

	grid = [
		[0, 0, 0, 0, 0, 0, 0,],
		[0, 0, 0, 0, 0, 0, 0,],
		[0, 1, 0, 0, 0, 0, 0,],
		[0, 1, 0, 0, 0, 0, 2,],
		[0, 1, 0, 2, 2, 0, 2,],
		[2, 2, 1, 2, 1, 1, 2,],
		[2, 1, 1, 1, 2, 1, 1,]
	 ] 
	res = b.think(grid)
	print(res)


if __name__ == '__main__':
	test_brain()


