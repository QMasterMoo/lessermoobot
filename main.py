from botcore.dbconnector import dbconnector
from botcore.twitchconnector import twitchconnector
from botcore.inputmanager import inputmanager
from botcore.commandmanager import commandmanager
import MySQLdb

class main:
	def __init__(self):
		self.db = dbconnector()
		self.serv = twitchconnector()
		self.cleaner = inputmanager()
		self.cmd = commandmanager()

con = main()

while True:
	"""
	Takes in data and sends it off to the cleaner
	"""
	raw = con.serv.getData()
	output = con.cleaner.clean(raw, con.cmd, con.db, con.serv)

	"""
	Tests if it's a valid output and not None, if so it logs it
	"""
	if not output == None:
		con.db.insertMessageIntoLog(output[0], output[1], output[2], output[3])


	#Just puts out things into console
	if not output == None:
		print output


