import numpy as np
import random

import entity

import database as db


VERBOSE = True



# ------------------------------ Game --------------------------------------------

class Game:
	def __init__(self, width, length):
		self.init_board(width, length)
		self.pick_players()

	def init_board(self, width, length):
		self.board = Board(width, length)

	def pick_players(self):
		self.players = []
		self.players += [entity.Generic('Player 1')]
		self.players += [entity.RandomAI('Player 2')]

	# -------------------------------- Party ------------------------------------------

	def init_party(self):
		first, second = self.players
		party = Party(board, first, second)
		# party.start()


# ------------------------------- Board -------------------------------------------


class Board:
	def __init__(self, width, length):
		 self.reshape_board(width, length)

	def reshape_board(self, width, length): # TODO use
		self.width = width
		self.length = length

		self.set_board()

	def set_board(self):
		self.board = np.zeros((self.width, self.length))

	# ---------------------------- Core ----------------------------------------------

	def is_complete(self):
		pass

	# ---------------------------- display ----------------------------------------------

	def __str__(self):
		title = f"Board ({self.width}, {self.length})"
		grid = str(self.board)
		axe = '  ' + '  '.join([str(x) for x in range(1, self.length+1)])
		sep = '\n'

		return title + sep + grid + sep + axe




# ----------------------- Database ---------------------------

def access_db(db_name):
	return db.get_connection(db_name)


def populate_db(db_connection, list):
	# convert list elements to tuple
	rows = [(elm,) for elm in list]

	db.insert_rows(db_connection, rows)


def load_db(db_connection):
	rows = db.get_all_primes(db_connection)

	primes = []
	for row in rows:
		primes += [row['primes']]

	return primes


def test_write_and_read_db():
	db_name = 'database/connect_four.db'
	prime_db = access_db(db_name)
	
	# create
	primes = [i for i in range(5)]
	populate_db(prime_db, primes)
	prime_db.close()

	# access
	prime_db = access_db(db_name)
	rows = load_db(prime_db)
	prime_db.close()


# --------------------------------------------------------------------------


class Party:
	def __init__(self, board, first, second):
		 self.board = board

		 self.first = first
		 self.first.id = 1
		 self.second = second
		 self.second.id = 2
		 
		 self.turn = 0

	def start(self):
		while "Party is running":
			if next_play():
				break

			action = self.second.play()
			self.board.update(self.second.id, action)
			if self.board.is_complete():
				break

			self.turn += 1


	def next_play(self, player):
		action = self.first.play()
		self.board.update(self.first.id, action)
		return self.board.is_complete()
		



# ------------------------ Test --------------------------------------------------


verbose_print = print if VERBOSE else lambda *a, **k: None

def test_Model():
	width = 7
	model = Board(width, width)
	print(model)

	p1 = entity.Generic('Player 1')
	p2 = entity.RandomAI('Player 2')


	p1.play(model.board)
	p2.play(model.board)


if __name__ == '__main__':
	test_Model()

