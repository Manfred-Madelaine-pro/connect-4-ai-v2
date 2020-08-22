import numpy as np


class Board:
	def __init__(self, width, length, min_tile_connected):
		self.width = width
		self.length = length
		self.goal = min_tile_connected # TODO give bonuses when more tiles than required are connected 


	def set_board(self):
		self.grid = np.zeros((self.width, self.length))
		self.history = []

	# ---------------------------- display ----------------------------------------------

	def __str__(self):
		grid = str(self.grid)
		axe = '  ' + '  '.join([str(x) for x in range(1, self.length+1)])
		sep = '\n'

		return grid + sep + axe

	# ---------------------------- Verifications ----------------------------------------------

	def is_complete(self):
		return self.grid_is_full() or self.tiles_are_connected()

	# ---------------------------- Full 

	def grid_is_full(self):
		return len(self.history) >= self.width * self.length

	def column_is_full(self, col):
		for row in self.grid:
			if row[col] == 0:
				return False
		return True

	# ---------------------------- Check 

	def tiles_are_connected(self):
		return sum(self.all_checks()) >= 1

	def all_checks(self):
		val = self.get_last_player()
		row, col = self.get_last_tile()

		horz = self.check_horz(val, row, col)
		vert = self.check_vert(val, row, col)
		diag = self.check_diag(val, row, col)

		return horz, vert, diag

	def check_horz(self, val, row, col):
		c = 0
		born_inf = min(0, abs(col - self.goal))
		born_sup = min(self.length, col + self.goal)
		tiles = self.grid[row][born_inf : born_sup]

		return self.count_adjacent_tiles(val, tiles) >= self.goal

	def check_vert(self, val, row, col):
		born_inf = min(0, abs(row - self.goal))
		born_sup = min(self.width, row + self.goal)
		tiles = [t[col] for t in self.grid[born_inf : born_sup]]

		return self.count_adjacent_tiles(val, tiles) >= self.goal

	def check_diag(self, val, row, col):
		# bug when width != length		
		diag_left  = [self.grid[i+row][i+col] for i in range(self.width) if i+row < self.width and i+col < self.length]
		diag_right  = [self.grid[row-i][col-i] for i in range(self.width) if row-i >= 0 and col-i >= 0]

		# print(diag_left, diag_right)
		cl = self.count_adjacent_tiles(val, diag_left)
		cr = self.count_adjacent_tiles(val, diag_right)
		# return cl >= self.goal or cr >= self.goal
		return False

	def count_adjacent_tiles(self, val, tiles):
		c = 0
		for t in tiles:
			if t == val:
				c += 1
			else:
				c = 0
		return c

	# ---------------------------- Utils 

	def winning_info(self):
		# TODO several sens & how many tiles are connected ?
		row, col = self.get_last_tile()
		sens = [d for c,d in zip(self.all_checks(), ['horizontaly', 'verticaly', 'diagonaly']) if c]
		return row, col, ', '.join(sens)

	def get_last_tile(self):
		col = self.history[-1]
		for i in range(len(self.grid)):
			if self.grid[i][col] != 0:
				return (i, col)

	def get_last_player(self):
		return 2 if len(self.history) % 2 == 0 else 1

	def update(self, player_id, col):
		for row in self.grid[::-1]:
			if row[col] == 0:
				row[col] = player_id
				break
		self.history += [col]
		

# ----------------------------- Test ---------------------------------------------

def test_check():
	b = Board(7, 7)
	b.grid = [
		[0, 1, 1, 1, 1, 2, 2,],
		[2, 2, 2, 2, 2, 1, 1,],
		[2, 2, 2, 2, 2, 1, 1,],
		[2, 2, 2, 1, 1, 1, 2,],
		[1, 1, 1, 1, 1, 1, 2,],
		[1, 2, 2, 2, 2, 1, 2,],
		[1, 2, 2, 1, 1, 2, 1,]
	]

	res = b.check_horz(2, 2, 0)
	print(res)
	res = b.check_vert(1, 1, 5)
	print(res)
	res = b.check_diag(1, 1, 1)
	# res = b.check_diag(1, 1, 7)
	print(res)

	b.grid = [
		[0, 0, 0, 0, 0, 0, 0,],
		[0, 0, 0, 0, 0, 0, 0,],
		[0, 0, 0, 0, 0, 0, 1,],
		[0, 0, 0, 2, 0, 0, 2,],
		[0, 0, 0, 2, 0, 0, 1,],
		[1, 0, 0, 2, 1, 2, 2,],
		[1, 1, 1, 2, 1, 2, 1,]
	]

	res = b.check_vert(2, 2, 6)
	print(res)


if __name__ == '__main__':
	test_check()

