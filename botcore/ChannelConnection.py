from .dbconnector import dbconnector
from .twitchconnector import twitchconnector
#from .commandmanager import commandmanager
#from .startupmanager import startupmanager

class ChannelConnection:
	def __init__(self):
		print("a")
		self.db = dbconnector()
		print("b")
		#self.cleaner = inputmanager()
		#self.cmd = commandmanager()


	def run(self):
		"""
		Main Loop 
		"""
		twitch = twitchconnector(self.db.getTwitchConfig())

		while twitch.IsConnectionAlive():
			# blocking
			msg = twitch.getMessage()

			self.db.logMessage(msg)


			#Just puts out things into console
			print(msg.getRawMessage())
