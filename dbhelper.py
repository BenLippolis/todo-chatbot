import sqlite3 

class DBHelper:
	# Creat DB connection 
	def __init__(self, dbname="todo.sqlite"):
		self.dbname = dbname
		self.conn = sqlite3.connect(dbname)

	# Create table in DB called items with description column 
	def setup(self):
		stmt = "CREATE TABLE IF NOT EXISTS items (description text)"
		self.conn.execute(stmt)
		self.conn.commit()

	# Insert item text into DB 
	def add_item(self, item_text):
		stmt = "INSERT INTO items (description) VALUES (?)"
		args = (item_text, )
		self.conn.execute(stmt, args)
		self.conn.commit()

	# Delete item text from DB 
	def delete_item(self, item_text):
		stmt = "DELETE FROM items WHERE description = (?)"
		args = (item_text, )
		self.conn.execute(stmt, args)
		self.conn.commit()

	# Return a list of all items in DB 
	# SQLite always returns data in tuple
	def get_items(self):
		stmt = "SELECT description FROM items"
		return [x[0] for x in self.conn.execute(stmt)]