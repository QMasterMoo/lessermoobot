import os

class startupmanager:


	def __init__(self):
		"""
		Creates and modifies a file named 'version'
		which contains the internal version number which will help
		when updating structures in mysql or anything else
		"""
		self.currentInternalVersion = '2'
		try:
			lock = open('botcore/version', 'r+')
			self.version = int(lock.readline())
			lock.close()
		except:
			self.version = 0
		#Since there isn't a way to delete a single line I rewrite over it
		lock = open('botcore/version', 'w')
		lock.write(self.currentInternalVersion)
		lock.close()

	def outVersion(self):
		"""
		Test functions
		"""
		print self.version


	def checkUpdate(self, db):
		"""
		checks the version for updates
		does the functions required for an update if needed
		"""
		self.db = db
		self._makeFolders()
		if self.version <= 0:
			self._initTables()
			print "First time setup complete!"
			print "If lmb was already setup and you see this something went wrong!"
		if self.version <= 1:
			self._initQuoteTable()
			self._makeNextGameFile()
			print "Lessermoobot has updated (1)!"
		"""
		How to add future update versions etc...
		if self.version <= 1:
			print "next version thing etc..."
		"""


	def _initTables(self):
		"""
		creates the tables needed in the database
		"""
		#Creates the log table
		self.db.cursorExecute("CREATE TABLE log (\
			id INT UNSIGNED NOT NULL AUTO_INCREMENT, \
			user_id INT UNSIGNED NOT NULL, \
			date DATETIME NOT NULL, \
			type CHAR(100) NOT NULL, \
			data VARCHAR(60000) NOT NULL, \
			PRIMARY KEY (id)\
			);")
		#Creates the users table
		self.db.cursorExecute("CREATE TABLE users (\
			user_id INT UNSIGNED NOT NULL AUTO_INCREMENT, \
			userName CHAR(100) NOT NULL UNIQUE, \
			PRIMARY KEY (user_id)\
			);")


	def _makeFolders(self):
		"""
		creates the neccessary subfolders for the history and logs
		"""
		if not os.path.isdir('logs'):
			os.makedirs('logs')
		if not os.path.isdir('logs/history'):
			os.makedirs('logs/history')
		if not os.path.isdir('errorlogs'):
			os.makedirs('errorlogs')
		if not os.path.isdir('customfiles'):
			os.makedirs('customfiles')


	def _initQuoteTable(self):
		"""
		creates the tables needed for !quote
		"""
		self.db.cursorExecute("CREATE TABLE quote (\
			id INT UNSIGNED NOT NULL AUTO_INCREMENT, \
			user_id INT UNSIGNED NOT NULL, \
			date DATETIME NOT NULL, \
			data VARCHAR(2000) NOT NULL, \
			PRIMARY KEY (id) \
			);")

	def _makeNextGameFile(self):
		"""
		makes the file
		"""
		txt = open('customfiles/nextgame', 'w')
		txt.close()