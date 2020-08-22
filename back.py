import random

import board
import entity
import database as db
from conf.global_config import *


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
		while "players want's to play":
			game.init_party()
			break


	def pick_player(self): # TODO
		name = '?'
		while not name.isalnum():
			name = input('Enter your name (only alpahnumeric values): ')


# ------------------------------ Game --------------------------------------------

class Game:
	def __init__(self, grid, min_tile_connected, name1, type1, name2, type2):
		self.init_board(*grid.values(), min_tile_connected)
		self.pick_players(name1, type1, name2, type2)
		self.database = Database()

	def init_board(self, width, length, min_tile_connected):
		self.board = board.Board(width, length, min_tile_connected)

	def pick_players(self, name1, type1, name2, type2):
		self.players = []
		self.players += [self.create_entity(name1, type1)]
		self.players += [self.create_entity(name2, type2)]

	def create_entity(self, name, type):
		args = [f'{name} ({type})']
		type = type.lower()
		f = None
		if type == 'human':
			f = entity.Human
		elif type == 'neuralnetwork':
			f = entity.NeuralNetwork
			args += [self.board.goal]
		elif type == 'randomai':
			f = entity.RandomAI

		return f(*args)

	# -------------------------------- Party ------------------------------------------

	def init_party(self):
		first, second = self.players
		# TODO : who want's to start ?
		# random.shuffle()

		party = Party(self.board, first, second)
		party.start()

		self.database.save(party.data())
		self.database.load_db()


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
		print()
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

	def data(self):
		return (
			db.array_to_string([self.board.width, self.board.length]),
			self.first.name,
			self.second.name,
			self.turn,
			db.array_to_string(self.board.history)
		)


# ----------------------------- Database -----------------------------------------

class Database:
	def __init__(self):
		self.db_name = 'database/connect_four.db'
		
	def access_db(self):
		return db.get_connection(self.db_name)

	def save(self, data):
		conn = self.access_db()
		id = db.insert_row(conn, data)
		conn.close()
		print(f'Game #{id} saved.')

	def load_db(self):
		conn = self.access_db()
		rows = db.select_all(conn)

		# db.print_table(rows)

		actions = []
		for row in rows:
			actions += [row['actions']]

		conn.close()
		return actions


# ------------------------ Test --------------------------------------------------

def test_Model():
	width = 7
	model = board.Board(width, width)
	print(model)


	p1 = entity.Generic('Player 1')
	p2 = entity.RandomAI('Player 2')


	p1.play(model.board)
	p2.play(model.board)


if __name__ == '__main__':
	test_Model()

