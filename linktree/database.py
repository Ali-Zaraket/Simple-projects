import sqlite3 as sq 


# database and table creation 
def create_table():
	connection = sq.connect('linktree.db')
	c = connection.cursor()

	c.execute('''CREATE TABLE linktree(

		title varchar,
		url path);

	''')
	connection.commit()
	connection.close()


class Database(object):

	''' Database controlling class where all database functions land '''

	def __init__(self):

		self.database_name = 'linktree.db'
		self.connection = sq.connect(self.database_name)
		self.cursor = self.connection.cursor()

	def save(self, lst):  # SAVING THE ADDED LINK TO THE DATABASE
		sql = 'INSERT INTO linktree VALUES (?,?);'
		self.cursor.executemany(sql, (lst, ))
		self.connection.commit()

	def delete(self, title):   # DELETING SPECIFIC VALUE FROM THE DATABASE ACCORDING TO A VALUE THE USER SUBMITS
		sql = 'DELETE FROM linktree WHERE title = (?);'
		# print(title)
		# print(type(title))
		self.cursor.executemany(sql, ([title, ], ))
		self.connection.commit()

	def update(self, update_key, new_value, title_name): # UPDATING A VALUE USING THE USER COMMITS
		if update_key == 'title':
			sql = 'UPDATE linktree SET title = (?) WHERE title = (?);'
		elif update_key == 'url':
			sql = 'UPDATE linktree SET url = (?) WHERE title = (?);'

		self.cursor.executemany(sql, ([new_value, title_name], ))
		self.connection.commit()

	def get(self):  # RETURNING ALL THE DATA IN THE DATABASE
		sql = 'SELECT * FROM linktree;'
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def close(self):   # CLOSING THE CONNECTION
		self.connection.close()
