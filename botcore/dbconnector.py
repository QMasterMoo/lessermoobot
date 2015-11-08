import MySQLdb
import datetime
from config import databaseAddress, databaseUser, databaseUserPass, databaseName
import sys
import random

class dbconnector:

	#Just makes the database connection
	def __init__(self):
		try:
			self.db = MySQLdb.connect(databaseAddress,
			 							databaseUser, 
										databaseUserPass, 
										databaseName)
		except:
			self._logError("CRITICAL ERROR: CONNECTING TO DATABASE")
			sys.exit(0)

	"""
	It inserts everything into the log
	"""
	def insertMessageIntoLog(self, userName, date, msgType, data):
		self.cursor = self.db.cursor()
		self._insertUserIntoID(userName)
		uid = self.getIDFromUsername(userName)
		try:
			self.cursor.execute("INSERT INTO log VALUES (NULL, %s, \'%s\', \'%s\', \'%s\')"
				% (str(uid), date, msgType, data))
			self.db.commit()
		except:
			self.db.rollback()
			#Currently an error with a certain message type
			#self._logError("CRITICAL ERROR: INSERTING MESSAGE INTO LOG")
		self.cursor.close()

	"""
	queries data for general log
	"""
	def queryLog(self, length):
		self.cursor = self.db.cursor()
		try:
			self.cursor.execute("SELECT COUNT( * ) FROM log")
			maxVal = self.cursor.fetchone()[0]
			minVal = maxVal - length
			if minVal < 0:
				minVal = 0
			self.cursor.execute("SELECT * FROM  log LIMIT %s , %s" % (minVal, maxVal))
			output = self.cursor.fetchall()
			self.cursor.close()
			return output
		except:
			self._logError("ERROR: querying in general")
		self.cursor.close()

	"""
	Queries for a specific mode or type
	It's untested, but should work
	"""
	def queryType(self, mode, length):
		self.cursor = self.db.cursor()
		try: 
			self.cursor.execute("SELECT COUNT( * ) FROM log WHERE type = \'%s\'" % (mode))
			maxVal = self.cursor.fetchone()[0]
			minVal = maxVal - length
			if minVal < 0:
				minVal = 0
			self.cursor.execute("SELECT * FROM  log WHERE type = \'%s\' LIMIT %s , %s" % (mode, minVal, maxVal))
			output = self.cursor.fetchall()
			print output
			self.cursor.close()
			return output
		except:
		    self._logError("ERROR: quering type")
		self.cursor.close()

	"""
	queries data for general log
	"""
	def queryHistory(self, userName, length):
		self.cursor = self.db.cursor()
		uid = self.getIDFromUsername(userName)
		try:
			self.cursor.execute("SELECT COUNT( * ) FROM log WHERE user_id = %s" % str(uid) )
			maxVal = self.cursor.fetchone()[0]
			minVal = maxVal - length
			if minVal < 0:
				minVal = 0
			self.cursor.execute("SELECT * FROM log WHERE user_id = %s LIMIT %s, %s" % (uid, minVal, maxVal))
			output = self.cursor.fetchall()
			self.cursor.close()
			return output
		except:
			self._logError("ERROR: querying history")
		self.cursor.close()

	"""
	retrieves username from id
	"""
	def getUsernameFromID(self, userID):
		self.cursor = self.db.cursor()
		try:
			self.cursor.execute("SELECT * FROM users WHERE user_id=%s" % str(userID))
			result = self.cursor.fetchone()
			return result[1]
		except:
			self._logError("ERROR: retrieving userName from id")
		self.cursor.close()

	"""
	takes in the username and returns the user's id
	"""
	def getIDFromUsername(self, userName):
		self.cursor = self.db.cursor()
		try:
			self.cursor.execute("SELECT * FROM users WHERE username=\'%s\'" % userName)
			result = self.cursor.fetchone()
			return result[0]
		except:
			self._logError("ERROR: retrieving id from userName")
		self.cursor.close()

	"""
	executes external input
	"""
	def cursorExecute(self, command):
		self.cursor = self.db.cursor()
		try:
			self.cursor.execute(command)
		except:
			self.db.rollback()
			self._logError("ERROR: executing custom command")
		self.cursor.close()

	"""
	inserts quote data into quote table
	"""
	def insertQuote(self, userName, quote):
		self.cursor = self.db.cursor()
		date = str(datetime.datetime.now())[:19]
		uid = self.getIDFromUsername(userName)
		try:
			self.cursor.execute("INSERT INTO quote VALUES (NULL, %s, \'%s\', \'%s\')" 
				% (str(uid), date, quote) )
			self.db.commit()
			self.cursor.execute("SELECT id FROM quote WHERE data=\'%s\'" % quote)
			qid = self.cursor.fetchall()[-1][0]
			self.cursor.close()
			return qid
		except:
			self.db.rollback()
			self._logError("ERROR: inserting quote")
		self.cursor.close()


	"""
	queries quotes
	"""
	def queryQuote(self, qid):
		self.cursor = self.db.cursor()
		try:
			if qid == 0:
				self.cursor.execute("SELECT COUNT( * ) FROM quote")
				maxVal = self.cursor.fetchone()[0]
				quoteId = random.randint(1, maxVal)
				self.cursor.execute("SELECT * FROM quote where id=\'%s\'" % quoteId)
				quote = self.cursor.fetchone()
				self.cursor.close()
				date = "%s" % str(quote[2])[:10]
				quote = "\"%s\" - %s (#%s)" % (quote[3], date, str(quote[0]))
				return quote
			else:
				self.cursor.execute("SELECT * FROM quote where id=\'%s\'" % qid)
				quote = self.cursor.fetchone()
				self.cursor.close()
				date = "%s" % str(quote[2])[:10]
				quote = "\"%s\" - %s (#%s)" % (quote[3], date, str(quote[0]))
				return quote
		except:
			pass
		self.cursor.close()

	"""
	Deletes the quote based on id
	"""
	def deleteQuote(self, qid):
		self.cursor = self.db.cursor()
		try:
			self.cursor.execute("DELETE FROM quote WHERE id=%s" % qid)
			self.db.commit()
			self.cursor.close()
		except:
			self.cursor.rollback()
		self.cursor.close()

	"""
	inserts the username into the 'users' table
	"""
	def _insertUserIntoID(self, userName):
		self.cursor = self.db.cursor()
		try:
			self.cursor.execute("INSERT INTO users VALUES ( NULL , \'%s\')" % userName)
			self.db.commit()
		except:
			self.db.rollback() #unable to ERROR LOG since it'll be an error most times
		self.cursor.close()

	"""
	used for exiting the program and logging things
	"""
	def _logError(self, msg):
		date = datetime.datetime.now()
		try:
			txt = open("errorlogs/" + str(date)[:19] + ".txt" ,"w")
			txt.write(msg + '\n')
			txt.close()
		except:
			print "CRITICAL ERROR: LOGGING HISTORY"