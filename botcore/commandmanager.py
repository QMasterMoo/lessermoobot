import datetime #will be used for command cooldowns
import json
import urllib2
from writer import writer
from config import logSite, subMessage, resubMessage, twitchChannel

class commandmanager:

	def __init__(self):
		#Eventually will init commands from file x
		self.logger = writer()
		self.currentMinute = 0
		self.lastMinute = -1
		self.modList = ['moomasterq']#as long as this isn't empty the bot will work

	"""
	Invokes the various hardcoded managers
	Support for other commands will come in the future
	"""
	def manage(self, userName, data, db, serv):
		self.db = db
		self.dataIn = data
		self.currentMinute = datetime.datetime.now().minute
		self._subManager(userName, serv)#passing serv allows sending multiple messages
		#Not sure how to do without variables since I don't want to call it twice
		if userName in self.getModList():
			hManage = self._historyManager()
			lManage = self._logManager()
			if not hManage == None:
				return hManage
			elif not lManage == None:
				return lManage
			else:
				return None
		else:
			return None

	"""
	Returns the mod list in a list
	See issue #15
	"""
	def getModList(self):
		if self.currentMinute != self.lastMinute: #Anti flood measure for tmi
			self.lastMinute = self.currentMinute
			self.modList = ['moomasterq']#resets mod list
			modJSON= urllib2.urlopen("https://tmi.twitch.tv/group/user/%s/chatters" % twitchChannel[1:])
			modJSON = json.loads(modJSON.read().decode("utf-8"))
			for userLevel in ['staff','admins','global_mods','moderators']:
				if modJSON["chatters"][userLevel]:
					for user in modJSON["chatters"][userLevel]:
						self.modList.append(user)
		return self.modList

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
	This method takes in the serv object (connection to twitch server)
	which is used to send message to the twitch server thanking people for subbing
	"""
	def _subManager(self, userName, serv):
		if userName == "twitchnotify":
			dataSplit = self.dataIn.split(' ')
			subName = dataSplit[0]
			subType = dataSplit[1]
			if subType == 'subscribed':
				subMonth = dataSplit[3]
				serv.msg(resubMessage % (subName, subMonth))
			else:
				serv.msg(subMessage % subName)

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

