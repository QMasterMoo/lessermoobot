import datetime

class writer:

	def __init__(self):
		self.thing = ""

	"""
	Writes the !log to a file
	"""
	def logToFile(self, data, db):
		try:
			txt = open("logs/log.txt", 'w')
			for line in data:
				lineOut = '[' + str(line[2]) + '] ' + db.getUsernameFromID(line[1]) + ': ' + line[4] + '\n'
				txt.write(lineOut)
			txt.close()
		except:
			print "error logging history"

	"""
	Writes user's !history to file
	"""
	def logToFileHistory(self, userName, data):
		try:
			txt = open("logs/history/" + userName + ".txt", 'w')
			for line in data:
				lineOut = '[' + str(line[2]) + '] ' + userName + ': ' + line[4] + '\n'
				txt.write(lineOut)
			txt.close()
		except:
			print "error logging history"

	"""
	Writes (as a string) custom data to a custom file
	Only writes to one single line
	"""
	def writeCustomFile(self, fileName, data):
		try:
			txt = open("customfiles/" + fileName, 'w+')
			txt.write(str(data))
			txt.close()
		except:
			print "error creating custom file"

	"""
	Reads (as a string) a single line of data from a custom file
	When used with writeCustomFile() file it'll work, otherwise be careful with multiple lines
	"""
	def readCustomFile(self, fileName):
		try: 
			txt = open("customfiles/" + fileName, 'r+')
			out = txt.readline()
			txt.close()
			return out
		except:
			print "error reading file or the file does not yet exist"