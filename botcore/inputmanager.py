from config import twitchBotUsername
import datetime
import re

class inputmanager:

	#I don't want it to be empty so I make this here
	def __init__(self):
		pass


	def clean(self, messageData):
		"""
		Takes in the raw data and sends it off to the various sub methods to
		   be cleaned from extra things and replies with the userName, time,
		   mode or type that the message was sent through, and the chat.
		"""
		pass
		# if not self.isPing() and not self._isMode():
		# 	self.mode = self._getMode()
		# 	#left in just in case I decide to track hosts/unhosts
		# 	if self.mode == 'NOTICE':
		# 		return None
		# 	elif self.mode == "PRIVMSG":
		# 		output = [self._findUserNamePRIVMSG(), self._getTime(), self.mode, self._cleanPRIVMSG()]
		# 		cmd.manage(output[0], output[3], db, serv) #Not sure how to make this done without intermediary variables
		# 		return output
		# 	elif self.mode == 'CLEARCHAT':
		# 		output = [self._findUserNameCLEARCHAT(), self._getTime(), self.mode, 
		# 				"CLEARCHAT FOR %s@%s" % (self._findUserNameCLEARCHAT(), self._getTime())]
		# 		return output
		# 	else:
		# 		return None
		# elif self.isPing():
		# 	serv.ping()


	def isPing(self):
		"""
		determines if the message is a ping
		"""
		return (self.data[0:6] == "PING :")


	def _findUserNamePRIVMSG(self):
		"""
		finds the userName of the person who sent the message or whatever
		   does NOT work with CLEARCHAT
		"""
		try:
			userName = re.sub('[^a-zA-Z0-9_]','', self.data.split('!')[0])
			return userName
		except:
			return "error.finding.userName"


	def _isMode(self):
		"""
		determines if it's a mode thing that normally breaks the bot
		"""
		return (self.data[1:6] == "jtv M")


	def _getMode(self):
		"""
		finds the mode or message type of the data
		"""
		try:
			self.mode = self.data.split('.tv ')[1]
			self.mode = self.mode.split(' #')[0]
			return self.mode
		except:
			return "unknown"


	def _cleanNOTICE(self):
		"""
		useless method right now since NOTICE isn't used in this program
		"""
		return ""


	def _cleanPRIVMSG(self):
		"""
		cleans the PRIVMSG mode/type
		"""
		self.message = ""
		self.messageRay = self.data[1:].split(':',1)[1:]
		for i in self.messageRay:
			self.message = self.message + i.strip('\r\n')
		return self.message


	def _cleanCLEARCHAT(self):
		"""
		cleans the CLEARCHAT type
		"""
		self.ban = ""
		self.banRay = self.data[1:].split(' :')[1:]
		for i in self.banRay:
			self.ban = self.ban + i.strip('\r\n')
		return self.ban


	def _findUserNameCLEARCHAT(self):
		"""
		clearchat has no userName so instead it returns the userName of 
		   the person who was timed out
		"""
		try:
			userName = re.sub('[^a-zA-Z0-9_]','', self.data.split(':')[2])
			return userName
		except:
			return "error.finding.userName"


	def _getTime(self):
		"""
		returns the time ready for mysql logging
		"""
		self.dateTime= ""
		self.date = datetime.datetime.now()
		return str(self.date)[:19]