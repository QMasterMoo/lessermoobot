import MySQLdb
import datetime
from config import databaseAddress, databaseUser, databaseUserPass, databaseName

class dbconnector:

	#RME: Just makes the database connection
	def __init__(self):
		try:
			self.db = MySQLdb.connect(databaseAddress,
			 							databaseUser, 
										databaseUserPass, 
										databaseName)
		except:
			print "Error connecting to database, recheck your inputs"

	"""
	R: username, date, message type, and message data
	M: nothing
	E: inserts everything into the log
	"""
	def insertMessageIntoLog(self, userName, date, msgType, data):
		self.cursor = self.db.cursor()
		self._insertUserIntoID(userName)
		uid = self._getIDFromUsername(userName)
		try:
			self.cursor.execute("INSERT INTO log VALUES (NULL, %s, \'%s\', \'%s\', \'%s\')"
				% (str(uid), date, msgType, data))
			self.db.commit()
		except:
			self.db.rollback()
			print('failed')
		self.cursor.close()

	"""
	TODO: Write method to query data for userName
	"""

	"""
	TODO: Write method to query for specific msgType
	"""

	"""
	TODO: Write method to generate generate log for the last x messages
	"""

	"""
	TODO: 
	"""


	"""
	R: takes in userName
	M: n/a
	E: inserts the username into the 'users' table
	"""
	def _insertUserIntoID(self, userName):
		self.cursor = self.db.cursor()
		try:
			self.cursor.execute("INSERT INTO users VALUES ( NULL , \'%s\')" % userName)
			self.db.commit()
		except:
			self.db.rollback()
		self.cursor.close()

	"""
	R: takes in username
	M: n/a
	E: takes in the username and returns the user's id
	"""
	def _getIDFromUsername(self, userName):
		self.cursor = self.db.cursor()
		try:
			self.cursor.execute("SELECT * FROM users WHERE username=\'%s\'" % userName)
			result = self.cursor.fetchone()
			return result[0]
		except:
			print("Error retreiving data")
		self.cursor.close()