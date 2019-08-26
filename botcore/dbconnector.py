import datetime
# from .config import databaseAddress, databaseUser, databaseUserPass, databaseName
import sys
import random

import mysql.connector

class dbconnector:

	
	def __init__(self):
		"""
		initializes the database
		"""
		try:
			self.db = mysql.connector.connect(host='',
												user='', 
												passwd='', 
												database='')
			print("aa")
			#cursor = self.db.cursor(dictionary=True)
			self.BotUserID = 1
			self.ChannelID = 1

		except:
			#self._logError("CRITICAL ERROR: CONNECTING TO DATABASE")
			sys.exit(0)


	def logMessage(self, msg):
		"""
		It inserts everything into the log
		"""
		cursor = self.db.cursor()
		try:
			#args = [userName, messageDate,messageText]
			args = ['test123', '', messageText]
			cursor.callproc('spInsertMessage', args)
			#self.db.commit()
		except:
			self.db.rollback()
		cursor.close()

	def getTwitchConfig(self):
		# evntualy useful
		cursor = self.db.cursor(dictionary=True)

		config = {
			"ChannelName": "",
			"BotUsername": "",
			"OAuthKey": ""
		}

		cursor.execute("SELECT C.ChannelName FROM Channels C WHERE C.ChannelID = (%s)", (self.ChannelID,))
		config["ChannelName"] = cursor.fetchone()["ChannelName"]

		cursor.execute("SELECT BU.BotUsername, BU.OAuthKey FROM BotUsers BU WHERE BU.BotuserID = (%s) ", (self.BotUserID,))
		result = cursor.fetchone()
		config["BotUsername"] = result["BotUsername"]
		config["OAuthKey"] = result["OAuthKey"]
		
		cursor.close()

		return config

	# def queryLog(self, length):
	# 	"""
	# 	queries data for general log
	# 	"""
	# 	self.cursor = self.db.cursor()
	# 	try:
	# 		self.cursor.execute("SELECT COUNT( * ) FROM log")
	# 		maxVal = self.cursor.fetchone()[0]
	# 		minVal = maxVal - length
	# 		if minVal < 0:
	# 			minVal = 0
	# 		self.cursor.execute("SELECT * FROM  log LIMIT %s , %s" % (minVal, maxVal))
	# 		output = self.cursor.fetchall()
	# 		self.cursor.close()
	# 		return output
	# 	except:
	# 		self._logError("ERROR: querying in general")
	# 	self.cursor.close()



	# def queryType(self, mode, length):
	# 	"""
	# 	Queries for a specific mode or type
	# 	It's untested, but should work
	# 	"""
	# 	self.cursor = self.db.cursor()
	# 	try: 
	# 		self.cursor.execute("SELECT COUNT( * ) FROM log WHERE type = \'%s\'" % (mode))
	# 		maxVal = self.cursor.fetchone()[0]
	# 		minVal = maxVal - length
	# 		if minVal < 0:
	# 			minVal = 0
	# 		self.cursor.execute("SELECT * FROM  log WHERE type = \'%s\' LIMIT %s , %s" % (mode, minVal, maxVal))
	# 		output = self.cursor.fetchall()
	# 		print output
	# 		self.cursor.close()
	# 		return output
	# 	except:
	# 	    self._logError("ERROR: quering type")
	# 	self.cursor.close()


	# def queryHistory(self, userName, length):
	# 	"""
	# 	queries data for general log
	# 	"""
	# 	self.cursor = self.db.cursor()
	# 	uid = self.getIDFromUsername(userName)
	# 	try:
	# 		self.cursor.execute("SELECT COUNT( * ) FROM log WHERE user_id = %s" % str(uid) )
	# 		maxVal = self.cursor.fetchone()[0]
	# 		minVal = maxVal - length
	# 		if minVal < 0:
	# 			minVal = 0
	# 		self.cursor.execute("SELECT * FROM log WHERE user_id = %s LIMIT %s, %s" % (uid, minVal, maxVal))
	# 		output = self.cursor.fetchall()
	# 		self.cursor.close()
	# 		return output
	# 	except:
	# 		self._logError("ERROR: querying history")
	# 	self.cursor.close()


	# def getUsernameFromID(self, userID):
	# 	"""
	# 	retrieves username from id
	# 	"""
	# 	self.cursor = self.db.cursor()
	# 	try:
	# 		self.cursor.execute("SELECT * FROM users WHERE user_id=%s" % str(userID))
	# 		result = self.cursor.fetchone()
	# 		return result[1]
	# 	except:
	# 		self._logError("ERROR: retrieving userName from id")
	# 	self.cursor.close()



	# def getIDFromUsername(self, userName):
	# 	"""
	# 	takes in the username and returns the user's id
	# 	"""
	# 	self.cursor = self.db.cursor()
	# 	try:
	# 		self.cursor.execute("SELECT * FROM users WHERE username=\'%s\'" % userName)
	# 		result = self.cursor.fetchone()
	# 		return result[0]
	# 	except:
	# 		self._logError("ERROR: retrieving id from userName")
	# 	self.cursor.close()


	# def cursorExecute(self, command):
	# 	"""
	# 	executes external input
	# 	"""
	# 	self.cursor = self.db.cursor()
	# 	try:
	# 		self.cursor.execute(command)
	# 	except:
	# 		self.db.rollback()
	# 		self._logError("ERROR: executing custom command")
	# 	self.cursor.close()


	# def insertQuote(self, userName, quote):
	# 	"""
	# 	inserts quote data into quote table
	# 	"""
	# 	self.cursor = self.db.cursor()
	# 	date = str(datetime.datetime.now())[:19]
	# 	uid = self.getIDFromUsername(userName)
	# 	try:
	# 		self.cursor.execute("INSERT INTO quote VALUES (NULL, %s, \'%s\', \'%s\')" 
	# 			% (str(uid), date, quote) )
	# 		self.db.commit()
	# 		self.cursor.execute("SELECT id FROM quote WHERE data=\'%s\'" % quote)
	# 		qid = self.cursor.fetchall()[-1][0]
	# 		self.cursor.close()
	# 		return qid
	# 	except:
	# 		self.db.rollback()
	# 		self._logError("ERROR: inserting quote")
	# 	self.cursor.close()



	# def queryQuote(self, qid):
	# 	"""
	# 	queries quotes
	# 	"""
	# 	self.cursor = self.db.cursor()
	# 	try:
	# 		if qid == 0:
	# 			self.cursor.execute("SELECT * FROM quote AS r1 JOIN ( \
	# 				SELECT CEIL( RAND( ) * ( SELECT MAX( id ) FROM quote )) AS id) AS r2 \
	# 				WHERE r1.id >= r2.id ORDER BY r1.id ASC LIMIT 1")
	# 			quote = self.cursor.fetchone()
	# 			self.cursor.close()
	# 			date = "%s" % str(quote[2])[:10]
	# 			quote = "\"%s\" - %s (#%s)" % (quote[3], date, str(quote[0]))
	# 			return quote
	# 		else:
	# 			self.cursor.execute("SELECT * FROM quote where id=\'%s\'" % qid)
	# 			quote = self.cursor.fetchone()
	# 			self.cursor.close()
	# 			date = "%s" % str(quote[2])[:10]
	# 			quote = "\"%s\" - %s (#%s)" % (quote[3], date, str(quote[0]))
	# 			return quote
	# 	except:
	# 		pass
	# 	self.cursor.close()
	# 	return "error retreiving quote"


	# def deleteQuote(self, qid):
	# 	"""
	# 	Deletes the quote based on id
	# 	"""
	# 	self.cursor = self.db.cursor()
	# 	try:
	# 		self.cursor.execute("DELETE FROM quote WHERE id=%s" % qid)
	# 		self.db.commit()
	# 		self.cursor.close()
	# 	except:
	# 		self.cursor.rollback()
	# 	self.cursor.close()



	# def _logError(self, msg):
	# 	"""
	# 	used for exiting the program and logging things
	# 	"""
	# 	date = datetime.datetime.now()
	# 	try:
	# 		txt = open("errorlogs/" + str(date)[:19] + ".txt" ,"w")
	# 		txt.write(msg + '\n')
	# 		txt.close()
	# 	except:
	# 		print "CRITICAL ERROR: LOGGING HISTORY"