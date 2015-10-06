import datetime #will be used for command cooldowns

class commandmanager:

	def __init__(self):
		#Eventually will have more commands
		self.asdfjkl = "I will eventually init text based commands here"

	#username in here is for seeing if the user is mod or not
	#idk where to put check for mod or if I'm doing it through urllib and json or mysql
	def manage(self, userName, data, db):
		self.db = db
		self._historyManager(data)

	def _historyManager(self, data):
		data = ':' + data
		if not data.find(":!history "):
			dataSplit = data.split(":!history ")[1:]
			try:
				data = ""
				for obj in dataSplit:
					data = data + obj
				spaceSplit = data.split(' ')
				self._historyUserCustom(spaceSplit[0], int(spaceSplit[1]))
			except:
				self._historyUser(dataSplit[0])

	"""
	TODO: Write !quote methods
		adds quote and such to a seperate database
	"""

	"""
	TODO: Write !log methods
		creates a generic log for last x messages
	"""

	def _historyUser(self, userName):
		self.db.logHistory(userName, 200)

	def _historyUserCustom(self, userName, length):
		self.db.logHistory(userName, length)