import datetime

class writer:

	def __init__(self):
		self.thing = ""

	"""
	Writes the !log to a file
	"""
	def logToFile(self, data, db):
		try:
			txt = open("logs/log.txt","w")
			for line in data:
				lineOut = '[' + str(line[2]) + '] ' + db.getUsernameFromID(line[1]) + ': ' + line[4] + '\n'
				txt.write(lineOut)
			txt.close()
		except:
			print("error logging history")

	"""
	Writes user's !history to file
	"""
	def logToFileHistory(self, userName, data):
		try:
			txt = open("logs/history/" + userName + ".txt","w")
			for line in data:
				lineOut = '[' + str(line[2]) + '] ' + userName + ': ' + line[4] + '\n'
				txt.write(lineOut)
			txt.close()
		except:
			print("error logging history")
