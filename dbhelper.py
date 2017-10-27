import sqlite3 

class DBHelper:
	# Creat DB connection 
	def __init__(self, dbname="todo.sqlite"):
		self.dbname = dbname
		self.conn = sqlite3.connect(dbname)

	# Create table in DB called items with description column 
	def setup(self):
	    tblstmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text)"
	    itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)" 
	    ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
	    self.conn.execute(tblstmt)
	    self.conn.execute(itemidx)
	    self.conn.execute(ownidx)
	    self.conn.commit()

	# Insert item text into DB 
	def add_item(self, item_text, owner):
		stmt = "INSERT INTO items (description, owner) VALUES (?, ?)"
		args = (item_text, owner)
		self.conn.execute(stmt, args)
		self.conn.commit()

	# Delete item text from DB 
	def delete_item(self, item_text, owner):
		stmt = "DELETE FROM items WHERE description = (?) AND owner = (?)"
		args = (item_text, owner)
		self.conn.execute(stmt, args)
		self.conn.commit()

	# Return a list of all items in DB 
	# SQLite always returns data in tuple
	def get_items(self, owner):
		stmt = "SELECT description FROM items WHERE owner = (?)"
		args = (owner, )
		return [x[0] for x in self.conn.execute(stmt, args)]