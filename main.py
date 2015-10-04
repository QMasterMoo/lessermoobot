from botcore.dbconnector import dbconnector
from botcore.twitchconnector import twitchconnector
from botcore.inputmanager import inputmanager
import MySQLdb

class main:
	def __init__(self):
		self.db = dbconnector()
		self.serv = twitchconnector()
		self.cleaner = inputmanager()

con = main()

while True:
	"""
	Takes in data and sends it off to the cleaner
	"""
	output = con.serv.getData()
	output = con.cleaner.clean(output)

	"""
	Manages the ping
	"""
	if con.cleaner.isPing():
		con.serv.ping()

	"""
	Tests if it's a valid output and not None, if so it logs it
	"""
	if not output == None:
		con.db.insertMessageIntoLog(output[0], output[1], output[2], output[3])


	#temporary thing for testing?
	print output


