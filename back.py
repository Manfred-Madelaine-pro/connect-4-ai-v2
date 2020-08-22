import random

import board
import entity
import database as db
from conf.global_config import *


VERBOSE = True
SKIP_INPUT = True
DEFAULT_CONFIG = "conf/config.yml"


# ------------------------------ Menu --------------------------------------------

class Menu:
	def __init__(self):
		self.options = ['settings', 'start', 'exit']

		self.menu()

	def menu(self):
		self.intro()
		choice = self.choose_option()
		self.next_step(choice)

	def intro(self):
		menu = 'choose an option :'
		lines = [menu] + [f'{i}) {o}' for i,o in enumerate(self.options)]

		print('\n'.join([l.capitalize() for l in lines]))

	def choose_option(self):
		choice = '1' if SKIP_INPUT else '?'
		while not choice.isnumeric():
			choice = input("Enter the the option's id > ")
			if choice.isnumeric() and 0 <= int(choice) <= len(self.options)-1:
				break
			print('Incorrect input, please retry with a correct id.')
			choice = '?'
		return int(choice)

	def next_step(self, choice):
		option = self.options[choice]
		if option == 'start':
			default_settings = self.get_settings(DEFAULT_CONFIG)
			self.start(default_settings)
		if option == 'exit':
			print('See you next time !')
			return 0
		if option == 'settings':
			print('This part is still on constuction !\n')
			self.menu()

	def get_settings(self, config_file):
		global_conf = global_config(config_file)
		return global_conf['game'].values()

	def start(self, settings):
		game = Game(*settings)
		game.init_party()


	def pick_player(self): # TODO
		name = '?'
		while not name.isalnum():
			name = input('Enter your name (only alpahnumeric values): ')


# ------------------------------ Game --------------------------------------------

class Game:
	def __init__(self, width, length, name1, name2):
		self.init_board(width, length)
		self.pick_players(name1, name2)

	def init_board(self, width, length):
		self.board = board.Board(width, length)

	def pick_players(self, name1, name2):
		self.players = []
		self.players += [entity.RandomAI(name1)]
		self.players += [entity.RandomAI(name2)]

	# -------------------------------- Party ------------------------------------------

	def init_party(self):
		first, second = self.players
		# TODO : who want's to start ?
		# random.shuffle()
		party = Party(self.board, first, second)
		party.start()
		# TODO save party in db


# ------------------------------- Party -------------------------------------------

class Party:
	def __init__(self, board, first, second):
		self.board = board

		self.first = first
		self.first.id = 1
		self.second = second
		self.second.id = 2

		self.turn = 1

	def start(self):
		self.board.set_board()
		print(self.board)
		while "Party is running":
			print(f'Turn #{self.turn}')
			if self.next_play(self.first) or self.next_play(self.second):
				break

			self.turn += 1

		print('End of game :')
		if self.board.grid_is_full():
			print("It's a draw !")
		else :
			winner = self.first if self.board.get_last_player() == 1 else self.second
			row, col, sens = self.board.winning_info()
			print(f'{winner.name} won {sens} with the tile t{(row+1,col+1)} after {self.turn} turns !')


	def next_play(self, player):
		while 'pick a column':
			column = player.play(self.board.grid)
			if not self.board.column_is_full(column):
				break
		
		print(f'{player.name} plays at {column}')

		self.board.update(player.id, column)
		print(self.board)

		return self.board.is_complete()


# ----------------------- Database ---------------------------

class Database:
	def access_db(db_name):
		return db.get_connection(db_name)


	def populate_db(db_connection, list):
		# convert list elements to tuple
		rows = [(elm,) for elm in list]

		db.insert_rows(db_connection, rows)


	def load_db(db_connection):
		rows = db.select_all(db_connection)

		actions = []
		for row in rows:
			actions += [row['actions']]

		return actions


# ------------------------ Test --------------------------------------------------


verbose_print = print if VERBOSE else lambda *a, **k: None

def test_Model():
	width = 7
	model = board.Board(width, width)
	print(model)


	p1 = entity.Generic('Player 1')
	p2 = entity.RandomAI('Player 2')


	p1.play(model.board)
	p2.play(model.board)


def test_write_and_read_db():
	db_name = 'database/connect_four.db'
	database = access_db(db_name)
	
	# create

	rows = [
		['7, 7', 'Random AI', 'Random AI 2', '3', '1, 2, 3, 4, 5'],
		['4, 4', 'Random AI', 'Random AI 2', '2', '1, 2, 3'],
	]
	populate_db(database, rows)
	database.close()

	# access
	database = access_db(db_name)
	rows = load_db(database)
	database.close()


if __name__ == '__main__':
	test_Model()

