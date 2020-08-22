import sqlite3

from prettytable import from_db_cursor


SEPARATOR = ', '


def get_connection(db_name):
	con = sqlite3.connect(db_name)
	con.row_factory = sqlite3.Row
	return con


def create_table(con):
	sql_create_table = """
		CREATE TABLE IF NOT EXISTS games (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		dimensions TEXT,
		player1 TEXT,
		player2 TEXT,
		turn INTEGER,
		actions TEXT,
		creation_date text NOT NULL
		);
	"""
	with con:
		con.execute(sql_create_table)


def insert_row(con, row):
	sql_insert_row = """
		INSERT INTO games (dimensions,player1,player2,turn,actions,creation_date)
		VALUES (
		  ?,
		  ?,
		  ?,
		  ?,
		  ?,
		  DATETIME('now')
		);
	"""
	with con:
		try:
			con.execute(sql_insert_row, row)

			max_id = con.execute('SELECT max(id) FROM games').fetchone()[0]
			return max_id
		except sqlite3.IntegrityError:
			return 'Line already exists.' 


def array_to_string(arr):
	return SEPARATOR.join(str(e) for e in arr)


def string_to_array(string):
	return s.split(SEPARATOR)


def select_all(con):
	select_all = """
		SELECT * FROM games;
	"""
	return con.execute(select_all)
	

def print_table(rows):
	table = from_db_cursor(rows)
	print(table) 



# ----------------------- Test ---------------------------

def test_db_creation():
	con = get_connection(':memory:')
	create_table(con)

	rows = [
		( '7, 7', 'Random AI', 'Random AI 2', '3', '1, 2, 3, 4, 5'),
		( '4, 4', 'Random AI', 'Random AI 2', '2', '1, 2, 3'),
	]
	insert_row(con, rows)
	rows = select_all(con)
	print_table(rows)

	con.close()


if __name__ == '__main__':
	test_db_creation()