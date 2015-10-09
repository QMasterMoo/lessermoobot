from config import twitchBotUsername
import datetime
import re

class inputmanager:

	#I don't want it to be empty so I make this here
	def __init__(self):
		self.mode = ""

	"""
	Takes in the raw data and sends it off to the various sub methods to
	   be cleaned from extra things and replies with the userName, time,
	   mode or type that the message was sent through, and the chat.
	"""
	def clean(self, data, cmd, db, serv):
		self.data = data
		if not self.isPing() and not self._isMode():
			self.mode = self._getMode()
			#left in just in case I decide to track hosts/unhosts
			if self.mode == 'NOTICE':
				return None
			elif self.mode == "PRIVMSG":
				output = [self._findUserNamePRIVMSG(), self._getTime(), self.mode, self._cleanPRIVMSG()]
				manageOut = cmd.manage(output[0], output[3], db, serv) #Not sure how to make this done without intermediary variables
				if not manageOut == None:
					serv.msg(manageOut)
				return output
			elif self.mode == 'CLEARCHAT':
				output = [self._findUserNameCLEARCHAT(), self._getTime(), self.mode, 
						"CLEARCHAT FOR %s@%s" % (self._findUserNameCLEARCHAT(), self._getTime())]
				return output
			else:
				return None
		elif self.isPing():
			serv.ping()

	"""
	determines if the message is a ping
	"""
	def isPing(self):
		return (self.data[0:6] == "PING :")

	"""
	finds the userName of the person who sent the message or whatever
	   does NOT work with CLEARCHAT
	"""
	def _findUserNamePRIVMSG(self):
		try:
			userName = re.sub('[^a-zA-Z0-9_]','', self.data.split('!')[0])
			return userName
		except:
			return "error.finding.userName"

	"""
	determines if it's a mode thing that normally breaks the bot
	"""
	def _isMode(self):
		return (self.data[1:6] == "jtv M")

	"""
	finds the mode or message type of the data
	"""
	def _getMode(self):
		try:
			self.mode = self.data.split('.tv ')[1]
			self.mode = self.mode.split(' #')[0]
			return self.mode
		except:
			return "unknown"

	"""
	useless method right now since NOTICE isn't used in this program
	"""
	def _cleanNOTICE(self):
		return ""

	"""
	cleans the PRIVMSG mode/type
	"""
	def _cleanPRIVMSG(self):
		self.message = ""
		self.messageRay = self.data[1:].split(':',1)[1:]
		for i in self.messageRay:
			self.message = self.message + i.strip('\r\n')
		return self.message

	"""
	cleans the CLEARCHAT type
	"""
	def _cleanCLEARCHAT(self):
		self.ban = ""
		self.banRay = self.data[1:].split(' :')[1:]
		for i in self.banRay:
			self.ban = self.ban + i.strip('\r\n')
		return self.ban

	"""
	clearchat has no userName so instead it returns the userName of 
	   the person who was timed out
	"""
	def _findUserNameCLEARCHAT(self):
		try:
			userName = re.sub('[^a-zA-Z0-9_]','', self.data.split(':')[2])
			return userName
		except:
			return "error.finding.userName"

	"""
	returns the time ready for mysql logging
	"""
	def _getTime(self):
		self.dateTime= ""
		self.date = datetime.datetime.now()
		return str(self.date)[:19]