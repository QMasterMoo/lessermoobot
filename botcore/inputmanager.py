from config import twitchBotUsername
import datetime
import re

class inputmanager:

	def __init__(self):
		self.data = ""

	def clean(self, data):
		self.data = data
		if not self.isPing() and not self._isMode():
			self.mode = self._getMode()
			self.userName = self._findUserName(self.data)
			#NOTICE type no longer needed, but left if we want
			if self.mode == 'NOTICE':
				return None
			elif self.mode == "PRIVMSG":
				return [self.userName, self._getTime(), self.mode, self._cleanPRIVMSG()]
			elif self.mode == 'CLEARCHAT':
				return [self.userName, self._getTime(), self.mode, self._cleanCLEARCHAT()]
			else:
				return None

	def _findUserName(self, data):
		try:
			self.userName = re.sub('[^a-zA-Z0-9_]','', data.split('!')[0])
			return self.userName
		except:
			return "error.finding.userName"

	def isPing(self):
		return (self.data[0:6] == "PING :")

	def _isMode(self):
		return (self.data[1:6] == "jtv M")

	def _getMode(self):
		try:
			self.mode = self.data.split('.tv ')[1]
			self.mode = self.mode.split(' #')[0]
			return self.mode
		except:
			return "unknown"

	def _cleanNOTICE(self):
		return ""

	def _cleanPRIVMSG(self):
		self.message = ""
		self.messageRay = self.data[1:].split(':',1)[1:]
		for i in self.messageRay:
			self.message = self.message + i.strip('\r\n')
		return self.message

	def _cleanCLEARCHAT(self):
		self.ban = ""
		self.banRay = self.data[1:].split(' :')[1:]
		for i in self.banRay:
			self.ban = self.ban + i.strip('\r\n')
		return self.ban

	def _getTime(self):
		self.dateTime= ""
		self.date = datetime.datetime.now()
		return str(self.date)[:19]