import os

class startupmanager:

	"""
	Creates and modifies a file named 'version'
	which contains the internal version number which will help
	when updating structures in mysql or anything else
	"""
	def __init__(self):
		self.currentInternalVersion = '1'
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
		print self.version

	"""
	checks the version for updates
	does the functions required for an update if needed
	"""
	def checkUpdate(self, db):
		self.db = db
		self._makeFolders()
		if self.version <= 0:
			self._initTables()
			print "First time setup complete!"
			print "If lmb was already setup and you see this something went wrong!"
		"""
		How to add future update versions etc...
		if self.version <= 1:
			print "next version thing etc..."
		"""

	"""
	creates the tables needed in the database
	"""
	def _initTables(self):
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

	"""
	creates the neccessary subfolders for the history and logs
	"""
	def _makeFolders(self):
		if not os.path.isdir('logs'):
			os.makedirs('logs')
		if not os.path.isdir('logs/history'):
			os.makedirs('logs/history')
		if not os.path.isdir('errorlogs'):
			os.makedirs('errorlogs')
		if not os.path.isdir('customfiles'):
			os.makedirs('customfiles')