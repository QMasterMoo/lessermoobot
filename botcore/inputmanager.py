from config import twitchBotUsername
import datetime
import re

class inputmanager:

	#I don't want it to be empty so I make this here
	def __init__(self):
		self.data = ""
		self.mode = ""

	"""
	R: data from the irc interface
	M: n/a
	E: Takes in the data and sends it off to the various sub methods to
	   be cleaned from extra things and replies with the userName, time,
	   mode or type that the message was sent through, and the chat.
	See issue #2 for possible optimization
	"""
	def clean(self, data):
		self.data = data
		if not self.isPing() and not self._isMode():
			self.mode = self._getMode()
			#NOTICE might not be needed
			if self.mode == 'NOTICE':
				return None
			elif self.mode == "PRIVMSG":
				return [self._findUserName(), self._getTime(), self.mode, self._cleanPRIVMSG()]
			elif self.mode == 'CLEARCHAT':
				return [self._findUserNameCLEARCHAT(), self._getTime(), self.mode, 
						"CLEARCHAT FOR %s@%s" % (self._findUserNameCLEARCHAT(), self._getTime())]
			else:
				return None

	"""
	R: n/a
	M: n/a
	E: determines if the message is a ping
	"""
	def isPing(self):
		return (self.data[0:6] == "PING :")

	"""
	R: n/a
	M: self.userName
	E: finds the userName of the person who sent the message or whatever
	   does NOT work with CLEARCHAT
	"""
	def _findUserName(self):
		try:
			self.userName = re.sub('[^a-zA-Z0-9_]','', self.data.split('!')[0])
			return self.userName
		except:
			return "error.finding.userName"

	"""
	R: n/a
	M: n/a
	E: determines if it's a mode thing that normally breaks the bot
	"""
	def _isMode(self):
		return (self.data[1:6] == "jtv M")

	"""
	R: n/a
	M: self.mode
	E: finds the mode or message type of the data
	"""
	def _getMode(self):
		try:
			self.mode = self.data.split('.tv ')[1]
			self.mode = self.mode.split(' #')[0]
			return self.mode
		except:
			return "unknown"

	"""
	R: n/a
	M: n/a
	E: useless method right now since NOTICE isn't used in this program
	"""
	def _cleanNOTICE(self):
		return ""

	"""
	R: n/a
	M: n/a
	E: cleans the PRIVMSG mode/type
	"""
	def _cleanPRIVMSG(self):
		self.message = ""
		self.messageRay = self.data[1:].split(':',1)[1:]
		for i in self.messageRay:
			self.message = self.message + i.strip('\r\n')
		return self.message

	"""
	R: n/a
	M: n/a
	E: cleans the CLEARCHAT type
	"""
	def _cleanCLEARCHAT(self):
		self.ban = ""
		self.banRay = self.data[1:].split(' :')[1:]
		for i in self.banRay:
			self.ban = self.ban + i.strip('\r\n')
		return self.ban

	"""
	R: n/a
	M: self.userName
	E: clearchat has no userName so instead it returns the userName of 
	   the person who was timed out
	"""
	def _findUserNameCLEARCHAT(self):
		try:
			self.userName = re.sub('[^a-zA-Z0-9_]','', self.data.split(':')[2])
			return self.userName
		except:
			return "error.finding.userName"

	"""
	R: n/a
	M: n/a
	E: returns the time ready for mysql logging
	"""
	def _getTime(self):
		self.dateTime= ""
		self.date = datetime.datetime.now()
		return str(self.date)[:19]