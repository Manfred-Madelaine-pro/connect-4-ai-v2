import numpy as np


MIN_TILE_CONNECTED = 4 # TODO give bonuses when more tiles than required are connected 


class Board:
	def __init__(self, width, length):
		self.width = width
		self.length = length

	def set_board(self):
		self.grid = np.zeros((self.width, self.length))
		self.history = []

	# ---------------------------- Core ----------------------------------------------

	def is_complete(self):
		return self.grid_is_full()

	def grid_is_full(self):
		return len(self.history) >= self.width * self.length

	def column_is_full(self, col):
		for row in self.grid:
			if row[col] == 0:
				return False
		return True

	def tiles_are_connected(self):
		pass

	def update(self, player_id, col):
		for row in self.grid[::-1]:
			if row[col] == 0:
				row[col] = player_id
				break
		self.history += [col]

	# ---------------------------- display ----------------------------------------------

	def __str__(self):
		grid = str(self.grid)
		axe = '  ' + '  '.join([str(x) for x in range(1, self.length+1)])
		sep = '\n'

		return grid + sep + axe
		