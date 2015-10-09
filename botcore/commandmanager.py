import datetime #will be used for command cooldowns
from writer import writer
from config import logSite, subMessage, resubMessage

class commandmanager:

	def __init__(self):
		#Eventually will have more commands
		self.logger = writer()
		self.asdfjkl = "I will eventually init text based commands here"

	#username in here is for seeing if the user is mod or not
	#idk where to put check for mod or if I'm doing it through urllib and json or mysql
	"""
	Invokes the various hardcoded managers
	Support for other commands will come in the future
	"""
	def manage(self, userName, data, db, serv):
		self.db = db
		self.dataIn = data
		#Not sure how to make this done without intermediary variables
		hManage = self._historyManager()
		lManage = self._logManager()
		sManage = self._subManager(userName, serv)
		if not hManage == None:
			return hManage
		elif not lManage == None:
			return lManage
		else:
			return None


	"""
	Manages the finding and executing of the !history userName command
	"""
	def _historyManager(self):
		data = ':' + self.dataIn
		if not data.find(":!history "):
			dataSplit = data.split(":!history ")[1:]
			try:
				data = ""
				for obj in dataSplit:
					data = data + obj
				spaceSplit = data.split(' ')
				self.logger.logToFileHistory(spaceSplit[0] , 
					self._historyUserCustom(spaceSplit[0], int(spaceSplit[1])))
				return "%s/history/%s.txt" % (logSite, spaceSplit[0])
			except:
				self.logger.logToFileHistory(spaceSplit[0] , 
					self._historyUser(dataSplit[0]) )
				return "%s/history/%s.txt" % (logSite, dataSplit[0])
		else:
			return None

	"""
	Manages the finding and executing of the !log command
	"""
	def _logManager(self):
		data = ':' + self.dataIn
		if not data.find(":!log"):
			try:
				dataSplit = data.split(":!log ")[1]
				self.logger.logToFile(self._logCustom(int(dataSplit)), self.db)
				return "%s/log.txt" % logSite
			except:
				self.logger.logToFile(self._log(), self.db)
				return "%s/log.txt" % logSite
		else:
			return None

	"""
	TODO: Write !quote methods
		adds quote and such to a seperate table on mysql, not planned for 
		initial release, see #12
	"""

	"""
	TODO: implement
	This method takes in the serv object (connection to twitch server)
	which is used to send message to the twitch server thanking people for subbing
	"""
	def _subManager(self, userName, serv):
		return

	"""
	Queries database for last 200 messages for the user
	"""
	def _historyUser(self, userName):
		return self.db.queryHistory(userName, 200)

	"""
	Queries database for last length messages for the user
	"""
	def _historyUserCustom(self, userName, length):
		return self.db.queryHistory(userName, length)

	"""
	Queries database for last 500 messages
	"""
	def _log(self):
		return self.db.queryLog(500)

	"""
	Queries database for last length messages
	"""
	def _logCustom(self, length):
		return self.db.queryLog(length)

