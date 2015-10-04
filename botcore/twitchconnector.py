from config import twitchServer, twitchPort, twitchChannel, twitchBotUsername, twitchBotPassword
import socket

class twitchconnector:
	#RME: creates connection to server
	def __init__(self):
		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.irc.connect((twitchServer, twitchPort))
		self.irc.send("CAP REQ :twitch.tv/membership \n")
		self.irc.send("CAP REQ :twitch.tv/commands \n")
		self.irc.send("PASS " + twitchBotPassword + "\n")
		self.irc.send("NICK "+ twitchBotUsername +"\n")
		self.irc.send("USER "+ twitchBotUsername + "\n")
		self.irc.send("JOIN " + twitchChannel + "\n")

	"""
	R: n/a
	M: n/a
	E: replies with to twitch's pings so we don't get kicked out
	"""
	def ping(self):
		self.irc.send("PONG :ping\n")

	"""
	R: message data to be sent
	M: n/a
	E: sends the message to twitch with the type PRIVMMSG
	"""
	def msg(self, message):
		self.irc.send("PRIVMSG " + twitchChannel + " :" + message + "\r\n")

	"""
	R: n/a
	M: n/a
	E: returns the message from the irc server
	"""
	def getData(self):
		return self.irc.recv(2048)