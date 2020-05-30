import sqlite3
from sqlite3 import Error
import os

class Database(object):
	def __init__(self, bot):
		self.bot = bot
		self.database = self.bot.database
		self.conn = None
		self.c = None

	def create_database(self, name):
		if not os.path.exists(f'{self.database}/{name}.db'):
			f = open(f'{self.database}/{name}.db', 'w')
			f.close()

	def create_databases(self):
		for guild in self.bot.guilds:
			self.create_database(guild.name)
	
	def exists_database(self, name):
		return os.path.exists(f'{self.database}/{name}.db')

	def create_default_database(self, name):
		self.conn = sqlite3.connect(f'{self.database}/{name}.db')
		self.c = self.conn.cursor()
		self.c.execute('''CREATE TABLE Members (
							id INTEGER PRIMARY KEY,
							nick text,
							server text,
							time int,
							warnings int,
							partner text
						)''')
		self.conn.commit()
		self.conn.close()
	
	def set_default_database_value(self, name, data):
		self.conn = sqlite3.connect(f'{self.database}/{name}.db')
		self.c = self.conn.cursor()
		#print(data[0])
		self.c.execute('''INSERT INTO Members VALUES ({}, '{}', '{}', {}, {}, '{}')'''.format(data[0], data[1], data[2], data[3], data[4], data[5]))
		self.conn.commit()
		self.conn.close()
	
	def delete_database_id(self, name, id):
		self.conn = sqlite3.connect(f'{self.database}/{name}.db')
		self.c = self.conn.cursor()
		self.c.execute('''DELETE FROM Members WHERE id = {}'''.format(id))
		self.conn.commit()
		self.conn.close()

	def set_new_database_value(self, name, id, data):
		self.conn = sqlite3.connect(f'{self.database}/{name}.db')
		#print(name, id, data)
		self.c = self.conn.cursor()
		self.c.execute('''UPDATE Members
						  SET
							nick = '{}',
							server = '{}',
							time = {},
							warnings = {},
							partner = '{}'
						  WHERE id = {}
						  '''.format(data[0], data[1], data[2], data[3], data[4], id))
		self.conn.commit()
		self.conn.close()

	def get_database_value(self, name, id):
		self.conn = sqlite3.connect(f'{self.database}/{name}.db')
		self.c = self.conn.cursor()
		self.c.execute('SELECT * FROM Members WHERE id = {}'.format(id))
		data = self.c.fetchall()[0]
		self.conn.commit()
		self.conn.close()
		return data

	def get_database_values(self, name):
		self.conn = sqlite3.connect(f'{self.database}/{name}.db')
		self.c = self.conn.cursor()
		self.c.execute('SELECT * FROM Members')
		data = self.c.fetchall()
		self.conn.commit()
		self.conn.close()
		return data

	def is_default(self, name, id):
		data = self.get_database_value(name, id)
		if data[3:] == (0, 0, ''):
			return True
		return False
