import random

VERBOSE = True

class Generic:
	def __init__(self, name):
		self.name = name
		self.id = 0

	def play(self, board):
		print(f"{self.name}: Don't know how to play...")

	def play_is_valid(self, board, pos):
		pass # todo if column is full


class Human(Generic):
	def __init__(self, name):
		super().__init__(name)

	def play(self, board):
		print(f"{self.name}: Do what you want !")


class Replay(Generic):
	def __init__(self, name, actions):
		super().__init__(name)
		self.actions = actions[::-1]

	def play(self, board):
		action = self.actions.pop()
		print(f"{self.name}: Replay action : {action}!")
		return action


class RandomAI(Generic):
	def __init__(self, name):
		super().__init__(name)

	def play(self, board):
		return random.randint(0, len(board[0])-1)
		

# --------------------------------------------------------------------------


verbose_print = print if VERBOSE else lambda *a, **k: None

def test_Entity():
	e = Generic('Generic Entity')
	rd = RandomAI('Random Entity')
	
	board = [[]*7]
	e.play(board)
	rd.play(board)

	rp = Replay('Replay Entity', [1, 5, 2, 4, 3])
	for i in range(2):
		rp.play(board)


if __name__ == '__main__':
	test_Entity()

