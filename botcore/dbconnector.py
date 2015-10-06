import MySQLdb
import datetime
from config import databaseAddress, databaseUser, databaseUserPass, databaseName

class dbconnector:

	#Just makes the database connection
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
	TODO: Write method to query data for general log
	"""

	"""
	TODO: Write method to query for specific msgType
	"""

	"""
	R: 
	M: 
	E: 
	Functions properly, consider other methods for logging
	"""
	def logHistory(self, userName, length):
		self.cursor = self.db.cursor()
		uid = self._getIDFromUsername(userName)
		try:
			self.cursor.execute("SELECT COUNT( * ) FROM `log` WHERE `user_id` = %s" % str(uid) )
			maxVal = self.cursor.fetchone()[0]
			minVal = maxVal - length
			if minVal < 0:
				minVal = 0
			self.cursor.execute("SELECT * FROM `log` WHERE `user_id` = %s LIMIT %s, %s" % (uid, minVal, maxVal))
			output = self.cursor.fetchall()
			print output
			"""
			TODO: Eventually it won't return the output but rather log it
			Possible make another class somewhere and make it create an object of that class
			to that has logging methods for things like this so it doesn't keep passing input around
			"""
			return output
		except:
			self.db.rollback()
		self.cursor.close()


	"""
	TODO: Write method to retrieve username from id
	"""
	def _getUsernameFromID(self, userID):
		self.cursor = self.db.cursor()

		self.cursor.close()

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
			print("error getting id from username")
		self.cursor.close()
