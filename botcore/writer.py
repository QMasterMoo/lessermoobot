import datetime

class writer:

	def __init__(self):
		self.thing = ""


	def logToFile(self, data, db):
		"""
		Writes the !log to a file
		"""
		try:
			txt = open("logs/log.txt", 'w')
			for line in data:
				lineOut = '[' + str(line[2]) + '] ' + db.getUsernameFromID(line[1]) + ': ' + line[4] + '\n'
				txt.write(lineOut)
			txt.close()
		except:
			print "error logging history"


	def logToFileHistory(self, userName, data):
		"""
		Writes user's !history to file
		"""
		try:
			txt = open("logs/history/" + userName + ".txt", 'w')
			for line in data:
				lineOut = '[' + str(line[2]) + '] ' + userName + ': ' + line[4] + '\n'
				txt.write(lineOut)
			txt.close()
		except:
			print "error logging history"


	def writeCustomFile(self, fileName, data):
		"""
		Writes (as a string) custom data to a custom file
		Only writes to one single line
		"""
		try:
			txt = open("customfiles/" + fileName, 'w+')
			txt.write(str(data))
			txt.close()
		except:
			print "error creating custom file"


	def readCustomFile(self, fileName):
		"""
		Reads (as a string) a single line of data from a custom file
		When used with writeCustomFile() file it'll work, otherwise be careful with multiple lines
		"""
		try: 
			txt = open("customfiles/" + fileName, 'r+')
			out = txt.readline()
			txt.close()
			return out
		except:
			print "error reading file or the file does not yet exist"